from datetime import datetime, timedelta
from articles import get_articles, path_to_date_str, src_path
from markdown_file import read_markdown_file, write_markdown_file
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("delta", nargs="?", type=int, default=0)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    current_ = datetime.now()
    current = current_.strftime(r"%Y/%m")
    current_ = datetime.strptime(current, r"%Y/%m") + timedelta(days=args.delta * 31)
    current = current_.strftime(r"%Y/%m")
    current_file = src_path() / current / "index.md"
    next_ = current_ + timedelta(days=31)
    next = next_.strftime(r"%Y/%m")

    # 创建 <root>/<today>.md
    header = {
        "date": next + "/01",
        "title": "败犬のC++每月精选 " + current.replace("/", "-"),
        "next": False,
        "prev": False,
    }
    write_markdown_file(
        current_file,
        header,
        f"\n# 败犬のC++每月精选 {current.replace("/", "-")}\n\n[[toc]]\n",
    )

    print(current_file)
