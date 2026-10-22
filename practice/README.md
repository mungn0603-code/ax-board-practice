# 4주차(10/17) 데이터 수집 실습

작성자: 문규남. 작성자의 아이디어를 Claude로 템플릿화해 초안을 잡고, 직접 검토하며 구체화했다.

| 실습 | 폴더 | 질문 | 결과 |
|---|---|---|---|
| A 공개 CSV | start/01_csv | 2007년 Dream 섬의 종별 관측은 몇 건인가 | 46건(Adelie 20, Chinstrap 26). 2008년은 34건(16, 18) |
| B 웹 표 | start/02_html | Bruins는 1990~1992년 중 언제 가장 많이 이겼나 | 1992년 51승(1990 44승, 1991 36승). 3페이지 75행, 팀 26개 |
| C Atom 목록 | start/03_feed | 받은 목록의 서로 다른 사건은 몇 개인가 | 44개. 두 번 읽은 처리 기록 88행, 사건 44행 |
| 판단 기록 | decision_record.md | 도서관 A·B 중 무엇을 먼저 시험할까 | 요청 기록(A 17건, B 2건)으로 A. 처음 기록 칸은 본인 작성 |

## 다시 실행
```bash
cd start/01_csv
python3 collect_csv.py --out runs/a03_subset --stage select --columns species,island,year,body_mass_g --year 2007 --island Dream
```
- 실습 A는 원문을 직접 받는다. runs/ 결과는 저장소에 올리지 않았다.
- 실습 B·C는 작업 환경 네트워크가 사이트를 막아 본인 브라우저로 받았다. relay/에 원문 해시·바이트·획득시각과 행 값을 남겼다.
- 실습 B 1페이지 원문 HTML(50KB)은 올리지 않았다. 다시 실행하려면 브라우저로 받아 relay/hockey_page_1.html에 두면 해시를 대조한다.
