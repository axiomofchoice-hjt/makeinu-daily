from typing import Dict, List
from collections import defaultdict
from pathlib import Path
import re


def walk(dir: Path):
    for path, _, files in Path.walk(dir):
        for file in files:
            yield path / file


def articles() -> Dict[str, List[Path]]:
    src = Path(__file__).parent.parent / "src"
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


if __name__ == "__main__":
    print(articles())
