import { defineConfig, createContentLoader, SiteConfig } from 'vitepress';
import { Feed } from 'feed';
import getArticles from './articles.mts';
import getSidebar from './sidebar.mjs';
import { writeFileSync } from 'fs';
import path from 'path';

const host = 'https://makeinu-daily.pages.dev';

let articles = getArticles('src');
const sidebar = getSidebar(articles);

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "败犬日报",
  description: "C++ Makeinu Daily",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Latest', link: `/${articles[articles.length - 1]}` }
    ],

    sidebar,

    socialLinks: [
      { icon: 'rss', link: `${host}/feed.rss` },
      { icon: 'github', link: 'https://github.com/axiomofchoice-hjt/makeinu-daily' }
    ],
    search: {
      provider: 'local'
    },
    footer: {
      message: 'Released under the <a href="https://github.com/axiomofchoice-hjt/makeinu-daily/blob/main/LICENSE">MIT License</a>.',
      copyright: 'Copyright © 2024-present <a href="https://github.com/axiomofchoice-hjt">Axiomofchoice-hjt</a>'
    }
  },
  markdown: {
    lineNumbers: true,
    math: true
  },
  cleanUrls: true,
  srcDir: 'src',
  buildEnd: async (config: SiteConfig) => {
    const feed = new Feed({
      title: "败犬日报",
      description: "C++ Makeinu Daily",
      id: host,
      link: host,
      image: `${host}/favicon.jpg`,
      favicon: `${host}/favicon.ico`,
      copyright: 'Copyright © 2024-present Axiomofchoice-hjt',
    });

    const posts = await createContentLoader('*/*/*.md', {
      excerpt: true,
      render: true,
    }).load();

    posts.sort(
      (a, b) =>
        +new Date(b.frontmatter.date as string) -
        +new Date(a.frontmatter.date as string)
    );

    for (const { url, excerpt, frontmatter, html } of posts) {
      feed.addItem({
        title: frontmatter.title,
        id: `${host}${url}`,
        link: `${host}${url}`,
        description: excerpt,
        content: html,
        date: frontmatter.date,
      });
    }

    writeFileSync(path.join(config.outDir, 'feed.rss'), feed.rss2());
  },
});
