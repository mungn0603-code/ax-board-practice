"""실습 A — Palmer Penguins 공개 CSV 수집기 (Python 표준 라이브러리만 사용)

단계
  fetch   : 원문을 raw/penguins.csv 에 그대로 저장 + 출처 기록
  inspect : 헤더·행 수·열별 빈값/NA 수 계산, 첫 3행을 sample.csv 로
  select  : --columns/--year/--island 범위만 selected.csv 로, summary.md 작성

원칙: 기존 --out 폴더는 거절, 실패하면 중단, 가짜 자료나 자동 사본 전환 없음.
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import sys
import urllib.request
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
EXPECTED_HEADER = ["species", "island", "bill_length_mm", "bill_depth_mm",
                   "flipper_length_mm", "body_mass_g", "sex", "year"]
USER_AGENT = "cheonan-ax-practice/1.0 (education)"


def fail(msg):
    print(f"[중단] {msg}", file=sys.stderr)
    sys.exit(1)


def prepare_out(out):
    out = Path(out)
    if out.exists():
        fail(f"{out} 폴더가 이미 있습니다. 기존 결과를 보호하기 위해 새 이름을 쓰세요.")
    (out / "raw").mkdir(parents=True)
    return out


def fetch(out):
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
    except Exception as exc:  # 접근 실패 시 우회하지 않고 멈춤
        fail(f"다운로드 실패: {exc}")
    collected_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    raw_path = out / "raw" / "penguins.csv"
    raw_path.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    with open(out / "collection_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_url", "collected_at_utc", "source_kind", "bytes", "sha256", "saved_as"])
        w.writerow([SOURCE_URL, collected_at, "actual", len(data), sha, "raw/penguins.csv"])
    (out / "collection_info.md").write_text(
        "# 수집 기록\n\n"
        f"- 출처: Palmer Penguins 공식 저장소 단순화 자료 penguins.csv\n"
        f"- 주소: {SOURCE_URL}\n"
        f"- 이용 조건: CC0 (공식 소개 https://allisonhorst.github.io/palmerpenguins/)\n"
        f"- 획득시각(UTC): {collected_at}\n"
        f"- source_kind: actual (이번에 웹에서 직접 받음)\n"
        f"- 바이트: {len(data)}\n- SHA-256: {sha}\n"
        "- 관측 기간은 2007~2009년이며, 위 획득시각은 다운로드 시각입니다.\n",
        encoding="utf-8")
    print(f"저장: {raw_path} ({len(data)} bytes, sha256 {sha[:12]}…)")
    return data, sha


def read_rows(data):
    reader = csv.reader(io.StringIO(data.decode("utf-8")))
    header = next(reader)
    if header != EXPECTED_HEADER:
        fail(f"헤더가 예상과 다릅니다: {header} — 원문을 확인하세요.")
    rows = []
    for line_no, row in enumerate(reader, start=2):  # 원문 줄번호(헤더=1)
        if len(row) != len(header):
            fail(f"원문 {line_no}번째 줄의 칸 수가 {len(row)}개입니다 — 원문을 확인하세요.")
        rows.append((line_no, dict(zip(header, row))))
    return header, rows


def inspect(out, data):
    header, rows = read_rows(data)
    missing = {c: sum(1 for _, r in rows if r[c] in ("", "NA")) for c in header}
    with open(out / "sample.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_row_number"] + header)
        for line_no, r in rows[:3]:
            w.writerow([line_no] + [r[c] for c in header])
    lines = [f"- 헤더: {', '.join(header)}", f"- 행 수(헤더 제외): {len(rows)}", f"- 열 수: {len(header)}",
             "- 열별 빈값/NA 수:"] + [f"  - {c}: {n}" for c, n in missing.items()]
    (out / "inspect.md").write_text("# inspect 결과\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def select(out, data, sha, columns, year, island):
    header, rows = read_rows(data)
    cols = [c.strip() for c in columns.split(",")]
    unknown = [c for c in cols if c not in header]
    if unknown:
        fail(f"없는 열: {unknown}")
    years = {r["year"] for _, r in rows}
    islands = {r["island"] for _, r in rows}
    if year and year not in years:
        fail(f"없는 연도: {year} (있는 연도: {sorted(years)})")
    if island and island not in islands:
        fail(f"없는 섬: {island} (있는 섬: {sorted(islands)})")
    picked = [(n, r) for n, r in rows
              if (not year or r["year"] == year) and (not island or r["island"] == island)]
    with open(out / "selected.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_record_id", "source_row_number"] + cols)
        for n, r in picked:
            w.writerow([f"{sha[:12]}:{n}", n] + [r[c] for c in cols])  # NA 는 그대로 유지
    miss = {c: sum(1 for _, r in picked if r[c] in ("", "NA")) for c in cols}
    (out / "summary.md").write_text(
        "# select 요약\n\n"
        f"- 원문 행 수: {len(rows)}\n- 선택 행 수: {len(picked)}\n"
        f"- 필터: year={year or '전체'}, island={island or '전체'}\n- 선택 열: {', '.join(cols)}\n"
        "- 선택 열 누락(NA/빈값) 수:\n" + "".join(f"  - {c}: {n}\n" for c, n in miss.items()) +
        f"- 원문 SHA-256: {sha}\n", encoding="utf-8")
    print(f"선택 {len(picked)}행 / 원문 {len(rows)}행 → {out/'selected.csv'}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--stage", choices=["fetch", "inspect", "select"], required=True)
    p.add_argument("--columns", default="species,island,year,body_mass_g")
    p.add_argument("--year")
    p.add_argument("--island")
    a = p.parse_args()
    out = prepare_out(a.out)
    data, sha = fetch(out)  # 모든 단계는 원본을 새 --out 에 먼저 보존
    if a.stage == "inspect":
        inspect(out, data)
    elif a.stage == "select":
        select(out, data, sha, a.columns, a.year, a.island)


if __name__ == "__main__":
    main()
