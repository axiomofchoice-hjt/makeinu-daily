from pathlib import Path
import yaml

root = Path(__file__).parent.parent / 'src'

files = []
for file in root.rglob("*.md"):
    # 只处理日报，排除月报的 index.md
    if file.stem.isdigit():
        files.append(file)

for file in files:
    # 读取文件
    with file.open(encoding='utf8') as f:
        lines = f.readlines()
        header = []
        if lines[0].strip() != '---':
            continue
        for i, line in enumerate(lines[1:]):
            if line.strip() == '---':
                size = i + 2
                break
            header.append(line)
    # 解析 yaml
    header = yaml.safe_load(''.join(header))
    # 修改 publish 为 False
    header['publish'] = False
    # 写回
    with file.open('w', encoding='utf8') as f:
        f.write('---\n')
        yaml.dump(header, f, allow_unicode=True)
        f.write('---\n')
        f.writelines(lines[size:])
