import { DefaultTheme } from 'vitepress';

function recurse(sidebar: DefaultTheme.SidebarItem[], article: string[], link: string) {
  link += "/" + article[0];
  if (article.length > 1) {
    const text = article[0];
    let item = sidebar.find((item) => item.text === text);
    if (item === undefined) {
      item = { text, items: [] };
      sidebar.push(item);
    }
    if (article.length == 2 && article[1] == 'index') {
      item.link = link;
    }
    if (item.items === undefined) { return; }  // make language server happy
    item.collapsed = true;  // 默认折叠
    recurse(item.items, article.slice(1), link);
  } else {
    if (link.startsWith('/topic/')) {
      console.log(link)
      sidebar.push({
        text: article[0],
        link: link.replace('/index', '/'),  // "/topic/index" 变成 "/topic/"，可以匹配到对应的侧边栏高亮
      });
    } else if (link.endsWith('/index')) {
      sidebar.push({
        text: "每月精选",
        link: link.replace('/index', '/'),  // "/YYYY/MM/index" 变成 "/YYYY/MM/"，可以匹配到对应的侧边栏高亮
      });
    } else {
      sidebar.push({
        text: link.replace('/', '').replaceAll('/', '-'),  // 移除开头的斜杠，剩下的斜杠替换成短横线
        link,
      });
    }
  }
}

export default (articles: string[]) => {
  let sidebar: DefaultTheme.SidebarItem[] = [];
  articles.forEach(article => {
    recurse(sidebar, article.split("/"), '');
  });
  sidebar.forEach(item => {
    if (item.text != 'topic') { item.collapsed = undefined; }
  });
  return sidebar;
};
