<script setup>
import DefaultTheme from 'vitepress/theme'

const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <template #nav-bar-content-before>
      <span class="current-page-title" v-if="$frontmatter.layout !== 'home'">
        {{ $frontmatter.title }}
      </span>
    </template>
  </Layout>
</template>

<style scoped>
.current-page-title {
  margin-left: 2rem;
  xfont-weight: 600;
  color: var(--vp-c-text-1);
}
</style>
