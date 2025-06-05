#!/usr/bin/env python3
"""
Google Cloud Vertex AI Imagen MCP Server

🎨 텍스트 프롬프트로부터 고품질 이미지를 생성하는 MCP 서버

Author: Claude & Kevin Park
License: MIT
Version: 1.0.0
"""

import asyncio
import base64
import json
import os
import sys
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

# Google Cloud 라이브러리
try:
    import requests
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
except ImportError:
    print("❌ 필요한 라이브러리를 설치해주세요:")
    print("pip install requests google-auth google-auth-oauthlib google-auth-httplib2")
    sys.exit(1)

# MCP 라이브러리 (선택사항)
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolRequest, CallToolResult, ListToolsRequest, ListToolsResult,
        Tool, TextContent, ImageContent, EmbeddedResource
    )
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VertexAIImagenClient:
    """Vertex AI Imagen API 클라이언트"""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.credentials = None
        self.base_url = f"https://{location}-aiplatform.googleapis.com/v1"
        
        # 지원되는 모델 목록
        self.supported_models = [
            "imagegeneration@006",
            "imagegeneration@005", 
            "imagegeneration@002",
            "imagen-3.0-generate-001",
            "imagen-3.0-generate-002",
            "imagen-3.0-fast-generate-001"
        ]
        
    def setup_credentials(self, service_account_path: str) -> bool:
        """서비스 계정 키로 인증 설정"""
        try:
            if not os.path.exists(service_account_path):
                raise FileNotFoundError(f"서비스 계정 키 파일을 찾을 수 없습니다: {service_account_path}")
            
            self.credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            
            if not self.credentials.valid:
                self.credentials.refresh(Request())
            
            logger.info("✅ Google Cloud 인증 성공")
            return True
            
        except Exception as e:
            logger.error(f"❌ 인증 실패: {e}")
            return False
    
    async def generate_image(self, **kwargs) -> Dict[str, Any]:
        """이미지 생성"""
        prompt = kwargs.get("prompt")
        model_version = kwargs.get("model_version", "imagegeneration@006")
        image_count = kwargs.get("image_count", 1)
        aspect_ratio = kwargs.get("aspect_ratio", "1:1")
        
        # 모델 버전 검증
        if model_version not in self.supported_models:
            raise ValueError(f"지원되지 않는 모델: {model_version}. 지원 모델: {self.supported_models}")
        
        url = (
            f"{self.base_url}/projects/{self.project_id}/locations/{self.location}/"
            f"publishers/google/models/{model_version}:predict"
        )
        
        # 요청 데이터 구성
        request_data = {
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": min(image_count, 4),
                "aspectRatio": aspect_ratio,
                "addWatermark": kwargs.get("add_watermark", False)
            }
        }
        
        # 선택적 매개변수 추가
        if kwargs.get("negative_prompt"):
            request_data["parameters"]["negativePrompt"] = kwargs["negative_prompt"]
        
        if kwargs.get("safety_setting"):
            request_data["parameters"]["safetySetting"] = kwargs["safety_setting"]
        
        if kwargs.get("enhance_prompt", True):
            request_data["parameters"]["enhancePrompt"] = True
        
        if kwargs.get("seed") is not None:
            request_data["parameters"]["seed"] = kwargs["seed"]
            request_data["parameters"]["addWatermark"] = False  # 시드 사용시 워터마크 비활성화
        
        headers = {
            "Authorization": f"Bearer {self.credentials.token}",
            "Content-Type": "application/json"
        }
        
        try:
            logger.info(f"🎨 이미지 생성: {prompt[:50]}...")
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(url, json=request_data, headers=headers, timeout=180)
            )
            
            if response.status_code != 200:
                error_message = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ API 오류: {error_message}")
                raise Exception(error_message)
            
            result = response.json()
            logger.info(f"✅ 생성 완료: {len(result.get('predictions', []))}개 이미지")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 생성 실패: {e}")
            raise

