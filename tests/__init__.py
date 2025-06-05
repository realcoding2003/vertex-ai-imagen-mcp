"""
테스트를 위한 초기화 파일
"""

import os
import sys

# 테스트용 환경 변수 설정
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "test-project")
os.environ.setdefault("VERTEX_AI_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "test-credentials.json")

# src 디렉토리를 Python path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
