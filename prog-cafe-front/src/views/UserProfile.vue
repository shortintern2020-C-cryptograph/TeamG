<template>
  <div class="user-profile">
    <User :following="following" :name="targetId" :rank="rank" :online="online" />
    <div class="github-info">
      <GitHubSHIBA :githubId="targetId" />
      <Techs :skills="skills" />
      <Follower :name="followingList" :followingList="followingList" />
    </div>
  </div>
</template>

<script lang="ts">
/**
 * @author Kenya Sugimoto
 */
import { Component, Vue, Watch } from 'vue-property-decorator';
import User from '@/components/searchResults/user/User.vue';
import GitHubSHIBA from '@/components/userProfile/GitHubSHIBA.vue';
import Techs from '@/components/userProfile/techs/Techs.vue';
import Follower from '@/components/userProfile/Follower.vue';
import { getUserInfo } from '@/utils/http';
import { store } from '@/utils/store';

@Component({
  components: {
    User,
    GitHubSHIBA,
    Techs,
    Follower,
  },
})
export default class UserProfile extends Vue {
  following = false;
  skills = [] as string[];
  followingList = [] as string[];
  rank = '';
  online = false;

  get targetId() {
    return this.$route.params.userId;
  }
  get selfId() {
    return store.githubId ?? '';
  }

  @Watch('targetId', { immediate: true })
  getUserInfo() {
    getUserInfo(this.selfId, this.targetId, true).then((res) => {
      this.following = res.following;
      this.skills = res.skills;
      this.followingList = res.following_list ?? [];
      this.rank = res.rank;
      this.online = res.online;
    }).catch((err) => {
      console.error(err);
    });
  }
}
</script>

<style lang="scss" scoped>
/**
 * @author Ryoya Wakuda
 */
  .user-profile {
    width: 90vw;
    background: var(--background);
    padding: 3em;
    margin: 3em auto;
    box-shadow: 0px 0px 10px 0 var(--shadow);
  }
</style>
