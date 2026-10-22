"""실습 B — Hockey Teams 웹 표 수집기 (표준 라이브러리)

작업 환경 네트워크가 scrapethissite.com을 막아, 본인 브라우저로 받은 원문을 relay/ 에서 읽는다.
  - 1페이지: 원문 HTML 전체(relay/hockey_page_1.html), 브라우저 해시와 일치 확인
  - 2·3페이지: 브라우저에서 tr.team 행 값만 추출(relay/rows_pN.tsv), 원문 해시·바이트는 relay_log.csv
단계: sample(1페이지 첫 3행) / collect(--pages, --columns)
"""
import argparse
import csv
import hashlib
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
RELAY = HERE / "relay"
ROBOTS = "User-agent: *\nDisallow: /lessons/\nDisallow: /faq/"  # 2026-10-22 브라우저로 확인
TARGET_PATH = "/pages/forms/"
FIELD_MAP = {"team": "name", "year": "year", "wins": "wins", "losses": "losses",
             "ot_losses": "ot-losses", "pct": "pct", "goals_for": "gf",
             "goals_against": "ga", "diff": "diff"}


def fail(msg):
    print(f"[중단] {msg}", file=sys.stderr)
    sys.exit(1)


def robots_allows(path):
    return not any(path.startswith(line.split(":", 1)[1].strip())
                   for line in ROBOTS.splitlines() if line.startswith("Disallow:"))


class TeamTable(HTMLParser):
    """tr.team 안의 td(class)만 읽는다. 페이지 전체 글을 공백으로 자르지 않는다."""

    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell, self.buf = [], None, None, []

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "") or ""
        if tag == "tr" and "team" in cls.split():
            self.row = {}
        elif tag == "td" and self.row is not None:
            self.cell, self.buf = cls.split()[0], []

    def handle_data(self, data):
        if self.cell:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.cell:
            self.row[self.cell] = "".join(self.buf).strip()
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def load_log():
    with open(RELAY / "relay_log.csv", encoding="utf-8") as f:
        return {int(r["page"]): r for r in csv.DictReader(f)}


def page_rows(page, log):
    if page not in log:
        fail(f"{page}페이지 원문 기록이 없습니다. 받지 않은 페이지를 만들어 채우지 않습니다.")
    if page == 1:
        raw = (RELAY / "hockey_page_1.html").read_bytes()
        if hashlib.sha256(raw).hexdigest() != log[1]["sha256"]:
            fail("1페이지 원문 해시가 브라우저 기록과 다릅니다.")
        parser = TeamTable()
        parser.feed(raw.decode("utf-8"))
        return parser.rows
    with open(RELAY / f"rows_p{page}.tsv", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f, delimiter="\t")]


def prepare_out(out):
    out = Path(out)
    if out.exists():
        fail(f"{out} 폴더가 이미 있습니다. 새 이름을 쓰세요.")
    out.mkdir(parents=True)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--pages", default="1")
    p.add_argument("--stage", choices=["sample", "collect"], required=True)
    p.add_argument("--columns", default="team,year,wins,losses,ot_losses")
    a = p.parse_args()
    if not robots_allows(TARGET_PATH):
        fail("robots.txt가 표 경로를 막습니다.")
    pages = [int(x) for x in a.pages.split(",")]
    if any(x not in (1, 2, 3) for x in pages):
        fail("이번 범위는 1~3페이지뿐입니다.")
    cols = [c.strip() for c in a.columns.split(",")]
    if "team" not in cols or "year" not in cols:
        fail("team과 year는 반드시 남깁니다.")
    if any(c not in FIELD_MAP for c in cols):
        fail(f"없는 항목: {[c for c in cols if c not in FIELD_MAP]}")
    log = load_log()
    out = prepare_out(a.out)

    if a.stage == "sample":
        rows = page_rows(1, log)[:3]
        with open(out / "sample.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["source_page", "row_on_page", "team", "year", "wins", "losses", "ot_losses"])
            for i, r in enumerate(rows, 1):
                w.writerow([1, i] + [r[FIELD_MAP[c]] for c in ["team", "year", "wins", "losses", "ot_losses"]])
        print(open(out / "sample.csv", encoding="utf-8").read())
        return

    result, per_page, seen = [], {}, {}
    for pg in pages:
        rows = page_rows(pg, log)
        per_page[pg] = len(rows)
        for i, r in enumerate(rows, 1):
            key = f"{r['name']}|{r['year']}"
            if key in seen:
                fail(f"팀+연도 키 중복: {key} ({seen[key]} / {pg}p {i}행)")
            seen[key] = f"{pg}p {i}행"
            result.append([key, pg, i] + [r[FIELD_MAP[c]] for c in cols])
    with open(out / "hockey.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_id", "source_page", "row_on_page"] + cols)
        w.writerows(result)
    teams = {row[0].split("|")[0] for row in result}
    blanks = {c: sum(1 for row in result if row[3 + j] == "") for j, c in enumerate(cols)}
    lines = [f"- 페이지: {pages}, 페이지별 행 수: {per_page} (합 {sum(per_page.values())})",
             f"- 결과 행 수: {len(result)}", f"- 서로 다른 팀 이름 수: {len(teams)}",
             f"- 팀시즌 키 수: {len(seen)}", "- 빈 칸 수: " + ", ".join(f"{c} {n}" for c, n in blanks.items()),
             "- 출처: relay/relay_log.csv (source_kind=actual-browser)"]
    (out / "summary.md").write_text("# collect 요약\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
