<template>
  <div id="app">
    <Header />
    <router-view/>
    <Loading />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import Header from '@/components/global/header/Header.vue';
import Loading from '@/components/Loading.vue';
import { store } from '@/utils/store';
import { exit } from '@/utils/utils';

@Component({
  components: {
    Header,
    Loading,
  },
})
export default class App extends Vue {
  storeData = store;

  get githubId() {
    return store.githubId;
  }

  @Watch('githubId', { immediate: true })
  exit() {
    if (this.githubId === null && this.$route.name !== 'Sign in') exit();
  }
}
</script>

<style lang="scss">
* {
  box-sizing: border-box;
}
html, body {
  margin: 0;
  padding: 0;
  min-width: 100vw;
  min-height: 100vh;

  color: var(--font);
  background: url('./assets/background.jpg') center/cover no-repeat;

  font-family: 'Ubuntu', 'Noto Sans JP', sans-serif;

  overflow-x: hidden; // 最終奥義
}
</style>
