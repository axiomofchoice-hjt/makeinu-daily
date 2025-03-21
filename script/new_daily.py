from pathlib import Path
from httpx import head
import yaml
from datetime import datetime, timedelta

root = Path(__file__).parent.parent / "src"

files = []
for file in root.rglob("*.md"):
    # 只处理日报，排除月报的 index.md
    if file.stem.isdigit():
        files.append(str(file).replace("\\", "/"))

yesterday = max(files)[-13:-3]
print(yesterday)
yesterday_ = datetime.strptime(yesterday, r"%Y/%m/%d")
today_ = yesterday_ + timedelta(days=1)
today = today_.strftime(r"%Y/%m/%d")


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
    with file.open("w", encoding="utf8") as f:
        f.write("---\n")
        str_header = yaml.dump(header, allow_unicode=True)
        str_header = str_header.replace("'", "")
        f.write(str_header)
        f.write("---\n")
        f.writelines(lines)


# 更新 <root>/<yesterday>.md
file = root / f"{yesterday}.md"
header, lines = read_markdown(file)
header = yaml.safe_load("".join(header))
header["next"] = {"link": today, "text": "败犬日报 " + today.replace("/", "-")}
write_markdown(file, header, lines)

# 创建 <root>/<today>.md
file = root / f"{today}.md"
header = {
    "date": today.replace("/", "-"),
    "title": "败犬日报 " + today.replace("/", "-"),
    "next": False,
    "prev": {"link": yesterday, "text": "败犬日报 " + yesterday.replace("/", "-")},
}
write_markdown(
    file,
    header,
    [
        f"\n# 败犬日报 {today.replace("/", "-")}\n\n[[toc]]\n\n今日无话题收录 :kissing_heart:\n"
    ],
)

print(root / f"{today}.md")

# 更新 <root>/index.md
file = root / "index.md"
header, lines = read_markdown(file)
header = yaml.safe_load("".join(header))
header["hero"]["actions"][0]["link"] = today
write_markdown(file, header, lines)
