# AX 아이디어 보드

업무별 AI 활용 아이디어를 카드로 모으는 웹앱입니다. (2026 천안형 글로벌 인재육성사업 AX 액션러닝 실습)

## 실행 방법

```bash
npm install
npm run dev -- --port 3099
```

브라우저에서 `http://localhost:3099` 를 엽니다.

## 주요 기능

- 제목 · 대상 업무 · AI 아이디어를 입력해 카드 추가
- 카드 목록 표시와 삭제
- 새로고침해도 유지 (localStorage)

## 폴더 구조

```
index.html      앱이 붙는 HTML
src/main.jsx    React 시작점
src/App.jsx     화면과 상태
src/index.css   스타일
```

## 작업 방식

작성자의 아이디어를 Claude로 템플릿화해 초안을 잡고, 직접 검토하며 구체화했다. 작업 기록은 `docs/log.md`, 판단 근거는 `docs/decisions.md`에 남긴다.

## 남은 할 일

- 카드 태그와 태그 필터
- 삭제 전 확인창
