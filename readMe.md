# MCP AI Core

MCP(Mission Control Protocol) AI Core는 AI 에이전트와 도구들을 연결하는 프레임워크입니다.

## 프로젝트 구조

```
mcp-ai-core/
├── lib/
│   └── mcp_client.py      # MCP 클라이언트 기본 구현
├── src/
│   └── mcp_openai_client/
│       └── mcp_openai_client.py  # OpenAI API를 사용하는 MCP 클라이언트 구현
├── mcp-config.json        # MCP 서버 설정 파일
└── requirements.txt       # 프로젝트 의존성
```

## 주요 컴포넌트

### 1. MCPClient (lib/mcp_client.py)
- MCP 프로토콜의 기본 클라이언트 구현
- 서버 연결 및 통신 관리
- 도구 및 프롬프트 목록 관리
- 비동기 작업 처리

### 2. McpOpenAIClient (src/mcp_openai_client/mcp_openai_client.py)
- OpenAI API를 사용하는 MCP 클라이언트 구현
- GPT 모델과의 통신
- 도구 호출 및 결과 처리
- 대화형 인터페이스 제공

### 3. mcp-config.json
- MCP 서버 설정
- 서버 실행 명령어 및 파라미터
- 작업 디렉토리 설정

## 사용 방법

1. 환경 설정
```bash
# .env 파일 생성
OPENAI_API_KEY=your_api_key_here
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 클라이언트 실행
```bash
python src/mcp_openai_client/mcp_openai_client.py
```

## 주요 기능

- OpenAI API를 통한 자연어 처리
- MCP 프로토콜을 통한 도구 호출
- 비동기 작업 처리
- 대화형 인터페이스
- 도구 및 프롬프트 관리

## 의존성

- openai
- python-dotenv
- mcp (Mission Control Protocol)
- asyncio
- httpx

#### 프로젝트 실행 방법
```cmd
    initialize.bat
```

