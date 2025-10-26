from pathlib import Path
import os
from chat import Chat
from markdown_file import read_markdown_file, write_markdown_file
import json

api_key = os.getenv("DEEPSEEK_API_KEY")
assert api_key is not None, "Please set the DEEPSEEK_API_KEY environment variable."
chat = Chat(api_key=api_key)

root = Path(__file__).parent.parent

prompt = (root / "script" / "llm_analysis_prompt.txt").read_text()


def process_file(file: Path):
    header, text = read_markdown_file(file.as_posix())
    if "description" in header and "__tags__" in header:
        return

    print(f"Analyzing {file}")
    chat.clear()
    result = chat.call(prompt + "\n" + text)
    result = result.strip()
    if result.startswith("```json"):
        result = result[len("```json") :]
    if result.endswith("```"):
        result = result[: -len("```")]
    (root / "llm_analysis.log").write_text(f"File: {file}\nResult:\n{result}\n\n")
    result = json.loads(result)

    header["description"] = result["description"]
    header["__tags__"] = result["__tags__"]
    write_markdown_file(file.as_posix(), (header, text))
    print(f"Finished")


for path, dirs, files in Path.walk(root / "src"):
    for file in files:
        file = path / file
        if file.suffix == ".md" and file.stem.isdigit():
            process_file(file)
