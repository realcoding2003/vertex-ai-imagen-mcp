#!/usr/bin/env python3
"""
Google Cloud Vertex AI Imagen MCP Server (Simple Version)

🎨 vertex-ai-imagen 패키지를 활용한 간단한 MCP 서버

Author: Kevin Park
License: MIT
Version: 2.0.0
"""

import asyncio
import json
import os
import sys
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

# vertex-ai-imagen 패키지
try:
    from vertex_ai_imagen import ImagenClient
except ImportError:
    # MCP 모드에서는 조용히 종료
    if not sys.stdin.isatty():
        sys.exit(1)
    print("❌ vertex-ai-imagen 패키지를 설치해주세요:", file=sys.stderr)
    print("pip install vertex-ai-imagen", file=sys.stderr)
    sys.exit(1)

# 로깅 설정 - stderr로만 출력
logging.basicConfig(
    level=logging.ERROR,  # ERROR 레벨만 출력
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # stderr로 출력
)
logger = logging.getLogger(__name__)

# 전역 클라이언트
imagen_client = None

async def initialize_client():
    """ImagenClient 초기화"""
    global imagen_client
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT 환경변수가 설정되지 않았습니다.")
    
    imagen_client = ImagenClient(project_id=project_id)
    
    # 인증 설정
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        imagen_client.setup_credentials(credentials_path)
    else:
        # 환경에서 기본 인증 시도
        try:
            imagen_client.setup_credentials_from_env()
        except Exception:
            # 인증 실패 시 조용히 처리
            pass

async def handle_generate_image(params: Dict[str, Any]) -> Dict[str, Any]:
    """이미지 생성 처리"""
    try:
        # 클라이언트 초기화 확인
        global imagen_client
        if not imagen_client:
            await initialize_client()
        
        # 매개변수 추출
        prompt = params.get("prompt", "")
        if not prompt:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "❌ 오류: prompt는 필수 매개변수입니다."
                    }
                ]
            }
        
        kwargs = {
            "prompt": prompt,
            "count": min(params.get("count", 1), 4),
            "aspect_ratio": params.get("aspect_ratio", "1:1"),
            "model": params.get("model", "imagegeneration@006"),
            "safety_setting": params.get("safety_setting", "block_some")
        }
        
        if params.get("negative_prompt"):
            kwargs["negative_prompt"] = params["negative_prompt"]
        
        if params.get("seed") is not None:
            kwargs["seed"] = params["seed"]
        
        # 이미지 생성
        result = await imagen_client.generate(**kwargs)
        
        # 결과 처리
        if isinstance(result, list):
            images = result
        else:
            images = [result]
        
        # 저장 처리
        saved_files = []
        save_path = params.get("save_path")
        if save_path:
            os.makedirs(save_path, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_prefix = params.get("filename_prefix", "generated_image")
            
            for i, image in enumerate(images):
                filename = f"{filename_prefix}_{timestamp}_{i+1}.png"
                filepath = os.path.join(save_path, filename)
                image.save(filepath)
                saved_files.append(filepath)
        
        # 결과 구성
        result_text = f"✅ {len(images)}개 이미지 생성 완료!\n\n"
        
        for i, image in enumerate(images):
            result_text += f"🎨 이미지 {i+1}: {image.size:,} bytes\n"
        
        if saved_files:
            result_text += f"\n📁 저장된 파일들:\n"
            for filepath in saved_files:
                result_text += f"  📎 {filepath}\n"
        else:
            result_text += "\n💡 save_path를 지정하면 파일로 저장됩니다.\n"
        
        # 텍스트만 반환 (이미지는 일단 제외)
        response_content = [{"type": "text", "text": result_text}]
        
        return {"content": response_content}
        
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text", 
                    "text": f"❌ 이미지 생성 실패: {str(e)}"
                }
            ]
        }

