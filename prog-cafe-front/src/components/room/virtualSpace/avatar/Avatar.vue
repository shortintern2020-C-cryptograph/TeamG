<template>
  <div class="avatar">
    <Fire :level="fireLevel" />
    <Coffee v-if="isBreaking" />
    <PC />
    <AvatarIcon
      :userId="userId"
      :tablePosition="tablePosition"
      :breaking="isBreaking"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AvatarIcon from '@/components/room/virtualSpace/avatar/AvatarIcon.vue';
import Fire from '@/components/room/virtualSpace/avatar/Fire.vue';
import PC from '@/components/room/virtualSpace/avatar/PC.vue';
import Coffee from '@/components/room/virtualSpace/avatar/Coffee.vue';
import StatusPopup from '@/components/room/virtualSpace/avatar/statusPopup/StatusPopup.vue';
import { store } from '@/utils/store';
import { activeTimeThreshold } from '@/utils/constants';

@Component({
  components: {
    AvatarIcon,
    Fire,
    PC,
    Coffee,
    StatusPopup,
  },
})
export default class Avatar extends Vue {
  @Prop({ required: true })
  userId!: string;

  @Prop({ required: true })
  tablePosition!: number;

  get fireLevel() {
    return store.progress[this.userId]
      ? Math.floor(store.progress[this.userId] / activeTimeThreshold)
      : 0;
  }

  get isBreaking() {
    return store.userStatus[this.userId]
      ? store.userStatus[this.userId] === 'Breaking'
      : false;
  }
}
</script>

<style lang="scss" scoped>
.avatar {
  position: relative;
  width: 100%;
}
</style>
