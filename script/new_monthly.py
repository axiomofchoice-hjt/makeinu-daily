from datetime import datetime, timedelta
from articles import get_articles, path_to_date_str, src_path
from markdown_file import read_markdown_file, write_markdown_file

articles = [path_to_date_str(path) for path in get_articles()["monthly"]]

previous = max(articles)
previous_ = datetime.strptime(previous, r"%Y/%m")
current_ = previous_ + timedelta(days=31)
current = current_.strftime(r"%Y/%m")
next_ = current_ + timedelta(days=31)
next = next_.strftime(r"%Y/%m")

previous_file = src_path() / previous / "index.md"
current_file = src_path() / current / "index.md"


# 更新 <root>/<previous>/index.md
header, content = read_markdown_file(previous_file)
header["next"] = {
    "link": "/" + current,
    "text": "败犬のC++每月精选 " + current.replace("/", "-"),
}
write_markdown_file(previous_file, header, content)

# 创建 <root>/<today>.md
header = {
    "date": next.replace("/", "-") + "-01",
    "title": "败犬のC++每月精选 " + current.replace("/", "-"),
    "next": False,
    "prev": {
        "link": "/" + previous,
        "text": "败犬のC++每月精选 " + previous.replace("/", "-"),
    },
}
write_markdown_file(
    current_file,
    header,
    f"\n# 败犬のC++每月精选 {current.replace("/", "-")}\n\n[[toc]]\n",
)

print(current_file)
