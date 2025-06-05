# 설정 가이드

이 문서는 Vertex AI Imagen MCP Server의 상세한 설정 방법을 안내합니다.

## 사전 요구사항

### 1. Python 환경
```bash
python --version  # Python 3.8 이상 필요
```

### 2. Google Cloud 계정
- 유효한 Google 계정
- 결제 계정 연결 (무료 크레딧 사용 가능)

## Google Cloud 설정

### 1. 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. 프로젝트 ID 기록 (예: `my-imagen-project-123456`)

### 2. API 활성화

필수 API들을 활성화해야 합니다:

```bash
# gcloud CLI 사용 (추천)
gcloud services enable aiplatform.googleapis.com
gcloud services enable compute.googleapis.com

# 또는 Console에서 직접 활성화:
# - Vertex AI API
# - Compute Engine API (기본적으로 활성화됨)
```

### 3. 결제 설정

1. **결제 계정 연결**
   - Google Cloud Console > 결제
   - 기존 결제 계정 선택 또는 새로 생성
   - 프로젝트에 결제 계정 연결

2. **예산 설정 (권장)**
   ```bash
   # 예산 알림 설정으로 비용 관리
   # Console > 결제 > 예산 및 알림
   ```

### 4. 서비스 계정 생성

#### Console 사용

1. **IAM 및 관리 > 서비스 계정**
2. **서비스 계정 만들기**
3. 서비스 계정 세부정보:
   ```
   이름: imagen-api-service
   설명: Vertex AI Imagen API 접근용 서비스 계정
   ```
4. **권한 부여**:
   - `Vertex AI User` 역할 추가
   - (선택사항) `Storage Object Viewer` (Cloud Storage 사용시)

5. **키 생성**:
   - JSON 형식으로 키 파일 다운로드
   - 안전한 위치에 저장

#### gcloud CLI 사용

```bash
# 서비스 계정 생성
gcloud iam service-accounts create imagen-api-service \
    --description="Vertex AI Imagen API service account" \
    --display-name="Imagen API Service"

# 권한 부여
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:imagen-api-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# 키 파일 생성
gcloud iam service-accounts keys create ~/imagen-service-key.json \
    --iam-account=imagen-api-service@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## 로컬 환경 설정

### 1. 프로젝트 클론

```bash
git clone https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp.git
cd vertex-ai-imagen-mcp
```

### 2. 의존성 설치

```bash
# 기본 의존성
pip install -r requirements.txt

# MCP 통합용 (선택사항)
pip install mcp
```

### 3. 환경 변수 설정

#### 방법 1: .env 파일 (권장)

```bash
# .env 파일 생성
cat > .env << EOF
GOOGLE_CLOUD_PROJECT=your-project-id-here
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
EOF

# .env 파일 로드
source .env
```

#### 방법 2: 직접 export

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export VERTEX_AI_LOCATION="us-central1"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

#### 방법 3: ~/.bashrc 또는 ~/.zshrc에 추가

```bash
echo 'export GOOGLE_CLOUD_PROJECT="your-project-id"' >> ~/.bashrc
echo 'export VERTEX_AI_LOCATION="us-central1"' >> ~/.bashrc
echo 'export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"' >> ~/.bashrc
source ~/.bashrc
```

### 4. 설정 검증

```bash
# 환경 변수 확인
echo $GOOGLE_CLOUD_PROJECT
echo $GOOGLE_APPLICATION_CREDENTIALS

# 서비스 계정 키 파일 확인
ls -la $GOOGLE_APPLICATION_CREDENTIALS

# 인증 테스트
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
gcloud projects describe $GOOGLE_CLOUD_PROJECT
```

## 지역(Region) 설정

### 지원되는 지역

- `us-central1` (기본값, 권장)
- `us-east1`
- `us-west1`
- `europe-west2`
- `europe-west4`
- `asia-northeast1`
- `asia-southeast1`

### 지역 선택 가이드

```bash
# 지연 시간 고려
# 사용자와 가까운 지역 선택

# 미국: us-central1
# 유럽: europe-west2
# 아시아: asia-northeast1 (일본)
```

## 권한 설정

### 최소 권한 원칙

서비스 계정에 필요한 최소한의 권한만 부여:

```bash
# 필수 권한
- roles/aiplatform.user

# 선택적 권한 (필요시에만)
- roles/storage.objectViewer  # Cloud Storage 사용시
- roles/logging.logWriter     # 로깅 강화시
```

### 권한 확인

```bash
# 서비스 계정 권한 확인
gcloud projects get-iam-policy $GOOGLE_CLOUD_PROJECT \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:imagen-api-service@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com"
```

## 보안 설정

### 1. 서비스 계정 키 보안

```bash
# 키 파일 권한 설정
chmod 600 /path/to/service-account-key.json

# 소유자만 읽기 가능하도록 설정
```

### 2. 키 로테이션

```bash
# 정기적인 키 교체 (권장: 90일마다)
gcloud iam service-accounts keys create new-key.json \
    --iam-account=imagen-api-service@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com

# 기존 키 삭제
gcloud iam service-accounts keys delete OLD_KEY_ID \
    --iam-account=imagen-api-service@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
```

### 3. 네트워크 보안

```bash
# VPC 방화벽 규칙 (필요시)
# 특정 IP에서만 접근 허용
```

## 테스트

### 1. 기본 테스트

```bash
# 독립 실행 모드 테스트
python src/imagen_mcp_server.py

# 기본 예시 실행
python examples/basic_usage.py
```

### 2. 연결 테스트

```bash
# API 연결 확인
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://us-central1-aiplatform.googleapis.com/v1/projects/$GOOGLE_CLOUD_PROJECT/locations/us-central1/endpoints"
```

## 문제 해결

### 일반적인 문제들

1. **인증 실패**
   ```bash
   # 서비스 계정 키 경로 확인
   # 권한 재확인
   # 키 파일 형식 검증
   ```

2. **API 비활성화**
   ```bash
   # Vertex AI API 활성화 확인
   gcloud services list --enabled | grep aiplatform
   ```

3. **권한 부족**
   ```bash
   # Vertex AI User 역할 확인
   # 프로젝트 ID 정확성 확인
   ```

### 로그 확인

```bash
# 상세 로그 활성화
export LOG_LEVEL=DEBUG
python src/imagen_mcp_server.py
```

## 다음 단계

설정이 완료되면:

1. [API 문서](api.md)에서 사용법 확인
2. [예시 코드](../examples/) 실행
3. Claude Desktop 통합 설정

## 지원

문제가 발생하면:
- [GitHub Issues](https://github.com/YOUR_USERNAME/vertex-ai-imagen-mcp/issues)
- [문제 해결 가이드](troubleshooting.md)
