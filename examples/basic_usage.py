#!/usr/bin/env python3
"""
Vertex AI Imagen 기본 사용법 예제

이 예제는 vertex-ai-imagen 패키지를 직접 사용하여 
이미지를 생성하는 방법을 보여줍니다.
"""

import asyncio
import os
from vertex_ai_imagen import ImagenClient

async def main():
    """기본 사용법 예제"""
    
    # 환경 변수 확인
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT 환경변수를 설정해주세요")
        return
    
    # 클라이언트 초기화
    print("🚀 ImagenClient 초기화 중...")
    client = ImagenClient(project_id=project_id)
    
    # 인증 설정
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        client.setup_credentials(credentials_path)
    else:
        client.setup_credentials_from_env()
    
    print("✅ 인증 완료")
    
    # 기본 이미지 생성
    print("\n🎨 기본 이미지 생성...")
    try:
        images = await client.generate(
            prompt="A beautiful sunset over the ocean",
            aspect_ratio="16:9"
        )
        
        # 결과가 단일 객체인지 리스트인지 확인
        if isinstance(images, list):
            image_list = images
        else:
            image_list = [images]
        
        # 첫 번째 이미지 저장
        image = image_list[0]
        filename = "example_sunset.png"
        image.save(filename)
        
        print(f"✅ 이미지 저장: {filename}")
        print(f"   크기: {image.size:,} bytes")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return
    
    # 다중 이미지 생성
    print("\n🎨 다중 이미지 생성...")
    try:
        images = await client.generate(
            prompt="A cute cat playing with a ball of yarn",
            count=3,
            aspect_ratio="1:1",
            model="imagen-3.0-fast-generate-001"
        )
        
        # 결과가 단일 객체인지 리스트인지 확인
        if isinstance(images, list):
            image_list = images
        else:
            image_list = [images]
        
        for i, image in enumerate(image_list):
            filename = f"example_cat_{i+1}.png"
            image.save(filename)
            print(f"✅ 이미지 {i+1} 저장: {filename}")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return
    
    # 고급 옵션 사용
    print("\n🎨 고급 옵션 사용...")
    try:
        images = await client.generate(
            prompt="A futuristic city with flying cars and neon lights",
            negative_prompt="blurry, low quality, dark",
            aspect_ratio="16:9",
            model="imagen-3.0-generate-001",
            seed=12345,
            safety_setting="block_few"
        )
        
        # 결과가 단일 객체인지 리스트인지 확인
        if isinstance(images, list):
            image_list = images
        else:
            image_list = [images]
        
        image = image_list[0]
        filename = "example_futuristic_city.png"
        image.save(filename)
        
        print(f"✅ 고급 이미지 저장: {filename}")
        print(f"   크기: {image.size:,} bytes")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return
    
    # 사용 가능한 모델 목록
    print("\n🤖 사용 가능한 모델 목록:")
    try:
        models = client.list_models()
        for model in models:
            print(f"  • {model}")
    except Exception as e:
        print(f"❌ 모델 목록 조회 오류: {e}")
    
    print("\n✨ 모든 예제 완료!")

if __name__ == "__main__":
    print("🎨 Vertex AI Imagen 기본 사용법 예제")
    print("=" * 50)
    asyncio.run(main())
