from typing import Dict, List
from collections import defaultdict
from pathlib import Path
import re
from datetime import datetime


def walk(dir: Path):
    for path, _, files in Path.walk(dir):
        for file in files:
            yield path / file


def src_path() -> Path:
    return Path(__file__).parent.parent / "src"

def get_articles() -> Dict[str, List[Path]]:
    src = src_path()
    articles = defaultdict(list)
    for file in walk(src):
        rel = file.relative_to(src)
        if re.match(r"[0-9]{4}/[0-9]{2}/[0-9]{2}\.md", rel.as_posix()):
            articles["daily"].append(file)
        elif re.match(r"[0-9]{4}/[0-9]{2}/index\.md", rel.as_posix()):
            articles["monthly"].append(file)
        elif re.match(r"topic/.*\.md(?<!topic/index\.md)", rel.as_posix()):
            articles["topic"].append(file)
    return dict(articles)


def path_to_date_str(path: Path) -> str:
    if path.name == "index.md":
        return path.parent.relative_to(src_path()).as_posix()
    return path.relative_to(src_path()).as_posix()[:-3]


def path_to_datetime(path: Path) -> datetime:
    return datetime.strptime(path_to_date_str(path), r"%Y/%m/%d")


if __name__ == "__main__":
    print(get_articles())
