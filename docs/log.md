# 작업 로그

작성자: 문규남 · 작성 방식: 작성자의 아이디어를 Claude로 템플릿화해 초안을 잡고, 직접 검토하며 구체화했다.

| 일시(KST) | 작업 | 결과 |
|---|---|---|
| 2026-10-22 | 강의자료 폴더(01 강의자료) 4개 자료를 읽고 아이디어·액션·실습 목록을 1차로 정리했다 | 정리 문서 작성. 2주차 폴더는 비어 있어 제외했다 |
| 2026-10-22 | 1주차 AX 아이디어 보드(Vite + React, localStorage)를 만들었다 | 검증 5개 통과: 추가, 빈값 차단, 새로고침 유지, 삭제, 삭제 후 유지 |
| 2026-10-22 | CLAUDE.md, README.md, .gitignore를 작성하고 로컬 첫 commit을 남겼다 | f79b69b |
| 2026-10-22 | 원격 저장소 생성을 시도했다 | 연결된 토큰 권한 부족으로 실패. 저장소는 직접 만들었다(ax-board-practice, Public으로 생성됨) |
| 2026-10-22 | 4주차 실습 A(Palmer Penguins CSV) 수집기를 만들고 fetch→inspect→select→variant를 실행했다 | 344행·8열, body_mass_g NA 2개, sex NA 11개. 2007 Dream 46행(Adelie 20, Chinstrap 26), 2008 Dream 34행(16, 18). 수업 자료 값과 일치 |
| 2026-10-22 | 실습 B·C 데이터 접근을 확인했다 | 작업 환경의 네트워크 정책이 scrapethissite.com, earthquake.usgs.gov를 막았다 |
| 2026-10-22 | 실습 B 페이지를 브라우저로 받아 gzip+base64로 옮겼다 | 1페이지는 정상(50,456 bytes, 25행). 2·3페이지는 옮기는 과정에서 손상돼 CRC 오류가 났다 |
| 2026-10-22 | 새 저장소에 첫 파일(.gitignore) commit을 시도했다 | 연결된 GitHub 토큰에 이 저장소 접근 권한이 없어 실패했다(Resource not accessible by personal access token) |
| 2026-10-22 | 실습 B 2·3페이지를 다시 받았다. 원문 해시·바이트는 브라우저에서 기록하고 tr.team 행 값만 옮겼다 | 1페이지 원문 해시가 브라우저 기록과 일치했다. 75행, 팀 이름 26개, 팀시즌 키 중복 없음. Bruins 1990·1991·1992 = 44·36·51승 |
| 2026-10-22 | 실습 C USGS Atom 목록을 브라우저로 받아 수집·재처리했다 | entry 44개, observations 88행, entities 44행, 새 요청 0회. published 미제공 |
| 2026-10-22 | 4주차 decision_record 양식을 만들었다 | 처음 기록 칸은 본인이 채우도록 비워 두었다 |
| 2026-10-22 | GitHub MCP 토큰 상태를 점검했다(토큰 값은 출력하지 않음) | 설정 파일의 토큰은 mungn0603-code 소유이고 ax-board-practice에 push 권한이 있다고 판단했다(이후 D14에서 정정). 실행 중인 MCP 프로세스(00:45 시작)가 수정 전 토큰을 써서 쓰기가 실패했다 |
| 2026-10-22 | 로컬에서 충돌을 재현했다. main에서 feat/title-a(AX 보드 A)·feat/title-b(AX 보드 B)를 만들고 A를 먼저 merge한 뒤 B에 main을 합쳤다 | src/App.jsx 54행에 <<<<<<< HEAD / ======= / >>>>>>> main 표시가 생겼다. 재현만 하고 merge --abort로 되돌렸다(태그 demo/conflict-local). GitHub 실습은 본인이 웹에서 해결한다(D6) |
| 2026-10-22 | 앱 재시작 후(20:14) GitHub MCP로 다시 commit을 시도했다 | 새 프로세스도 같은 오류로 실패했다. 저장소가 Public이라 읽기는 어떤 토큰으로도 되므로, 앞선 "push 가능" 결과는 토큰 권한이 아니라 계정 권한이었다 |
| 2026-10-22 | 토큰 저장소 범위 수정 후 GitHub 반영을 시작했다 | .gitignore commit 성공(d761a5b). 이후 모든 commit 작성자는 gyunam(본인)이고 Co-Authored-By는 없다 |
| 2026-10-22 | main에 기본 기능(8012f10)과 태그 필터(22369ad)를 올렸다 | GitHub 파일 해시가 로컬 검증본과 모두 같았다 |
| 2026-10-22 | GitHub Flow: feat/title-change → PR #1 → 리뷰(Comment) → merge | App.jsx +1 −1 |
| 2026-10-22 | Issue #2(카드 삭제 전 확인창) → feat/delete-confirm → PR #3(Closes #2) → 줄 리뷰 → merge | merge와 함께 Issue #2가 자동으로 닫혔다 |
| 2026-10-22 | docs/readme-run → PR #4 | 새 폴더에 clone해 README 명령대로 실행했고 검증 9개가 통과했다 |
| 2026-10-22 | Issue #5(아이디어 개수 표시) → feat/idea-count → PR #6(Closes #5) → merge | 완료 조건 3개 확인, Issue #5 자동 종료 |
| 2026-10-22 | CLAUDE.md Git 규칙 → PR #7 → merge | Co-Authored-By 금지 규칙 포함 |
| 2026-10-22 | 10/10 실습: feat/mungn0603-code-small-change에 PRD 문서 4종·10/10 규칙, 작은 변경 B(7ef3cb7), 기록 commit → PR #8(본문 4줄) | build 성공, 안내 문구·입력값 추가·새로고침 유지 확인 |
| 2026-10-22 | PR #8 리뷰에서 AC-07 결과와 handoff 갱신을 요청하고 같은 PR에 수정 commit(a64013a)을 이었다 | merge(08be748). handoff 브랜치 docs/mungn0603-code-1010-handoff에 handoff.md만 담은 마지막 commit(cbb209b)을 올렸다 |
| 2026-10-22 | 충돌 실습: main에서 feat/title-a·feat/title-b를 만들고 PR #9(A)를 먼저 merge했다 | PR #10(B)은 App.jsx 59행에서 충돌한다. 로컬 시험 merge로 충돌 표시를 확인했다. 해결은 본인이 웹에서 한다(D6) |
| 2026-10-22 | practice/에 10/17 실습 A·B·C를 올렸다(PR #11) | 18개 파일 해시가 로컬과 같았다. 저장소 사본에서 A·C를 다시 실행해 같은 결과를 얻었다 |
| 2026-10-22 | PR #10 충돌을 GitHub 웹 Resolve conflicts로 해결했다 | B(AX 보드 B)를 남기고 merge commit 22f4a0e(부모 2개)를 만들었다. 충돌 표시 0개. 제목 줄 위에 빈 줄 1개가 생겼으나 화면에는 영향이 없다 |
| 2026-10-22 | 해결된 feat/title-b를 main에 시험 merge했다 | 충돌 없이 합쳐지고 build 성공, 브라우저 검증 21개 통과. Merge pull request 버튼은 아직 누르지 않아 PR #10은 열려 있다 |
| 2026-10-22 | PR #10 상태를 다시 확인했다 | 12:09에 merge 없이 닫혔다(closed, merged_at 없음). main 제목은 여전히 AX 보드 A이고, 충돌 해결 commit 22f4a0e는 feat/title-b에만 있다. Close pull request를 Merge 대신 누른 것으로 판단한다 |
| 2026-10-22 | PR #10을 다시 열고 Merge pull request로 머지했다 | merge commit dda2296. main 제목이 AX 보드 B로 바뀌었다. 새 clone에서 build 성공, 브라우저 검증 21개 통과. 전체 commit 30개, 작성자 본인 1명, Co-Authored-By 0건 |
