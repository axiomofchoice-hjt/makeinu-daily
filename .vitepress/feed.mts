import { Feed } from 'feed';
import { createContentLoader } from 'vitepress';

export default async () => {
  const host = 'https://makeinu-daily.pages.dev';

  const feed = new Feed({
    title: "败犬日报",
    description: "C++ Makeinu Daily",
    id: host,
    link: host,
    image: `${host}/favicon.jpg`,
    favicon: `${host}/favicon.ico`,
    copyright: 'Copyright © 2024-present Axiomofchoice-hjt',
  });

  let posts = await createContentLoader(['*.md', '*/*.md', '*/*/*.md'], {
    excerpt: true,
    render: true,
  }).load();

  posts = posts.filter(post => 'date' in post.frontmatter);
  posts.sort(
    (a, b) =>
      +new Date(b.frontmatter.date as string) -
      +new Date(a.frontmatter.date as string)
  );

  // 保留最后 100 篇
  posts.splice(100);

  // 移除代码行号
  const pattern = /<div class="line-numbers-wrapper" aria-hidden="true">.*?<\/div>/gs;
  for (const { url, excerpt, frontmatter, html } of posts) {
    feed.addItem({
      title: frontmatter.title,
      id: `${host}${url}`,
      link: `${host}${url}`,
      description: excerpt,
      content: html?.replaceAll(pattern, ''),
      date: frontmatter.date,
    });
  }

  return feed.rss2();
};
