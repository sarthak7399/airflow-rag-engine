import argparse
from pathlib import Path

import httpx

BASE = "https://airflow.apache.org/docs/apache-airflow/stable/"


def main():
    parser = argparse.ArgumentParser(description="Download Airflow docs (sample pages)")
    parser.add_argument("--out", type=str, default="data/raw/airflow-docs")
    parser.add_argument("--pages", nargs="*", default=["core-concepts/dags.html"])
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for page in args.pages:
        url = BASE + page
        resp = httpx.get(url, follow_redirects=True, timeout=60.0)
        resp.raise_for_status()
        dest = out / page.replace("/", "_")
        dest.write_text(resp.text, encoding="utf-8")
        print(f"saved {dest}")


if __name__ == "__main__":
    main()
