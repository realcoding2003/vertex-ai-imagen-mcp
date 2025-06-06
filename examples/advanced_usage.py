#!/usr/bin/env python3
"""
Vertex AI Imagen MCP Server 고급 사용 예제

다양한 모델과 매개변수를 사용하는 방법을 보여줍니다.
"""

import asyncio
import os
import base64
from datetime import datetime
from vertex_ai_imagen_mcp import VertexAIImagenClient

async def generate_with_different_models():
    """다양한 모델로 이미지 생성"""
    
    client = VertexAIImagenClient(
        os.getenv("GOOGLE_CLOUD_PROJECT"),
        os.getenv("VERTEX_AI_LOCATION", "us-central1")
    )
    
    if not client.setup_credentials(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")):
        print("❌ 인증 실패")
        return
    
    prompt = "A futuristic city with flying cars"
    
    # 테스트할 모델들
    models = [
        ("imagegeneration@006", "안정적인 모델"),
        ("imagen-3.0-fast-generate-001", "빠른 생성 모델"),
        ("imagen-3.0-generate-002", "고품질 모델")
    ]
    
    for model, description in models:
        print(f"\n🎨 {model} ({description}) 테스트 중...")
        
        try:
            start_time = datetime.now()
            
            result = await client.generate_image(
                prompt=prompt,
                model_version=model,
                aspect_ratio="16:9"
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            predictions = result.get("predictions", [])
            if predictions:
                # 이미지 저장
                image_data = base64.b64decode(predictions[0]["bytesBase64Encoded"])
                filename = f"example_{model.replace('@', '_').replace('-', '_')}.png"
                
                with open(filename, "wb") as f:
                    f.write(image_data)
                
                file_size = len(image_data)
                print(f"  ✅ 성공: {duration:.2f}초, {file_size:,} bytes")
                print(f"  💾 저장: {filename}")
            else:
                print(f"  ❌ 실패")
                
        except Exception as e:
            print(f"  ❌ 오류: {e}")

async def generate_with_advanced_options():
    """고급 옵션을 사용한 이미지 생성"""
    
    client = VertexAIImagenClient(
        os.getenv("GOOGLE_CLOUD_PROJECT"),
        os.getenv("VERTEX_AI_LOCATION", "us-central1")
    )
    
    if not client.setup_credentials(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")):
        print("❌ 인증 실패")
        return
    
    print("\n🎛️ 고급 옵션 테스트")
    
    # 고급 옵션 예제들
    examples = [
        {
            "name": "부정적 프롬프트 사용",
            "params": {
                "prompt": "A beautiful garden with flowers",
                "negative_prompt": "wilted, dead, brown, ugly",
                "aspect_ratio": "4:3"
            }
        },
        {
            "name": "시드를 사용한 재현 가능한 이미지",
            "params": {
                "prompt": "A random abstract pattern",
                "seed": 12345,
                "aspect_ratio": "1:1"
            }
        },
        {
            "name": "여러 이미지 생성",
            "params": {
                "prompt": "A cute cartoon character",
                "image_count": 3,
                "aspect_ratio": "1:1"
            }
        },
        {
            "name": "세로 이미지",
            "params": {
                "prompt": "A tall skyscraper reaching into the clouds",
                "aspect_ratio": "9:16"
            }
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name']}")
        
        try:
            result = await client.generate_image(**example['params'])
            
            predictions = result.get("predictions", [])
            if predictions:
                print(f"  ✅ {len(predictions)}개 이미지 생성 성공")
                
                # 모든 이미지 저장
                for j, prediction in enumerate(predictions):
                    image_data = base64.b64decode(prediction["bytesBase64Encoded"])
                    filename = f"advanced_example_{i}_{j+1}.png"
                    
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    
                    print(f"  💾 저장: {filename}")
                    
                    # 개선된 프롬프트 표시
                    if prediction.get("prompt"):
                        enhanced = prediction["prompt"]
                        original = example['params']['prompt']
                        if enhanced != original:
                            print(f"  📝 개선된 프롬프트: {enhanced}")
            else:
                print(f"  ❌ 이미지 생성 실패")
                
        except Exception as e:
            print(f"  ❌ 오류: {e}")

async def batch_generation():
    """배치 이미지 생성 예제"""
    
    client = VertexAIImagenClient(
        os.getenv("GOOGLE_CLOUD_PROJECT"),
        os.getenv("VERTEX_AI_LOCATION", "us-central1")
    )
    
    if not client.setup_credentials(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")):
        print("❌ 인증 실패")
        return
    
    print("\n📦 배치 이미지 생성")
    
    # 여러 프롬프트 배치 처리
    prompts = [
        "A serene mountain landscape",
        "A busy city street at night",
        "A cozy coffee shop interior",
        "A magical fantasy castle",
        "A peaceful beach at sunset"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{i}/{len(prompts)}: {prompt}")
        
        try:
            result = await client.generate_image(
                prompt=prompt,
                model_version="imagen-3.0-fast-generate-001",  # 빠른 모델 사용
                aspect_ratio="16:9"
            )
            
            predictions = result.get("predictions", [])
            if predictions:
                image_data = base64.b64decode(predictions[0]["bytesBase64Encoded"])
                filename = f"batch_{i:02d}_{prompt[:20].replace(' ', '_')}.png"
                
                with open(filename, "wb") as f:
                    f.write(image_data)
                
                print(f"  ✅ 완료: {filename}")
            else:
                print(f"  ❌ 실패")
                
        except Exception as e:
            print(f"  ❌ 오류: {e}")

async def main():
    """메인 함수"""
    
    # 환경 변수 확인
    required_vars = ["GOOGLE_CLOUD_PROJECT", "GOOGLE_APPLICATION_CREDENTIALS"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ 다음 환경 변수를 설정해주세요:")
        for var in missing_vars:
            print(f"  export {var}='your-value'")
        return
    
    print("🎨 Vertex AI Imagen 고급 사용 예제")
    print("=" * 50)
    
    # 각 예제 실행
    await generate_with_different_models()
    await generate_with_advanced_options()
    await batch_generation()
    
    print("\n🎉 모든 예제 완료!")
    print("생성된 이미지 파일들을 확인해보세요.")

if __name__ == "__main__":
    asyncio.run(main())
