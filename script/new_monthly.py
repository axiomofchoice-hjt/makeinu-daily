from pathlib import Path
import yaml
from datetime import datetime, timedelta

root = Path(__file__).parent.parent / "src"

files = []
for file in root.rglob("index.md"):
    # 只处理月报，排除主页 index.md
    if file.parent.name not in ["src", "topic"]:
        files.append(str(file).replace("\\", "/"))


previous = max(files)[-16:-9]
previous_ = datetime.strptime(previous, r"%Y/%m")
current_ = previous_ + timedelta(days=31)
current = current_.strftime(r"%Y/%m")
next_ = current_ + timedelta(days=31)
next = next_.strftime(r"%Y/%m")


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


# 更新 <root>/<previous>/index.md
file = root / f"{previous}/index.md"
header, lines = read_markdown(file)
header = yaml.safe_load("".join(header))
header["next"] = {
    "link": "/" + current,
    "text": "败犬のC++每月精选 " + current.replace("/", "-"),
}
write_markdown(file, header, lines)

# 创建 <root>/<today>.md
file = root / f"{current}/index.md"
header = {
    "date": next.replace("/", "-") + "-01",
    "title": "败犬のC++每月精选 " + current.replace("/", "-"),
    "next": False,
    "prev": {
        "link": "/" + previous,
        "text": "败犬のC++每月精选 " + previous.replace("/", "-"),
    },
}
write_markdown(
    file,
    header,
    [f"\n# 败犬のC++每月精选 {current.replace("/", "-")}\n\n[[toc]]\n"],
)

print(root / f"{current}/index.md")
