# 수집 계획 — 실습 B

- 질문: Boston Bruins는 1990·1991·1992년 중 어느 시즌에 가장 많이 이겼는가?
- 한 행: 한 팀의 한 시즌 (record_id = team|year)
- 범위: Hockey Teams 표 1~3페이지, 순서대로 요청, 1.25초 이상 간격 (브라우저에서 1.3초 간격으로 받음)
- robots.txt: /lessons/, /faq/만 Disallow → /pages/forms/ 수집 허용
- 출처: https://www.scrapethissite.com/pages/forms/?page_num=1~3
- 변경(B7): 1페이지 · goals_for(GF, 득점) 추가
