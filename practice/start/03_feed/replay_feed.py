"""실습 C5 — C4에서 받은 같은 원문을 로컬에서 두 번 읽는다 (새 네트워크 요청 0회)

observations.csv : 처리 기록 (2회 × N행 = 2N행)
entities.csv     : 사건 (entry_id당 1행 = N행)
"""
import argparse
import csv
import datetime as dt
import hashlib
import sys
import time
from pathlib import Path


def fail(msg):
    print(f"[중단] {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-run", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    src = Path(a.input_run) / "entries.csv"
    if not src.exists():
        fail(f"{src}가 없습니다.")
    out = Path(a.out)
    if out.exists():
        fail(f"{out} 폴더가 이미 있습니다.")
    raw = src.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    out.mkdir(parents=True)

    observations, entities = [], {}
    for pass_number in (1, 2):
        processed_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
        for i, r in enumerate(rows, 1):
            observations.append({"observation_id": f"p{pass_number}-{i:03d}", "pass_number": pass_number,
                                 "processed_at": processed_at, **{**r, "source_kind": "snapshot"}})
            entities.setdefault(r["entry_id"], {**r, "source_kind": "snapshot"})
        time.sleep(1)

    for name, rows in (("observations.csv", observations), ("entities.csv", list(entities.values()))):
        with open(out / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    original_kind = next(csv.DictReader(raw.decode("utf-8").splitlines()))["source_kind"]
    (out / "replay_info.md").write_text(
        f"# 재처리 기록\n\n- 입력: {src} (SHA-256 {sha})\n- 새 네트워크 요청: 0회\n"
        f"- original_source_kind: {original_kind}\n- collected_at은 C4 값을 유지했다.\n"
        f"- observations: {len(observations)}행, entities: {len(entities)}행\n", encoding="utf-8")
    print(f"observations {len(observations)}행 / entities {len(entities)}행")


if __name__ == "__main__":
    main()
