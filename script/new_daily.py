from pathlib import Path
import yaml
from datetime import datetime, timedelta

root = Path(__file__).parent.parent / "src"

files = []
for file in root.rglob("*.md"):
    # 只处理日报，排除月报的 index.md
    if file.stem.isdigit():
        files.append(str(file).replace("\\", "/"))

previous = max(files)[-13:-3]
previous_ = datetime.strptime(previous, r"%Y/%m/%d")
current_ = previous_ + timedelta(days=1)
current = current_.strftime(r"%Y/%m/%d")


def read_markdown(file):
    with file.open(encoding="utf8") as f:
        lines = f.readlines()
        header = []
        if lines[0].strip() != "---":
            exit(1)
        for i, line in enumerate(lines[1:]):
            if line.strip() == "---":
                size = i + 2
                break
            header.append(line)
    return header, lines[size:]


def write_markdown(file, header, lines):
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open("w", encoding="utf8") as f:
        f.write("---\n")
        str_header = yaml.dump(header, allow_unicode=True)
        str_header = str_header.replace("'", "")
        f.write(str_header)
        f.write("---\n")
        f.writelines(lines)


# 更新 <root>/<previous>.md
file = root / f"{previous}.md"
header, lines = read_markdown(file)
header = yaml.safe_load("".join(header))
header["next"] = {
    "link": "/" + current,
    "text": "败犬日报 " + current.replace("/", "-"),
}
write_markdown(file, header, lines)

# 创建 <root>/<current>.md
file = root / f"{current}.md"
header = {
    "date": current.replace("/", "-"),
    "title": "败犬日报 " + current.replace("/", "-"),
    "next": False,
    "prev": {
        "link": "/" + previous,
        "text": "败犬日报 " + previous.replace("/", "-"),
    },
}
write_markdown(
    file,
    header,
    [
        f"\n# 败犬日报 {current.replace("/", "-")}\n\n[[toc]]\n\n今日无话题收录 :kissing_heart:\n"
    ],
)

print(root / f"{current}.md")

# 更新 <root>/index.md
file = root / "index.md"
header, lines = read_markdown(file)
header = yaml.safe_load("".join(header))
header["hero"]["actions"][0]["link"] = current
write_markdown(file, header, lines)
