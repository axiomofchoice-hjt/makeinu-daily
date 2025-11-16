from articles import get_articles
from markdown_file import read_markdown_file

if __name__ == "__main__":
    articles = get_articles()
    monthly_articles = articles["monthly"]
    for article in monthly_articles[:2]:
        header, content = read_markdown_file(article)
        print(f"{content}\n")
