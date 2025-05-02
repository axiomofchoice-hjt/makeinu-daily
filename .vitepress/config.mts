import { defineConfig, createContentLoader, SiteConfig } from 'vitepress';
import getArticles from './articles.mts';
import getSidebar from './sidebar.mjs';
import feed from './feed.mjs';
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
      { text: 'About', link: '/about' },
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
      message: 'Released under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0 License</a>.',
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
    writeFileSync(path.join(config.outDir, 'feed.rss'), await feed());
  },
});
