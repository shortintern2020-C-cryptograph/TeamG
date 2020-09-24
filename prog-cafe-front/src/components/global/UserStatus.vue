<template>
  <div class="user-status" @click="toUserProfile(name)">
    <div class="user-icon-wrapper" :class="{ online: !!online, 'disp-online': dispOnlineStats }">
      <UserIcon :name="name" />
    </div>
    <UserName :name="name" />
    <div v-if="rank" class="user-rank">
      Rank {{rank}}
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import UserIcon from '@/components/global/UserIcon.vue';
import UserName from '@/components/global/UserName.vue';

@Component({
  components: {
    UserIcon,
    UserName,
  },
})
export default class UserStatus extends Vue {
  @Prop({ required: true }) name!: string;
  @Prop({ default: null, type: String }) rank!: string | null;
  @Prop({ default: null, type: Boolean }) online!: string | null;

  get dispOnlineStats() {
    return this.online != null;
  }

  toUserProfile(name: string) {
    if (this.$route.name !== 'User') this.$router.push({ name: 'User', params: { userId: name } });
    else if (this.$route.params.userId !== name) {
      this.$router.push({ name: 'User', params: { userId: name } });
    }
  }
}
</script>

<style lang="scss" scoped>
.user-status {
  display: grid;
  grid-template-columns: 10em minmax(0, 1fr);
  grid-template-areas:
    'icon name'
    'icon rank';
  cursor: pointer;

  .user-icon-wrapper {
    position: relative;
    height: 8em;
    width: 8em;

    grid-area: icon;

    .user-icon {
      width: 100%;
      height: 100%;
    }

    &.disp-online::after {
      content: '';
      position: absolute;
      bottom: 0;
      right: 0;
      display: block;
      width: 1.5em;
      height: 1.5em;
      border: 5px solid var(--background);
      border-radius: 50%;
      background: grey;
    }
    &.disp-online.online::after {
      background: green;
    }
  }
  .user-name {
    margin: 0;
    margin-top: 0.5em;
    font-size: 2em;

    grid-area: name;
  }
  .user-rank {
    font-size: 1.25em;
    grid-area: rank;
  }
}
</style>
