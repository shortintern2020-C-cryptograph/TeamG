<template>
  <div v-if="followingList.length" class="followers">
    <h4>Following</h4>
    <template v-for="follower in followingList">
      <UserStatus :key="follower" :name="follower" />
    </template>
  </div>
</template>

<script lang="ts">
/**
 * @author Kenya Sugimoto
 */
import { Component, Prop, Vue } from 'vue-property-decorator';
import UserStatus from '@/components/global/UserStatus.vue';

@Component({
  components: {
    UserStatus,
  },
})
export default class Follower extends Vue {
  @Prop({ required: true })
  followingList!: string[];

  @Prop({ required: true })
  name!: string;

  @Prop({ required: false })
  rank!: string;
}
</script>

<style lang="scss" scoped>
/**
 * @author Ryoya Wakuda
 */
  .followers {
    margin-top: 80px;
    h4 {
      font-size: 1.5em;
      font-weight: bold;
      text-decoration: underline;
    }
    .user-status {
      margin: 20px 0 0 1vw;
    }
  }
</style>