if HAS_MCP:
    # 실제 MCP 서버 구현
    class ImagenMCPServer:
        def __init__(self):
            self.server = Server("vertex-ai-imagen")
            self.client = None
            self.setup_handlers()

        def setup_handlers(self):
            @self.server.list_tools()
            async def handle_list_tools() -> ListToolsResult:
                return ListToolsResult(
                    tools=[
                        Tool(
                            name="generate_image",
                            description="텍스트 프롬프트로부터 고품질 이미지 생성",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "prompt": {
                                        "type": "string",
                                        "description": "이미지 생성을 위한 텍스트 프롬프트"
                                    },
                                    "negative_prompt": {
                                        "type": "string",
                                        "description": "피하고 싶은 내용 (선택사항)"
                                    },
                                    "image_count": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 4,
                                        "default": 1,
                                        "description": "생성할 이미지 수"
                                    },
                                    "aspect_ratio": {
                                        "type": "string",
                                        "enum": ["1:1", "3:4", "4:3", "16:9", "9:16"],
                                        "default": "1:1",
                                        "description": "가로세로 비율"
                                    },
                                    "model_version": {
                                        "type": "string",
                                        "enum": [
                                            "imagegeneration@006",
                                            "imagegeneration@005", 
                                            "imagen-3.0-generate-001",
                                            "imagen-3.0-generate-002",
                                            "imagen-3.0-fast-generate-001"
                                        ],
                                        "default": "imagegeneration@006",
                                        "description": "사용할 모델 버전"
                                    },
                                    "safety_setting": {
                                        "type": "string",
                                        "enum": [
                                            "block_low_and_above",
                                            "block_medium_and_above", 
                                            "block_only_high"
                                        ],
                                        "default": "block_medium_and_above",
                                        "description": "안전 필터 수준"
                                    },
                                    "seed": {
                                        "type": "integer",
                                        "description": "재현 가능한 결과를 위한 시드 값 (선택사항)"
                                    }
                                },
                                "required": ["prompt"]
                            }
                        ),
                        Tool(
                            name="list_models",
                            description="사용 가능한 Imagen 모델 목록 조회",
                            inputSchema={
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        )
                    ]
                )

            @self.server.call_tool()
            async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
                try:
                    if name == "generate_image":
                        return await self._generate_image(**arguments)
                    elif name == "list_models":
                        return await self._list_models()
                    else:
                        raise ValueError(f"알 수 없는 도구: {name}")
                except Exception as e:
                    logger.error(f"도구 호출 오류: {e}")
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"❌ 오류: {str(e)}")]
                    )

        async def _generate_image(self, **kwargs) -> CallToolResult:
            """이미지 생성 처리"""
            if not self.client:
                raise Exception("클라이언트가 초기화되지 않았습니다")

            prompt = kwargs.get("prompt")
            result = await self.client.generate_image(**kwargs)

            content = []
            content.append(TextContent(
                type="text",
                text=f"✅ {len(result.get('predictions', []))}개의 이미지가 생성되었습니다.\n프롬프트: {prompt}"
            ))

            # 생성된 이미지들을 응답에 추가
            for i, prediction in enumerate(result.get("predictions", [])):
                if "bytesBase64Encoded" in prediction:
                    image_data = prediction["bytesBase64Encoded"]
                    mime_type = prediction.get("mimeType", "image/png")
                    
                    content.append(ImageContent(
                        type="image",
                        data=image_data,
                        mimeType=mime_type
                    ))
                    
                    # 개선된 프롬프트 표시
                    if prediction.get("prompt"):
                        content.append(TextContent(
                            type="text",
                            text=f"📝 개선된 프롬프트 {i+1}: {prediction['prompt']}"
                        ))

            return CallToolResult(content=content)

        async def _list_models(self) -> CallToolResult:
            """모델 목록 조회"""
            if not self.client:
                raise Exception("클라이언트가 초기화되지 않았습니다")
            
            models_info = []
            for model in self.client.supported_models:
                if "imagen-3.0" in model:
                    description = "Imagen 3.0 - 최신 고품질 이미지 생성"
                    if "fast" in model:
                        description += " (빠른 생성)"
                else:
                    description = f"Imagen {model.split('@')[1]} - 안정적인 이미지 생성"
                
                models_info.append(f"• {model}: {description}")
            
            content = [TextContent(
                type="text", 
                text=f"🤖 사용 가능한 모델 ({len(self.client.supported_models)}개):\n\n" + "\n".join(models_info)
            )]
            
            return CallToolResult(content=content)

        async def run(self):
            """MCP 서버 실행"""
            # 환경 변수 확인
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

            if not project_id or not credentials_path:
                logger.error("필수 환경 변수가 설정되지 않았습니다")
                logger.error("GOOGLE_CLOUD_PROJECT와 GOOGLE_APPLICATION_CREDENTIALS를 설정해주세요")
                sys.exit(1)

            # 클라이언트 초기화
            self.client = VertexAIImagenClient(project_id, location)
            
            if not self.client.setup_credentials(credentials_path):
                logger.error("인증 설정 실패")
                sys.exit(1)

            logger.info("🚀 Vertex AI Imagen MCP Server 시작")
            logger.info(f"프로젝트: {project_id}")
            logger.info(f"위치: {location}")
            
            # MCP 서버 실행
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(read_stream, write_stream, InitializationOptions())

