# 🎨 Vertex AI Imagen MCP Server

**Languages**: [🇺🇸 English](README.md)

---

**Google Cloud Vertex AI Imagen을 위한 Model Context Protocol (MCP) 서버**

이 MCP 서버는 [vertex-ai-imagen](https://github.com/realcoding2003/vertex-ai-imagen) 패키지를 활용하여 Claude Desktop에서 직접 고품질 AI 이미지를 생성할 수 있게 해줍니다.

## ✨ 주요 기능

- 🎯 **간단한 설정**: `vertex-ai-imagen` 패키지 기반의 간소화된 구조
- 🚀 **Claude Desktop 통합**: MCP를 통한 원활한 이미지 생성
- 🎨 **다양한 모델 지원**: Imagen 3.0, imagegeneration@006 등
- 🔧 **유연한 옵션**: 가로세로 비율, 이미지 수, 안전 설정 등
- 🔒 **안전한 인증**: Google Cloud 서비스 계정 기반

## 🚀 빠른 시작 (5분 설정)

### 1️⃣ 프로젝트 설치

```bash
git clone https://github.com/your-username/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp
pip install -r requirements.txt
```

### 2️⃣ Google Cloud 인증 설정

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성/선택
2. [Vertex AI API 활성화](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com)
3. 서비스 계정 생성 및 키 파일 다운로드 (아래 상세 가이드 참조)

### 3️⃣ Claude Desktop 설정

1. **설정 파일 위치**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **설정 파일 내용 추가**:

```json
{
  "mcpServers": {
    "vertex-ai-imagen": {
      "command": "python",
      "args": ["/절대경로/to/vertex-ai-imagen-mcp/mcp_server.py"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-actual-project-id",
        "GOOGLE_APPLICATION_CREDENTIALS": "/절대경로/to/your-key-file.json"
      }
    }
  }
}
```

3. **Claude Desktop 재시작**

### 4️⃣ 첫 이미지 생성 테스트

Claude Desktop 재시작 후: *"아름다운 일몰 풍경 이미지를 생성해줘"*

---

## 🛠️ 상세 설치 및 설정

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

#### 3.1 Google Cloud Project 및 API 활성화

1. **Google Cloud Console 접속**
   - [Google Cloud Console](https://console.cloud.google.com/)에 로그인합니다
   - 기존 프로젝트를 선택하거나 새 프로젝트를 생성합니다

2. **Vertex AI API 활성화**
   - 좌측 메뉴에서 "API 및 서비스" → "라이브러리"로 이동
   - "Vertex AI API"를 검색하고 클릭
   - "사용 설정" 버튼을 클릭하여 API를 활성화합니다

   또는 [직접 링크](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com)에서 활성화

#### 3.2 서비스 계정 생성 및 키 파일 다운로드

1. **서비스 계정 생성**
   - Google Cloud Console에서 "IAM 및 관리자" → "서비스 계정"으로 이동
   - "서비스 계정 만들기" 클릭
   - 서비스 계정 세부정보 입력:
     - **서비스 계정 이름**: `imagen-mcp` (또는 원하는 이름)
     - **서비스 계정 ID**: 자동 생성됨
     - **설명**: `Imagen MCP Server용 서비스 계정`
   - "만들고 계속하기" 클릭

2. **권한 부여**
   - "이 서비스 계정에 프로젝트 액세스 권한 부여" 섹션에서
   - "역할 선택" 드롭다운에서 `Vertex AI 사용자` 역할 선택
   - "계속" 클릭

3. **키 파일 생성 및 다운로드**
   - "사용자에게 이 서비스 계정 액세스 권한 부여" 섹션은 건너뛰고 "완료" 클릭
   - 생성된 서비스 계정 목록에서 방금 만든 계정의 이메일 주소 클릭
   - "키" 탭으로 이동
   - "키 추가" → "새 키 만들기" 클릭
   - 키 유형: **JSON** 선택
   - "만들기" 클릭하면 JSON 키 파일이 자동으로 다운로드됩니다

4. **키 파일 안전한 위치에 저장**

   ```bash
   # 예시: macOS/Linux
   mkdir -p ~/.config/gcloud
   mv ~/Downloads/your-project-id-xxxxxx.json ~/.config/gcloud/imagen-mcp-key.json
   
   # 예시: Windows
   mkdir %USERPROFILE%\.config\gcloud
   move %USERPROFILE%\Downloads\your-project-id-xxxxxx.json %USERPROFILE%\.config\gcloud\imagen-mcp-key.json
   ```

### 4. 환경 변수 설정

다운로드받은 키 파일과 프로젝트 정보를 환경 변수로 설정합니다:

**macOS/Linux:**

```bash
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/imagen-mcp-key.json"
```

**Windows (PowerShell):**

```powershell
$env:GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
$env:GOOGLE_APPLICATION_CREDENTIALS="$HOME\.config\gcloud\imagen-mcp-key.json"
```

> 💡 **프로젝트 ID 확인 방법**: Google Cloud Console 상단에 표시되는 프로젝트 이름 옆의 ID를 사용하세요.

## 🔧 Claude Desktop 설정

### 설정 파일 위치 확인

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### 설정 파일 편집

`claude_desktop_config.json` 파일을 생성/편집하여 MCP 서버를 등록하세요:

```json
{
  "mcpServers": {
    "vertex-ai-imagen": {
      "command": "python",
      "args": [
        "/절대경로/to/vertex-ai-imagen-mcp/mcp_server.py"
      ],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "your-actual-project-id",
        "GOOGLE_APPLICATION_CREDENTIALS": "/절대경로/to/your-key-file.json"
      }
    }
  }
}
```

> ⚠️ **중요**:
>
> - 모든 경로는 절대 경로로 지정해야 합니다
> - `your-actual-project-id`를 실제 Google Cloud 프로젝트 ID로 교체하세요
> - 키 파일 경로를 실제 다운로드한 JSON 파일 경로로 교체하세요

### 설정 완료 후

1. Claude Desktop을 완전히 종료합니다
2. Claude Desktop을 다시 시작합니다
3. 좌측 하단에 🔧 아이콘이 나타나면 MCP 서버가 성공적으로 연결된 것입니다

## 🚀 사용법

### Claude Desktop에서 사용

Claude Desktop을 재시작한 후, 다음과 같이 이미지를 생성할 수 있습니다:

```text
Claude에게: "아름다운 일몰 풍경 이미지를 생성해줘"
```

### 고급 옵션 사용

```text
Claude에게: "고양이가 우주를 여행하는 이미지를 16:9 비율로 2개 생성해줘. 
모델은 imagen-3.0-fast-generate-001을 사용하고, 
네거티브 프롬프트로 'blurry, low quality'를 추가해줘"
```

### 이미지 저장 경로 지정

```text
Claude에게: "아름다운 풍경 이미지를 생성하고 /Users/username/Pictures/AI_Images 폴더에 
'landscape.png'라는 이름으로 저장해줘"
```

### 정확한 파일명으로 저장

```text
Claude에게: "웹사이트 히어로 이미지를 생성해줘. 16:9 비율로 만들고 
imagen-3.0-generate-001 모델을 사용해서 
/Users/kevinpark/Documents/projects/realcoding.github.io/assets/images/posts/ai-tutorial/ 
경로에 'hero.png'로 저장해줘"
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
- `aspect_ratio` (string): 가로세로 비율 ("1:1", "3:4", "4:3", "16:9", "9:16")
- `model` (string): 사용할 모델 (기본값: "imagegeneration@006")
- `seed` (integer): 재현 가능한 결과를 위한 시드
- `safety_setting` (string): 안전 필터 수준 (기본값: "block_some")
- `save_path` (string): 이미지를 저장할 디렉토리 경로 (지정하지 않으면 Claude에만 표시)
- `filename` (string): 정확한 파일명 (확장자 포함 가능). **이 옵션을 사용하면 타임스탬프 없이 지정된 이름으로 저장됩니다.**
- `filename_prefix` (string): 파일명 접두사 (기본값: "generated_image"). **filename이 지정되지 않았을 때만 사용됩니다.**

> 💡 **파일명 동작 방식**:
>
> - `filename` 지정 시: 정확한 파일명으로 저장 (여러 이미지 생성 시 _1,_2 등 추가)
> - `filename` 미지정 시: `{filename_prefix}_{timestamp}_{번호}.png` 형식으로 저장

### `list_models`

사용 가능한 Imagen 모델 목록 조회

## 🤖 지원 모델

| 모델명 | 속도 | 품질 | 용도 |
|--------|------|------|------|
| `imagegeneration@006` | 🟡 보통 | 🟣 최고 | 일반적인 용도 |
| `imagen-3.0-generate-001` | 🟡 보통 | 🟣 최고 | 고품질 작업 |
| `imagen-3.0-generate-002` | 🟡 보통 | 🟣 최고 | 최신 고품질 |
| `imagen-3.0-fast-generate-001` | ⚡ 빠름 | 🟢 양호 | 빠른 프로토타이핑 |

## 🔍 트러블슈팅

### 일반적인 문제들

#### 1. 인증 오류

```bash
❌ 인증 실패: could not find default credentials
```

**해결방법:**

- `GOOGLE_APPLICATION_CREDENTIALS` 환경변수가 올바르게 설정되었는지 확인
- 서비스 계정 키 파일이 존재하고 읽기 가능한지 확인

#### 2. 권한 오류

```bash
❌ 403 Forbidden: The caller does not have permission
```

**해결방법:**

- 서비스 계정에 `roles/aiplatform.user` 역할이 부여되었는지 확인
- Vertex AI API가 활성화되었는지 확인

#### 3. 프로젝트 ID 오류

```bash
❌ Project ID가 설정되지 않았습니다
```

**해결방법:**

- `GOOGLE_CLOUD_PROJECT` 환경변수 설정
- Claude Desktop 설정에서 프로젝트 ID 확인

## 📁 프로젝트 구조

```bash
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

문제가 발생하거나 질문이 있으시면 [GitHub Issues](https://github.com/realcoding2003/vertex-ai-imagen-mcp/issues)에 등록해 주세요.

---

**Made with ❤️ by [Kevin Park](https://github.com/realcoding2003)**
