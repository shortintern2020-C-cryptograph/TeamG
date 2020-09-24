<template>
  <header>
    <div @click="toRoom" class="logos">
      <img src="@/assets/logo.svg" class="logo">
      <img src="@/assets/title.svg" class="title">
    </div>
    <SearchBox />
    <SelfUserStatus />
  </header>
</template>

<script lang="ts">
/**
 * @author Kenya Sugimoto
 */
import { Component, Vue } from 'vue-property-decorator';
import SearchBox from '@/components/global/header/SearchBox.vue';
import SelfUserStatus from '@/components/global/header/SelfUserStatus.vue';
import { store } from '@/utils/store';

@Component({
  components: {
    SearchBox,
    SelfUserStatus,
  },
})
export default class Header extends Vue {
  toRoom() {
    if (this.$route.name !== 'Room') this.$router.push({ name: 'Room', params: { roomId: store.roomId ?? '' } });
  }
}
</script>

<style lang="scss" scoped>
/**
 * @author Sotaro Tomikawa
 */
header {
  width: 100vw;
  height: 10vh;
  margin: 0;
  padding: 0 32px;
  position: relative;

  display: flex;
  justify-content: space-between;
  align-items: center;

  background: var(--background);
  box-shadow: 0 0 10px 0 var(--shadow);

  .logos {
    height: 100%;
    display: flex;
    align-items: center;
    .logo {
      height: 60%;
      margin-right: 16px;
    }
    .title {
      height: 50%;
    }
    cursor: pointer;
  }
}
</style>
