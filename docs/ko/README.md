# Vertex AI Imagen MCP Server

🎨 **Google Cloud Vertex AI Imagen API를 사용한 고품질 이미지 생성**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4)](https://cloud.google.com/vertex-ai)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

텍스트 설명으로부터 놀라운 이미지를 생성하는 Google Cloud Vertex AI Imagen 모델을 통합한 Model Context Protocol (MCP) 서버입니다. Claude Desktop과 완벽하게 작동하며 대화형 CLI와 MCP 프로토콜 모드를 모두 지원합니다.

## ✨ 주요 기능

- 🎨 **최신 AI 모델**: Imagen 3.0 및 레거시 모델 지원
- 🔧 **MCP 통합**: Claude Desktop을 위한 완전한 Model Context Protocol 지원
- 🖥️ **독립 실행 모드**: MCP 라이브러리가 없어도 사용 가능한 대화형 CLI
- ⚙️ **다양한 옵션**: 가로세로 비율, 네거티브 프롬프트, 안전 필터 등
- 🔒 **내장 안전 기능**: 자동 콘텐츠 필터링 및 워터마킹
- 🚀 **간편한 설정**: 환경 변수만으로 간단한 구성
- 📚 **포괄적인 문서**: 영어와 한국어로 작성된 상세한 가이드

## 🚀 빠른 시작

### 사전 요구사항

- Python 3.8+
- Vertex AI API가 활성화된 Google Cloud 계정
- `Vertex AI User` 역할이 부여된 서비스 계정

### 설치

```bash
git clone https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp
pip install -r requirements.txt
```

### 설정

1. **Google Cloud 서비스 계정 생성** 및 JSON 키 다운로드
2. **환경 변수 설정**:
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   export VERTEX_AI_LOCATION="us-central1"
   ```

### 사용법

#### 독립 실행 모드 (테스트용 권장)
```bash
python src/imagen_mcp_server.py
```

#### MCP 모드 (Claude Desktop 통합)
```bash
# MCP 라이브러리 설치
pip install mcp

# Claude Desktop 설정에 추가:
{
  "mcpServers": {
    "vertex-ai-imagen": {
      "command": "python",
      "args": ["/path/to/vertex-ai-imagen-mcp/src/imagen_mcp_server.py"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-project-id",
        "VERTEX_AI_LOCATION": "us-central1",
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account-key.json"
      }
    }
  }
}
```

## 🎨 사용 예시

### 기본 생성
```python
# 간단한 프롬프트
"석양이 지는 고요한 산 풍경"

# 옵션과 함께
{
  "prompt": "하늘을 나는 자동차가 있는 미래 도시",
  "negative_prompt": "흐릿한, 저품질",
  "aspect_ratio": "16:9",
  "image_count": 2
}
```

### 고급 사용법
```python
# 특정 모델을 사용한 고품질 생성
{
  "prompt": "왕관을 쓴 고양이의 세밀한 유화",
  "model_version": "imagen-3.0-generate-002",
  "aspect_ratio": "3:4",
  "safety_setting": "block_medium_and_above",
  "seed": 12345
}
```

## 🛠️ API 참조

### 지원하는 도구

#### `generate_image`
텍스트 프롬프트로부터 이미지를 생성합니다.

**매개변수:**
- `prompt` (필수): 원하는 이미지에 대한 텍스트 설명
- `negative_prompt`: 생성된 이미지에서 피하고 싶은 내용
- `image_count`: 생성할 이미지 수 (1-4)
- `aspect_ratio`: 이미지 크기 (`1:1`, `3:4`, `4:3`, `16:9`, `9:16`)
- `model_version`: 사용할 AI 모델 (아래 지원 모델 참조)
- `safety_setting`: 콘텐츠 필터 수준
- `seed`: 재현 가능한 결과를 위한 랜덤 시드

#### `list_models`
사용 가능한 모든 Imagen 모델과 기능을 나열합니다.

### 지원하는 모델

| 모델 | 설명 | 속도 | 품질 |
|------|------|------|------|
| `imagen-3.0-generate-002` | 최신 고품질 모델 | 보통 | 최고 |
| `imagen-3.0-generate-001` | 이전 Imagen 3.0 버전 | 보통 | 최고 |
| `imagen-3.0-fast-generate-001` | 빠른 생성 모델 | 빠름 | 좋음 |
| `imagegeneration@006` | 안정적인 레거시 모델 | 보통 | 좋음 |
| `imagegeneration@005` | 이전 레거시 버전 | 보통 | 좋음 |

## 📁 프로젝트 구조

```
vertex-ai-imagen-mcp/
├── src/
│   └── imagen_mcp_server.py      # 메인 MCP 서버 구현
├── examples/
│   ├── basic_usage.py            # 기본 사용 예시
│   └── advanced_usage.py         # 고급 기능 데모
├── docs/
│   ├── setup.md                  # 상세한 설정 가이드
│   ├── api.md                    # API 문서
│   ├── troubleshooting.md        # 일반적인 문제 및 해결책
│   ├── ko/                       # 한국어 문서
│   │   ├── README.md
│   │   ├── setup.md
│   │   └── api.md
│   └── images/                   # 문서용 이미지
├── tests/
│   ├── test_api.py              # API 테스트
│   └── test_mcp.py              # MCP 통합 테스트
├── requirements.txt              # Python 의존성
├── requirements-dev.txt          # 개발용 의존성
├── setup.py                      # 패키지 구성
├── .github/
│   └── workflows/
│       ├── test.yml             # 자동 테스트
│       └── release.yml          # 릴리스 자동화
├── LICENSE                       # MIT 라이선스
└── README.md                     # 메인 README (영어)
```

## 🌐 문서

- **English**: [Setup Guide](../setup.md) | [API Reference](../api.md) | [Troubleshooting](../troubleshooting.md)
- **한국어**: [설정 가이드](setup.md) | [API 참조](api.md) | [문제 해결](troubleshooting.md)

## 🧪 개발

### 로컬 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp

# 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 개발용 의존성 설치
pip install -r requirements-dev.txt

# 테스트 실행
python -m pytest tests/

# 코드 포맷팅
black src/ tests/
flake8 src/ tests/
```

### 예시 실행

```bash
# 기본 사용법
python examples/basic_usage.py

# 고급 기능
python examples/advanced_usage.py
```

## 🤝 기여하기

기여를 환영합니다! 자세한 내용은 [기여 가이드](CONTRIBUTING.md)를 참조해주세요.

### 개발 프로세스

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 작성
4. 새로운 기능에 대한 테스트 추가
5. 모든 테스트 통과 확인 (`python -m pytest`)
6. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
7. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
8. Pull Request 열기

### 코드 스타일

- 코드 포맷팅은 [Black](https://black.readthedocs.io/) 사용
- [PEP 8](https://pep8.org/) 스타일 가이드라인 준수
- 적절한 곳에 타입 힌트 추가
- 설명적인 커밋 메시지 작성

## 📋 요구사항

### 시스템 요구사항
- Python 3.8 이상
- API 호출을 위한 인터넷 연결
- 결제가 활성화된 Google Cloud 계정

### Python 의존성
- `requests>=2.31.0` - API 호출용 HTTP 클라이언트
- `google-auth>=2.23.0` - Google Cloud 인증
- `google-auth-oauthlib>=1.1.0` - OAuth2 지원
- `google-auth-httplib2>=0.1.1` - HTTP 전송
- `mcp>=0.1.0` - Model Context Protocol (선택사항)

### Google Cloud 요구사항
- Vertex AI API가 활성화된 프로젝트
- `Vertex AI User` 역할이 있는 서비스 계정
- 프로젝트에 연결된 결제 계정

## 💰 가격

이 도구는 사용량 기반 가격의 Google Cloud Vertex AI Imagen API를 사용합니다:

- **생성된 이미지당 과금**
- **모델과 해상도에 따라 가격 변동**
- **신규 사용자를 위한 무료 등급 제공**

자세한 가격 정보는 [Google Cloud 가격 페이지](https://cloud.google.com/vertex-ai/pricing)를 방문하세요.

### 비용 최적화 팁

- 더 빠르고 저렴한 생성을 위해 `imagen-3.0-fast-generate-001` 사용
- 가능한 경우 단일 요청으로 여러 이미지 생성
- 사용량 모니터링을 위한 결제 알림 설정
- 프로토타이핑에는 낮은 해상도 사용

## 🔒 보안 및 개인정보보호

- **서비스 계정 키**: 안전하게 저장하고 정기적으로 교체
- **콘텐츠 필터링**: 유해한 콘텐츠를 방지하는 내장 안전 필터
- **데이터 개인정보보호**: 생성 후 Google에서 이미지를 저장하지 않음
- **네트워크 보안**: 모든 API 호출에 HTTPS/TLS 암호화 사용

## ❓ 문제 해결

### 일반적인 문제

**인증 오류 (403 Forbidden)**
```bash
# 해결책: 서비스 계정 권한 확인
# "Vertex AI User" 역할이 할당되었는지 확인
```

**API 비활성화 오류**
```bash
# 해결책: Vertex AI API 활성화
gcloud services enable aiplatform.googleapis.com
```

**프로젝트를 찾을 수 없음**
```bash
# 해결책: 환경 변수 확인
echo $GOOGLE_CLOUD_PROJECT
echo $GOOGLE_APPLICATION_CREDENTIALS
```

더 자세한 문제 해결은 [문제 해결 가이드](troubleshooting.md)를 참조하세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](../../LICENSE) 파일을 참조하세요.

## 🙏 감사의 말

- **Google Cloud Vertex AI** - 강력한 AI 이미지 생성 기능 제공
- **Model Context Protocol** - 원활한 AI 도구 통합 가능
- **Anthropic Claude** - 더 나은 인간-AI 협업에 영감을 줌
- **오픈 소스 커뮤니티** - 이 프로젝트를 가능하게 만듦

## 📞 지원

- **이슈**: [GitHub Issues](https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp/issues)
- **토론**: [GitHub Discussions](https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp/discussions)
- **문서**: [전체 문서](../)

## 🌟 지원 보여주기

이 프로젝트가 도움이 된다면 다음을 고려해주세요:
- ⭐ 저장소에 스타 주기
- 🐛 버그 신고하기
- 💡 새로운 기능 제안하기
- 📝 문서에 기여하기
- 🔗 다른 사람들과 공유하기

---

**커뮤니티를 위한 커뮤니티에 의한 ❤️로 제작**

*즐거운 이미지 생성하세요! 🎨*
