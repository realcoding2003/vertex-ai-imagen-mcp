#!/usr/bin/env python3
"""
기본 사용 예시

이 예시는 Vertex AI Imagen MCP Server의 기본적인 사용법을 보여줍니다.
"""

import asyncio
import os
import sys
import base64

# 상위 디렉토리의 src 모듈 import를 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from imagen_mcp_server import VertexAIImagenClient

async def basic_example():
    """기본적인 이미지 생성 예시"""
    
    # 환경 변수에서 설정 읽기
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not project_id or not credentials_path:
        print("❌ 환경 변수가 설정되지 않았습니다.")
        print("GOOGLE_CLOUD_PROJECT와 GOOGLE_APPLICATION_CREDENTIALS를 설정해주세요.")
        return
    
    # 클라이언트 초기화
    client = VertexAIImagenClient(project_id, location)
    
    if not client.setup_credentials(credentials_path):
        print("❌ 인증 실패")
        return
    
    print("✅ 인증 성공! 이미지 생성을 시작합니다.")
    
    try:
        # 기본 이미지 생성
        print("\n🎨 기본 이미지 생성...")
        result = await client.generate_image(
            prompt="A beautiful sunset over mountains with a peaceful lake"
        )
        
        # 결과 저장
        if result.get("predictions"):
            prediction = result["predictions"][0]
            if "bytesBase64Encoded" in prediction:
                image_data = base64.b64decode(prediction["bytesBase64Encoded"])
                filename = "basic_example.png"
                
                with open(filename, "wb") as f:
                    f.write(image_data)
                
                file_size = os.path.getsize(filename)
                print(f"✅ 이미지 저장: {filename} ({file_size:,} bytes)")
                
                if prediction.get("prompt"):
                    print(f"📝 개선된 프롬프트: {prediction['prompt']}")
        
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    asyncio.run(basic_example())
