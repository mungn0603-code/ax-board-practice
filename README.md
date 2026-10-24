# my-intro — 한 줄 자기소개 다듬기

자기소개 한 줄을 넣으면 AI가 **면접용 · SNS용 · 발표용** 세 가지로 다듬어 준다.

## 주요 기능
- 자기소개 한 줄 입력 → '다듬기' 버튼
- 결과 카드 3장: 면접용 · SNS용 · 발표용
- 답한 모델 이름 표시 (OpenRouter `openrouter/free`가 고른 무료 모델)

## 구조
| 구분 | 파일 | 역할 |
| --- | --- | --- |
| 화면 | `app/page.tsx` | 입력칸 · 버튼 · 결과 카드 |
| 서버 | `app/api/polish/route.ts` | OpenRouter 호출 (키는 `.env`) |

Next.js (App Router) + TypeScript.

## 필요한 키
| 이름 | 설명 |
| --- | --- |
| `OPENROUTER_API_KEY` | OpenRouter API 키 (`sk-or-v1-...`) — openrouter.ai/settings/keys |

`.env.sample`을 복사해 `.env`를 만들고 값을 넣는다. `.env`는 커밋하지 않는다.

## 실행 방법
```bash
npm install
cp .env.sample .env   # OPENROUTER_API_KEY= 뒤에 키 붙여넣기
npm run dev           # 환경변수 PORT 사용 (없으면 3000)
```
브라우저에서 `http://localhost:$PORT` 를 연다.
