# my-intro — 한 줄 자기소개 다듬기

자기소개 한 줄을 넣으면 AI가 **면접용 · SNS용 · 발표용** 세 가지로 다듬어 주는 웹앱.

## 구조
- Next.js (App Router) + TypeScript, 한 프로젝트 안에서 화면과 서버를 나눈다.
- 화면(프론트엔드): `app/page.tsx` — 입력칸 · 버튼 · 결과 카드 3장 · 답한 모델 이름
- 서버(백엔드): `app/api/polish/route.ts` — OpenRouter 호출. 키는 서버에서만 읽는다.
- API: OpenRouter, `model: "openrouter/free"` (응답의 `model` 필드로 실제 답한 무료 모델 이름을 화면에 표시)

## 작업 규칙
- 답변과 화면 문구는 한국어로 쓴다.
- 작은 단계로 나눠 작업하고, 단계마다 화면에서 동작을 확인한 뒤 다음으로 넘어간다.
- 새 기능은 가짜(mock) 결과로 화면을 먼저 확인하고, 그다음 실제 API를 붙인다.

## GitHub 규칙
- 기능 하나가 동작하는 것을 확인하면 커밋하고 푸시한다.
- 커밋 메시지는 한국어로, 무엇을 · 왜 했는지 쓴다. (예: `OpenRouter 연결 — 가짜 결과를 실제 AI 답변으로 바꾸기 위해`)
- 기능을 바꾸거나 추가하면 README.md도 같이 업데이트한다. (주요 기능 · 실행 방법 · 필요한 키 이름)
- 빌드(`npm run build`)가 깨진 상태로는 커밋하지 않는다.

## 키 파일은 커밋 금지
- API 키는 `.env`에만 둔다: `OPENROUTER_API_KEY=...` (키 값은 사용자가 직접 넣는다)
- `.env`, `.env.local` 같은 키 파일은 커밋 · 푸시하지 않는다. (`.env.sample`만 커밋, 값은 비워 둔다)
- 키 값은 코드 · 로그 · 화면(클라이언트 코드)에 쓰지 않는다. 커밋 전 `git status`로 키 파일이 없는지 확인한다.

## 실행
- `npm run dev` — 환경변수 `PORT`를 쓴다 (userNN → 30NN) → `http://localhost:$PORT`
