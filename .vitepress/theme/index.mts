import DefaultTheme from 'vitepress/theme';
import giscusTalk from 'vitepress-plugin-comment-with-giscus';
import { EnhanceAppContext, useData, useRoute } from 'vitepress';
import { toRefs } from "vue";

export default {
  ...DefaultTheme,
  enhanceApp(ctx: EnhanceAppContext) {
    DefaultTheme.enhanceApp(ctx);
  },
  setup() {
    const { frontmatter } = toRefs(useData());
    const route = useRoute();
    giscusTalk({
      repo: 'axiomofchoice-hjt/makeinu-daily',
      repoId: 'R_kgDOM8IAtA',
      category: 'Announcements', // default: `General`
      categoryId: 'DIC_kwDOM8IAtM4Ct-Nh',
      mapping: 'pathname', // default: `pathname`
      inputPosition: 'top', // default: `top`
      lang: 'zh-CN', // default: `zh-CN`
      // i18n setting (Note: This configuration will override the default language set by lang)
      // Configured as an object with key-value pairs inside:
      // [your i18n configuration name]: [corresponds to the language pack name in Giscus]
      locales: {
        'zh-Hans': 'zh-CN',
        'en-US': 'en'
      },
      homePageShowComment: false, // Whether to display the comment area on the homepage, the default is false
      lightTheme: 'light', // default: `light`
      darkTheme: 'transparent_dark', // default: `transparent_dark`
    }, {
      frontmatter, route
    },
      // Whether to activate the comment area on all pages.
      // The default is true, which means enabled, this parameter can be ignored;
      // If it is false, it means it is not enabled.
      // You can use `comment: true` preface to enable it separately on the page.
      true
    );
  },
};
