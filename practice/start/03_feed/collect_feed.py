"""실습 C — USGS M2.5+ Past Day Atom 목록 수집기 (표준 라이브러리)

작업 환경 네트워크가 earthquake.usgs.gov를 막아, 본인 브라우저에서 받은 목록을 relay/ 에서 읽는다.
  relay/relay_info.csv : 원문 주소·바이트·SHA-256·획득시각(collected_at)·목록 갱신시각·published 제공 여부
  relay/entries.tsv    : 브라우저 DOMParser로 읽은 entry 5개 값(id, title, link, updated, category)
단계: sample(첫 3개) / collect(전체, --limit N)
"""
import argparse
import csv
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
RELAY = HERE / "relay"
COLS = ["entry_id", "title", "link", "updated_at", "categories", "collected_at", "source_kind"]


def fail(msg):
    print(f"[중단] {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--stage", choices=["sample", "collect"], required=True)
    p.add_argument("--limit", type=int)
    a = p.parse_args()
    if a.limit is not None and a.limit < 1:
        fail("--limit은 1 이상이어야 합니다.")
    out = Path(a.out)
    if out.exists():
        fail(f"{out} 폴더가 이미 있습니다. 새 이름을 쓰세요.")
    info = next(csv.DictReader(open(RELAY / "relay_info.csv", encoding="utf-8")))
    entries = list(csv.DictReader(open(RELAY / "entries.tsv", encoding="utf-8"), delimiter="\t"))
    if len(entries) != int(info["entry_count"]):
        fail("브라우저 기록의 entry 수와 옮긴 행 수가 다릅니다.")
    ids = [e["entry_id"] for e in entries]
    if any(not i for i in ids) or len(set(ids)) != len(ids):
        fail("ID가 없거나 중복됩니다. 원문과 추출 규칙을 확인하세요.")
    out.mkdir(parents=True)
    (out / "source").mkdir()
    shutil.copy(RELAY / "relay_info.csv", out / "source" / "relay_info.csv")
    shutil.copy(RELAY / "entries.tsv", out / "source" / "entries.tsv")

    picked = entries[:3] if a.stage == "sample" else entries[: a.limit] if a.limit else entries
    name = "sample.csv" if a.stage == "sample" else "entries.csv"
    with open(out / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for e in picked:
            w.writerow([e["entry_id"], e["title"], e["link"], e["updated_at"], e["categories"],
                        info["collected_at_utc"], info["source_kind"]])
    (out / "collection_info.md").write_text(
        "# 수집 기록\n\n"
        f"- 목록 주소: {info['source_url']} (USGS · M2.5+ · Past Day)\n"
        f"- collected_at(원문 획득, UTC): {info['collected_at_utc']}\n"
        f"- 목록 갱신시각(feed updated): {info['feed_updated']}\n"
        f"- 바이트: {info['bytes']} · SHA-256: {info['sha256']}\n"
        f"- source_kind: {info['source_kind']} (작업 환경 차단으로 본인 브라우저에서 받음)\n"
        f"- published: {'제공' if info['published_present'] == 'true' else '미제공'}\n"
        "- 발생시각은 원문 summary의 Time에 있으나 이번 7열에서는 추출하지 않았다.\n", encoding="utf-8")
    lines = [f"- 원문 항목 수: {info['entry_count']}", f"- 저장 행 수: {len(picked)}",
             f"- 고유 ID 수: {len({e['entry_id'] for e in picked})}", f"- 목록 갱신시각: {info['feed_updated']}"]
    if a.limit:
        lines.append(f"- 선택 조건: 앞의 {a.limit}개(앞부분 선택이며 전체 사건 수나 무작위 표본이 아님)")
    (out / "summary.md").write_text("# 요약\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