else:
    # MCP 라이브러리가 없을 때의 독립 실행 모드
    class ImagenMCPServer:
        def __init__(self):
            self.client = None

        async def initialize(self):
            """서버 초기화"""
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

            if not project_id:
                print("❌ GOOGLE_CLOUD_PROJECT 환경 변수가 설정되지 않았습니다")
                print("예시: export GOOGLE_CLOUD_PROJECT='your-project-id'")
                raise Exception("환경 변수 미설정")

            if not credentials_path:
                print("❌ GOOGLE_APPLICATION_CREDENTIALS 환경 변수가 설정되지 않았습니다")
                print("예시: export GOOGLE_APPLICATION_CREDENTIALS='/path/to/service-account-key.json'")
                raise Exception("환경 변수 미설정")

            self.client = VertexAIImagenClient(project_id, location)
            
            if not self.client.setup_credentials(credentials_path):
                raise Exception("인증 설정 실패")

            logger.info("🚀 Imagen MCP Server (독립 모드) 초기화 완료")
            logger.info(f"프로젝트: {project_id}")
            logger.info(f"위치: {location}")
            logger.info(f"지원 모델: {', '.join(self.client.supported_models)}")

        async def generate_image_interactive(self):
            """대화형 이미지 생성"""
            print(f"\n🎨 Vertex AI Imagen 이미지 생성기")
            print("명령어: 'quit' (종료), 'models' (모델 목록)")
            
            while True:
                try:
                    print("\n" + "="*60)
                    
                    command = input("명령어 또는 프롬프트를 입력하세요: ").strip()
                    
                    if command.lower() == 'quit':
                        print("👋 종료합니다.")
                        break
                    
                    if command.lower() == 'models':
                        print("\n🤖 사용 가능한 모델:")
                        for model in self.client.supported_models:
                            if "imagen-3.0" in model:
                                desc = "최신 고품질 모델"
                                if "fast" in model:
                                    desc += " (빠른 생성)"
                            else:
                                desc = f"안정적인 모델 v{model.split('@')[1]}"
                            print(f"  • {model}: {desc}")
                        continue
                    
                    if not command:
                        print("❌ 프롬프트를 입력해주세요.")
                        continue
                    
                    prompt = command
                    
                    # 추가 옵션 입력
                    print(f"\n📋 추가 옵션 (Enter로 기본값 사용):")
                    
                    image_count = input("이미지 수 (1-4, 기본값: 1): ").strip()
                    image_count = int(image_count) if image_count.isdigit() else 1
                    image_count = min(max(image_count, 1), 4)
                    
                    aspect_ratio = input("가로세로 비율 (1:1, 16:9, 9:16 등, 기본값: 1:1): ").strip()
                    if aspect_ratio not in ["1:1", "3:4", "4:3", "16:9", "9:16"]:
                        aspect_ratio = "1:1"
                    
                    model_version = input(f"모델 (기본값: imagegeneration@006): ").strip()
                    if model_version not in self.client.supported_models:
                        model_version = "imagegeneration@006"
                    
                    negative_prompt = input("제외할 내용 (선택사항): ").strip() or None
                    
                    print(f"\n🎨 이미지 생성 중...")
                    print(f"  📝 프롬프트: {prompt}")
                    print(f"  🔢 개수: {image_count}")
                    print(f"  📐 비율: {aspect_ratio}")
                    print(f"  🤖 모델: {model_version}")
                    
                    start_time = datetime.now()
                    
                    # 이미지 생성
                    result = await self.client.generate_image(
                        prompt=prompt,
                        image_count=image_count,
                        aspect_ratio=aspect_ratio,
                        model_version=model_version,
                        negative_prompt=negative_prompt
                    )
                    
                    generation_time = (datetime.now() - start_time).total_seconds()
                    
                    # 결과 처리
                    predictions = result.get("predictions", [])
                    if predictions:
                        print(f"\n✅ {len(predictions)}개 이미지 생성 성공! (소요시간: {generation_time:.1f}초)")
                        
                        # 이미지 저장
                        for i, prediction in enumerate(predictions):
                            if "bytesBase64Encoded" in prediction:
                                image_data = base64.b64decode(prediction["bytesBase64Encoded"])
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                safe_prompt = "".join(c for c in prompt[:20] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                                filename = f"imagen_{timestamp}_{safe_prompt.replace(' ', '_')}_{i+1}.png"
                                
                                # 현재 디렉토리에 저장
                                filepath = os.path.join(os.getcwd(), filename)
                                
                                with open(filepath, "wb") as f:
                                    f.write(image_data)
                                
                                file_size = os.path.getsize(filepath)
                                print(f"  💾 저장됨: {filename} ({file_size:,} bytes)")
                                
                                # 개선된 프롬프트 표시
                                if prediction.get("prompt"):
                                    print(f"  📝 개선된 프롬프트 {i+1}: {prediction['prompt']}")
                    else:
                        print("❌ 이미지가 생성되지 않았습니다.")
                        print(f"응답: {result}")
                        
                except KeyboardInterrupt:
                    print("\n👋 종료합니다.")
                    break
                except Exception as e:
                    print(f"❌ 오류: {e}")
                    import traceback
                    traceback.print_exc()

async def main():
    """메인 함수"""
    server = ImagenMCPServer()
    
    if HAS_MCP:
        # MCP 모드로 실행
        logger.info("MCP 서버 모드로 실행")
        await server.run()
    else:
        # 독립 실행 모드
        logger.info("독립 실행 모드로 시작")
        try:
            await server.initialize()
            await server.generate_image_interactive()
        except Exception as e:
            print(f"❌ 초기화 실패: {e}")
            sys.exit(1)

if __name__ == "__main__":
    print("🎨 Vertex AI Imagen MCP Server v1.0.0")
    print("=" * 50)
    
    if not HAS_MCP:
        print("⚠️ MCP 라이브러리가 없어 독립 실행 모드로 동작합니다.")
        print("MCP 통합을 위해서는 'pip install mcp' 를 실행하세요.\n")
    
    # 환경 변수 확인
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not project_id or not credentials_path:
        print("❌ 필수 환경 변수가 설정되지 않았습니다:")
        if not project_id:
            print("  - GOOGLE_CLOUD_PROJECT")
        if not credentials_path:
            print("  - GOOGLE_APPLICATION_CREDENTIALS")
        print("\n설정 예시:")
        print("export GOOGLE_CLOUD_PROJECT='your-project-id'")
        print("export GOOGLE_APPLICATION_CREDENTIALS='/path/to/service-account-key.json'")
        print("export VERTEX_AI_LOCATION='us-central1'")
        sys.exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 서버 종료")
    except Exception as e:
        print(f"❌ 서버 실행 실패: {e}")
        sys.exit(1)
