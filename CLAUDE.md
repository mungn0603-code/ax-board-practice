# AX 아이디어 보드 — 프로젝트 메모

- 기술: Vite + React 18, 저장은 브라우저 localStorage(`ax-board-ideas` 키)
- 개발 서버: `npm run dev -- --port 3099 --strictPort` (수업 서버에서는 배정 포트 30NN)
- 빌드 확인: `npm run build`
- 화면 문구는 한국어
- 주요 파일: `src/App.jsx`(화면·상태), `src/index.css`(스타일)

## Git 규칙

- main 브랜치에 직접 commit · push 하지 않는다
- 작업 전 main을 최신으로 받고 새 브랜치에서 시작한다
- 브랜치 이름: feat/내용, fix/내용, docs/내용
- 커밋 메시지: "feat: 한국어 설명" 형식
- commit 작성자는 작성자 본인이며 Co-Authored-By를 넣지 않는다
- PR 본문에 관련 Issue(Closes #번호)와 확인 방법을 적는다
- 충돌이 나면 임의로 해결하지 말고 양쪽 내용을 설명한 뒤 멈춘다

## 10/10 작업 규칙
- PRD와 wireframe을 먼저 읽는다.
- 기능은 자기 branch에서 수정한다.
- 현재 저장 방식(localStorage)·개수를 유지한다.
- 선택한 작은 변경 하나만 수행한다.
- 수정 후 build와 브라우저 확인 방법을 알려준다.
- AI는 commit까지만 수행한다. push·PR 생성은 작성자가 확인 후 진행한다.
