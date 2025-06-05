#!/usr/bin/env python3
"""
고급 사용 예시

다양한 옵션과 모델을 사용한 이미지 생성 예시
"""

import asyncio
import os
import sys
import base64
from datetime import datetime

# 상위 디렉토리의 src 모듈 import를 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from imagen_mcp_server import VertexAIImagenClient

async def advanced_example():
    """고급 옵션을 사용한 이미지 생성 예시"""
    
    # 환경 변수에서 설정 읽기
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not project_id or not credentials_path:
        print("❌ 환경 변수가 설정되지 않았습니다.")
        return
    
    # 클라이언트 초기화
    client = VertexAIImagenClient(project_id, location)
    
    if not client.setup_credentials(credentials_path):
        print("❌ 인증 실패")
        return
    
    print("✅ 인증 성공! 고급 이미지 생성을 시작합니다.")
    
    # 다양한 시나리오 테스트
    scenarios = [
        {
            "name": "고품질 풍경 (16:9)",
            "prompt": "A breathtaking mountain landscape with snow-capped peaks, crystal clear alpine lake, and dramatic sunset clouds",
            "negative_prompt": "blurry, low quality, dark, overexposed",
            "aspect_ratio": "16:9",
            "model_version": "imagen-3.0-generate-002",
            "image_count": 2
        },
        {
            "name": "빠른 생성 (정사각형)",
            "prompt": "A cute cartoon cat wearing a wizard hat, sitting on a pile of magical books",
            "aspect_ratio": "1:1",
            "model_version": "imagen-3.0-fast-generate-001",
            "image_count": 1
        },
        {
            "name": "안정적인 모델 (세로)",
            "prompt": "A futuristic cityscape with flying cars and neon lights, cyberpunk style",
            "negative_prompt": "boring, simple, outdated",
            "aspect_ratio": "9:16",
            "model_version": "imagegeneration@006",
            "image_count": 1,
            "seed": 12345
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"🎨 시나리오 {i}: {scenario['name']}")
        print(f"{'='*60}")
        print(f"프롬프트: {scenario['prompt']}")
        print(f"모델: {scenario['model_version']}")
        print(f"비율: {scenario['aspect_ratio']}")
        print(f"개수: {scenario['image_count']}")
        
        try:
            start_time = datetime.now()
            
            # 이미지 생성
            result = await client.generate_image(**scenario)
            
            generation_time = (datetime.now() - start_time).total_seconds()
            print(f"⏱️ 생성 시간: {generation_time:.2f}초")
            
            # 결과 저장
            predictions = result.get("predictions", [])
            if predictions:
                print(f"✅ {len(predictions)}개 이미지 생성 성공!")
                
                for j, prediction in enumerate(predictions):
                    if "bytesBase64Encoded" in prediction:
                        image_data = base64.b64decode(prediction["bytesBase64Encoded"])
                        
                        # 파일명 생성
                        safe_name = scenario['name'].replace(' ', '_').replace('(', '').replace(')', '')
                        filename = f"advanced_{i}_{safe_name}_{j+1}.png"
                        
                        with open(filename, "wb") as f:
                            f.write(image_data)
                        
                        file_size = os.path.getsize(filename)
                        print(f"💾 저장: {filename} ({file_size:,} bytes)")
                        
                        # 개선된 프롬프트 표시
                        if prediction.get("prompt"):
                            print(f"📝 개선된 프롬프트: {prediction['prompt']}")
            else:
                print("❌ 이미지 생성 실패")
                
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    print(f"\n🎉 모든 시나리오 완료!")

async def batch_generation_example():
    """배치 생성 예시"""
    print("\n" + "="*60)
    print("🎨 배치 이미지 생성 예시")
    print("="*60)
    
    # 환경 변수에서 설정 읽기
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not project_id or not credentials_path:
        return
    
    client = VertexAIImagenClient(project_id, location)
    
    if not client.setup_credentials(credentials_path):
        return
    
    # 여러 프롬프트를 한 번에 처리
    prompts = [
        "A serene Japanese garden with cherry blossoms",
        "A modern minimalist living room with natural light",
        "A vintage bookstore with cozy reading corners",
        "A tropical beach at sunset with palm trees"
    ]
    
    tasks = []
    for prompt in prompts:
        task = client.generate_image(
            prompt=prompt,
            aspect_ratio="3:4",
            model_version="imagegeneration@006"
        )
        tasks.append(task)
    
    try:
        # 동시에 모든 이미지 생성
        start_time = datetime.now()
        results = await asyncio.gather(*tasks)
        total_time = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ {len(results)}개 이미지 배치 생성 완료!")
        print(f"⏱️ 총 소요 시간: {total_time:.2f}초")
        
        # 결과 저장
        for i, (prompt, result) in enumerate(zip(prompts, results)):
            if result.get("predictions"):
                prediction = result["predictions"][0]
                if "bytesBase64Encoded" in prediction:
                    image_data = base64.b64decode(prediction["bytesBase64Encoded"])
                    filename = f"batch_{i+1}_{prompt[:20].replace(' ', '_')}.png"
                    
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    
                    file_size = os.path.getsize(filename)
                    print(f"💾 {filename} ({file_size:,} bytes)")
    
    except Exception as e:
        print(f"❌ 배치 생성 오류: {e}")

if __name__ == "__main__":
    async def main():
        await advanced_example()
        await batch_generation_example()
    
    asyncio.run(main())
