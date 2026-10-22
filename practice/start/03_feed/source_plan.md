# 수집 계획 — 실습 C

- 질문: 받은 목록의 서로 다른 사건은 몇 개인가?
- 대상: USGS · M2.5+ · Past Day Atom 목록 (https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.atom)
- 한 행: 사건 entry 하나
- 7열: entry_id, title, link, updated_at(원문 갱신), categories, collected_at(원문 획득), source_kind
- 원문 published: 미제공. 발생시각은 summary의 Time에 있으나 이번 7열에서는 추출하지 않는다.