async def handle_list_models() -> Dict[str, Any]:
    """모델 목록 처리"""
    try:
        global imagen_client
        if not imagen_client:
            await initialize_client()
        
        models = imagen_client.list_models()
        model_list = "\n".join([f"• {model}" for model in models])
        result_text = f"🤖 사용 가능한 Imagen 모델:\n\n{model_list}"
        
        return {"content": [{"type": "text", "text": result_text}]}
        
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ 모델 목록 조회 실패: {str(e)}"
                }
            ]
        }

async def handle_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """메시지 처리"""
    try:
        method = message.get("method")
        params = message.get("params", {})
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "vertex-ai-imagen",
                        "version": "2.0.0"
                    }
                }
            }
        
        elif method == "notifications/initialized":
            # 초기화 완료 알림 - 응답 불필요
            return None
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "generate_image",
                            "description": "텍스트 프롬프트로부터 고품질 이미지 생성",
                            "inputSchema": {
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
                                    "count": {
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
                                    "model": {
                                        "type": "string",
                                        "default": "imagegeneration@006",
                                        "description": "사용할 Imagen 모델"
                                    },
                                    "seed": {
                                        "type": "integer",
                                        "description": "재현 가능한 결과를 위한 시드 값 (선택사항)"
                                    },
                                    "safety_setting": {
                                        "type": "string",
                                        "default": "block_some",
                                        "description": "안전 필터 설정"
                                    },
                                    "save_path": {
                                        "type": "string",
                                        "description": "이미지를 저장할 경로 (선택사항)"
                                    },
                                    "filename_prefix": {
                                        "type": "string",
                                        "default": "generated_image",
                                        "description": "저장할 파일명 접두사"
                                    }
                                },
                                "required": ["prompt"]
                            }
                        },
                        {
                            "name": "list_models",
                            "description": "사용 가능한 Imagen 모델 목록 조회",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name == "generate_image":
                result = await handle_generate_image(tool_args)
            elif tool_name == "list_models":
                result = await handle_list_models()
            else:
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"❌ 알 수 없는 도구: {tool_name}"
                        }
                    ]
                }
            
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": result
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {"code": -32601, "message": f"알 수 없는 메서드: {method}"}
            }
            
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "error": {"code": -32603, "message": f"내부 오류: {str(e)}"}
        }

async def stdio_server():
    """STDIO MCP 서버"""
    try:
        while True:
            # 표준 입력에서 메시지 읽기
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                message = json.loads(line)
                response = await handle_message(message)
                
                # 응답이 있는 경우만 출력 (notifications는 None 반환)
                if response is not None:
                    print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                # JSON 오류는 무시
                continue
                
    except KeyboardInterrupt:
        pass
    except Exception:
        pass

async def interactive_mode():
    """대화형 모드"""
    print("🎨 Vertex AI Imagen MCP Server", file=sys.stderr)
    print("대화형 모드로 실행됩니다.", file=sys.stderr)
    
    try:
        await initialize_client()
        print("✅ 초기화 완료", file=sys.stderr)
        
        while True:
            try:
                print("\n📝 이미지 생성 옵션:", file=sys.stderr)
                prompt = input("프롬프트: ").strip()
                if not prompt:
                    break
                
                print(f"🎨 이미지 생성 중... ({prompt[:30]}...)", file=sys.stderr)
                
                result = await handle_generate_image({"prompt": prompt})
                
                if "error" in result:
                    print(f"❌ {result['error']}", file=sys.stderr)
                else:
                    print(result["content"][0]["text"], file=sys.stderr)
                
                continue_choice = input("\n계속하시겠습니까? (y/N): ").strip().lower()
                if continue_choice not in ['y', 'yes']:
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 종료합니다.", file=sys.stderr)
                break
            except Exception as e:
                print(f"❌ 오류: {e}", file=sys.stderr)
                continue
                
    except Exception as e:
        print(f"초기화 실패: {e}", file=sys.stderr)

async def main():
    """메인 함수"""
    # 표준 입력이 터미널인지 확인
    if sys.stdin.isatty():
        # 대화형 모드
        await interactive_mode()
    else:
        # MCP STDIO 모드
        await stdio_server()

if __name__ == "__main__":
    asyncio.run(main()) 