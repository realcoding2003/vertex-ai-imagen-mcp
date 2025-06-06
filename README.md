# 🎨 Vertex AI Imagen MCP Server

**Google Cloud Vertex AI Imagen을 위한 Model Context Protocol (MCP) 서버**

이 MCP 서버는 [vertex-ai-imagen](https://github.com/realcoding2003/vertex-ai-imagen) 패키지를 활용하여 Claude Desktop에서 직접 고품질 AI 이미지를 생성할 수 있게 해줍니다.

## ✨ 주요 기능

- 🎯 **간단한 설정**: `vertex-ai-imagen` 패키지 기반의 간소화된 구조
- 🚀 **Claude Desktop 통합**: MCP를 통한 원활한 이미지 생성
- 🎨 **다양한 모델 지원**: Imagen 3.0, imagegeneration@006 등
- 🔧 **유연한 옵션**: 가로세로 비율, 이미지 수, 안전 설정 등
- 🔒 **안전한 인증**: Google Cloud 서비스 계정 기반

## 🛠️ 설치 및 설정

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Google Cloud 설정

#### 3.1 Google Cloud Project 설정
```bash
# Google Cloud CLI 설치 후
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Vertex AI API 활성화
gcloud services enable aiplatform.googleapis.com
```

#### 3.2 서비스 계정 생성
```bash
# 서비스 계정 생성
gcloud iam service-accounts create imagen-mcp \
  --display-name="Imagen MCP Server"

# 권한 부여
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:imagen-mcp@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# 키 파일 생성
gcloud iam service-accounts keys create ~/.config/gcloud/imagen-mcp-key.json \
  --iam-account=imagen-mcp@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 4. 환경 변수 설정

```bash
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/imagen-mcp-key.json"
```

## 🔧 Claude Desktop 설정

`claude_desktop_config.json` 파일을 수정하여 MCP 서버를 등록하세요:

```json
{
  "mcpServers": {
    "vertex-ai-imagen": {
      "command": "python",
      "args": [
        "/path/to/vertex-ai-imagen-mcp/mcp_server.py"
      ],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-project-id",
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your/service-account-key.json"
      }
    }
  }
}
```

### Claude Desktop 설정 파일 위치

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## 🚀 사용법

### Claude Desktop에서 사용

Claude Desktop을 재시작한 후, 다음과 같이 이미지를 생성할 수 있습니다:

```
Claude에게: "아름다운 일몰 풍경 이미지를 생성해줘"
```

### 고급 옵션 사용

```
Claude에게: "고양이가 우주를 여행하는 이미지를 16:9 비율로 2개 생성해줘. 
모델은 imagen-3.0-fast-generate-001을 사용하고, 
네거티브 프롬프트로 'blurry, low quality'를 추가해줘"
```

### 이미지 저장 경로 지정

```
Claude에게: "아름다운 풍경 이미지를 생성하고 /Users/username/Pictures/AI_Images 폴더에 
'landscape'라는 이름으로 저장해줘"
```

### 대화형 모드 (MCP 없이)

```bash
python mcp_server.py
```

## 🎯 사용 가능한 도구

### `generate_image`
텍스트 프롬프트로부터 이미지 생성

**필수 매개변수:**
- `prompt` (string): 이미지 생성 프롬프트

**선택적 매개변수:**
- `negative_prompt` (string): 피하고 싶은 내용
- `count` (integer, 1-4): 생성할 이미지 수
- `aspect_ratio` (string): 가로세로 비율 ("1:1", "16:9", "9:16", "4:3", "3:4")
- `model` (string): 사용할 모델
- `seed` (integer): 재현 가능한 결과를 위한 시드
- `safety_setting` (string): 안전 필터 수준
- `save_path` (string): 이미지를 저장할 디렉토리 경로 (지정하지 않으면 Claude에만 표시)
- `filename_prefix` (string): 저장할 파일명 접두사 (기본값: "generated_image")

### `list_models`
사용 가능한 Imagen 모델 목록 조회

## 🤖 지원 모델

| 모델명 | 속도 | 품질 | 용도 |
|--------|------|------|------|
| `imagegeneration@006` | 🟡 보통 | 🔵 우수 | 일반적인 용도 |
| `imagen-3.0-generate-001` | 🟡 보통 | 🟣 최고 | 고품질 작업 |
| `imagen-3.0-generate-002` | 🟡 보통 | 🟣 최고 | 최신 고품질 |
| `imagen-3.0-fast-generate-001` | ⚡ 빠름 | 🟢 양호 | 빠른 프로토타이핑 |

## 🔍 트러블슈팅

### 일반적인 문제들

#### 1. 인증 오류
```
❌ 인증 실패: could not find default credentials
```

**해결방법:**
- `GOOGLE_APPLICATION_CREDENTIALS` 환경변수가 올바르게 설정되었는지 확인
- 서비스 계정 키 파일이 존재하고 읽기 가능한지 확인

#### 2. 권한 오류
```
❌ 403 Forbidden: The caller does not have permission
```

**해결방법:**
- 서비스 계정에 `roles/aiplatform.user` 역할이 부여되었는지 확인
- Vertex AI API가 활성화되었는지 확인

#### 3. 프로젝트 ID 오류
```
❌ Project ID가 설정되지 않았습니다
```

**해결방법:**
- `GOOGLE_CLOUD_PROJECT` 환경변수 설정
- Claude Desktop 설정에서 프로젝트 ID 확인

## 📁 프로젝트 구조

```
vertex-ai-imagen-mcp/
├── mcp_server.py              # 메인 MCP 서버
├── requirements.txt           # Python 의존성
├── .gitignore                # Git 무시 파일
├── README.md                 # 이 파일
├── LICENSE                   # MIT 라이선스
├── claude_desktop_config.json # Claude Desktop 설정 예시
└── examples/                 # 사용 예제
    └── basic_usage.py        # 기본 사용법 예제
```

## 🤝 기여하기

1. 저장소를 포크합니다
2. 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🔗 관련 링크

- [vertex-ai-imagen 패키지](https://github.com/realcoding2003/vertex-ai-imagen) - 핵심 AI 이미지 생성 라이브러리
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai) - 공식 Vertex AI 문서
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 공식 사이트
- [Claude Desktop](https://claude.ai/desktop) - Claude Desktop 애플리케이션

## ❓ 질문 및 지원

문제가 발생하거나 질문이 있으시면 [GitHub Issues](https://github.com/your-username/vertex-ai-imagen-mcp/issues)에 등록해 주세요.

---

**Made with ❤️ by [Kevin Park](https://github.com/your-username)**
