import fs from 'fs';
import path from 'path';

function recurse(dir: string, root: string): string[] {
  const stats = fs.statSync(dir);
  let result: string[] = [];
  if (stats.isDirectory()) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      result = result.concat(recurse(path.join(dir, file), root));
    }
  }
  if (stats.isFile() && dir.endsWith(".md") && path.relative(root, dir).replaceAll('\\', '/').includes('/')) {
    result.push(path.relative(root, dir.slice(0, -3)).replaceAll('\\', '/'));
  }
  return result;
}

function isNumericString(str: string): boolean {
  for (let i = 0; i < str.length; i++) {
    if (str.charCodeAt(i) < 48 || str.charCodeAt(i) > 57) {
      return false;
    }
  }
  return true;
}

export default (root: string) => {
  let result = recurse(root, root);
  result.sort((dir1: string, dir2: string) => {
    // topic 排在最前，index 其次，数字文件名排后面
    if (dir1.startsWith('topic/') != dir2.startsWith('topic/')) {
      return dir1.startsWith('topic/') ? -1 : 1;
    }
    if (dir1.endsWith('/index') != dir2.endsWith('/index')) {
      return dir1.endsWith('/index') ? -1 : 1;
    }
    return dir1.localeCompare(dir2);
  });
  return result;
};
