import { defineConfig, createContentLoader, SiteConfig } from 'vitepress';
import getArticles from './articles.mts';
import getSidebar from './sidebar.mjs';
import feed from './feed.mjs';
import { writeFileSync } from 'fs';
import path from 'path';
import { withPwa } from '@vite-pwa/vitepress';

const host = 'https://makeinu-daily.pages.dev';

let articles = getArticles('docs');
const sidebar = getSidebar(articles);

// https://vitepress.dev/reference/site-config
export default withPwa(defineConfig({
  title: "败犬日报",
  description: "C++ Makeinu Daily",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'About', link: '/about' },
      { text: 'Topic', link: '/topic/' },
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
      message: 'Powered by <a href="https://vitepress.dev/">VitePress</a>. Released under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> License.',
      copyright: 'Copyright © 2024-present <a href="https://github.com/axiomofchoice-hjt">axiomofchoice-hjt</a>'
    },
    outline: {
      label: '页面导航'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页',
    },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
  },
  markdown: {
    lineNumbers: true,
    math: true
  },
  cleanUrls: true,
  buildEnd: async (config: SiteConfig) => {
    writeFileSync(path.join(config.outDir, 'feed.rss'), await feed());
  },
  base: process.env.VITE_APP_BASE_URL || '/',
  pwa: {
    registerType: 'autoUpdate',
    includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
    workbox: {
      globPatterns: ['**/*.{js,css,ico,png,svg,woff2}'],
      skipWaiting: true,
      clientsClaim: true,
      navigateFallback: undefined,
      runtimeCaching: [
        {
          urlPattern: ({ request }) => request.destination === 'document',
          handler: 'NetworkFirst',
          options: {
            cacheName: 'html-pages',
            expiration: {
              maxEntries: 30,
            },
          },
        },
      ],
    },
    manifest: {
      name: '败犬日报',
      short_name: 'Makeinu Daily',
      description: 'C++ Makeinu Daily',
      theme_color: '#ffffff',
      icons: [
        {
          src: '/pwa-192x192.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: '/pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png'
        },
      ],
    },
  },
}));
