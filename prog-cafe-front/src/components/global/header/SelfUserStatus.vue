<template>
  <div @click="toSelfUserProfile" class="self-user-status">
    <img :src="icon" alt="self icon">
    <div>
      <h4>{{name}}</h4>
      <p>{{status}}</p>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * @author Sotaro Tomikawa
 */
import { store } from '@/utils/store';
import { getAvatarIconUrl } from '@/utils/utils';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class SelfUserStatus extends Vue {
  get name() {
    return store.githubId ?? 'ssssota';
  }
  get icon() {
    return getAvatarIconUrl(this.name);
  }
  get status() {
    return store.status;
  }

  /**
   * @author Kenya Sugimoto
   */
  toSelfUserProfile() {
    if (this.$route.params.userId !== this.name) this.$router.push({ name: 'User', params: { userId: this.name ?? '' } });
  }
}
</script>

<style lang="scss" scoped>
/**
 * @author Sotaro Tomikawa
 */
.self-user-status {
  height: 100%;
  display: flex;
  align-items: center;

  img {
    height: 60%;
    margin: 1em;
  }
  div {
    h4 {
      margin: 0.1em;
      font-size: 1.25em;
    }
    p {
      margin: 0;
    }
  }

  cursor: pointer;
}
</style>
