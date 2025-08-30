#!/usr/bin/env python3
import csv
import argparse
from collections import OrderedDict
from pathlib import Path


def dedupe_by_id(csv_path: Path, id_field: str = "id", keep: str = "last") -> int:
    """
    Dedupe rows by `id_field`.

    keep:
      - "last": keep the last occurrence in the file (treat as newest)
      - "first": keep the first occurrence
    Returns number of removed rows.
    """
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)

    # Find which index to keep per id
    last_index: dict[str, int] = {}
    first_index: dict[str, int] = {}
    for idx, row in enumerate(rows):
        row_id = row.get(id_field)
        key = str(row_id) if row_id is not None else None
        if key is None:
            continue
        last_index[key] = idx
        if key not in first_index:
            first_index[key] = idx

    # Write back
    tmp_path = csv_path.with_suffix(".dedup.tmp")
    with tmp_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        kept_ids = set()
        for idx, row in enumerate(rows):
            row_id = row.get(id_field)
            key = str(row_id) if row_id is not None else None
            if key is None:
                writer.writerow(row)
                continue
            if keep == "last":
                if last_index.get(key) == idx and key not in kept_ids:
                    writer.writerow(row)
                    kept_ids.add(key)
            else:  # keep == first
                if first_index.get(key) == idx and key not in kept_ids:
                    writer.writerow(row)
                    kept_ids.add(key)

    # Replace original (keep a .bak backup)
    bak_path = csv_path.with_suffix(".bak")
    if bak_path.exists():
        bak_path.unlink()
    csv_path.replace(bak_path)
    tmp_path.replace(csv_path)

    removed = 0
    # To compute removed accurately, we need to re-count input rows
    with bak_path.open("r", encoding="utf-8", newline="") as f:
        before = sum(1 for _ in f) - 1  # minus header
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        after = sum(1 for _ in f) - 1
    return max(0, before - after)


def main():
    parser = argparse.ArgumentParser(
        description="Dedupe twitter_following_list_data.csv by id, keeping the newest (last occurrence)"
    )
    parser.add_argument(
        "--csv",
        default="twitter_following_list_data.csv",
        help="Path to CSV file (default: twitter_following_list_data.csv)",
    )
    parser.add_argument(
        "--keep",
        choices=["last", "first"],
        default="last",
        help="Which duplicate to keep: last (newest) or first",
    )
    parser.add_argument(
        "--id-field",
        default="id",
        help="ID field name to dedupe by (default: id)",
    )
    args = parser.parse_args()

    removed = dedupe_by_id(Path(args.csv), id_field=args.id_field, keep=args.keep)
    print(f"Deduped by '{args.id_field}', removed {removed} duplicate rows, backup saved as .bak")


if __name__ == "__main__":
    main()
