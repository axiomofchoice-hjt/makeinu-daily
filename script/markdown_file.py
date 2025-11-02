import yaml
from typing import Tuple
from pathlib import Path


def read_markdown_file(file_path: str | Path) -> Tuple[dict, str]:
    """Reads a markdown file and returns its YAML header and content."""
    with open(file_path, "r", encoding="utf8") as f:
        lines = f.readlines()
        header = []
        assert lines[0].strip() == "---", "Markdown file must start with a YAML header."
        for i, line in enumerate(lines[1:]):
            if line.strip() == "---":
                size = i + 2
                break
            header.append(line)
    header = yaml.safe_load("".join(header))
    content = "".join(lines[size:])
    return header, content


def write_markdown_file(file_path: str | Path, header: dict, content: str) -> None:
    """Writes a markdown file with the given YAML header and content."""
    with open(file_path, "w", encoding="utf8") as f:
        f.write("---\n")
        str_header = yaml.dump(
            header,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,  # 保持原始键顺序
            Dumper=yaml.SafeDumper,
        )
        f.write(str_header)
        if not str_header.endswith("\n"):
            f.write("\n")
        f.write("---\n")
        f.write(content)
