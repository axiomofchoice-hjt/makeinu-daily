from datetime import datetime, timedelta
from articles import get_articles, path_to_date_str, src_path
from markdown_file import read_markdown_file, write_markdown_file
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("delta", nargs='?', type=int, default=0)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    current_ = datetime.now() + timedelta(days=args.delta)
    current = current_.strftime(r"%Y/%m/%d")
    current_file = src_path() / f"{current}.md"

    # 创建 <root>/<current>.md
    header = {
        "date": current,
        "title": "败犬日报 " + current.replace("/", "-"),
        "next": False,
        "prev": False,
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
