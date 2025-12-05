from datetime import datetime, timedelta
from articles import get_articles, path_to_date_str, src_path
from markdown_file import read_markdown_file, write_markdown_file

articles = [path_to_date_str(path) for path in get_articles()["daily"]]

previous = max(articles)
previous_ = datetime.strptime(previous, r"%Y/%m/%d")
current_ = previous_ + timedelta(days=1)
current = current_.strftime(r"%Y/%m/%d")

previous_file = src_path() / f"{previous}.md"
current_file = src_path() / f"{current}.md"


# 更新 <root>/<previous>.md
header, content = read_markdown_file(previous_file)
header["next"] = {
    "link": "/" + current,
    "text": "败犬日报 " + current.replace("/", "-"),
}
write_markdown_file(previous_file, header, content)

# 创建 <root>/<current>.md
header = {
    "date": current,
    "title": "败犬日报 " + current.replace("/", "-"),
    "next": False,
    "prev": {
        "link": "/" + previous,
        "text": "败犬日报 " + previous.replace("/", "-"),
    },
}
current_file.parent.mkdir(parents=True, exist_ok=True)
write_markdown_file(
    current_file,
    header,
    f"\n# 败犬日报 {current.replace("/", "-")}\n\n[[toc]]\n\n今日无话题收录 :kissing_heart:\n",
)

print(current_file)

# 更新 <root>/index.md
index_file = src_path() / "index.md"
header, content = read_markdown_file(index_file)
header["hero"]["actions"][0]["link"] = current
header["features"][0]["link"] = current
write_markdown_file(index_file, header, content)
