import { DefaultTheme } from 'vitepress';

function recurse(sidebar: DefaultTheme.SidebarItem[], article: string[], link: string, collapsed: boolean) {
  link += (link.length ? '/' : '') + article[0];
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
    if (item.items === undefined) { return; } // make language server happy
    item.collapsed = collapsed;
    recurse(item.items, article.slice(1), link, collapsed);
  } else {
    if (link.startsWith('topic/')) {
      sidebar.push({ text: article[0], link });
    } else if (link.endsWith('/index')) {
      sidebar.push({ text: "每月精选", link });
    } else {
      sidebar.push({ text: link.replaceAll('/', '-'), link });
    }
  }
}

export default (articles: string[]) => {
  console.log(articles);
  let sidebar: DefaultTheme.SidebarItem[] = [];
  articles.forEach(article => {
    recurse(sidebar, article.split("/"), '', article !== articles[articles.length - 1]);
  });
  sidebar.forEach(item => {
    if (item.text != 'topic') { item.collapsed = undefined; }
  });
  return sidebar;
};
