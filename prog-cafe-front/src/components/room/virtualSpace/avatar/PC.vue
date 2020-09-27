<template>
  <img class="pc" src="@/assets/PC_right.png">
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class PC extends Vue {}
</script>

<style lang="scss" scoped>
/**
 * @author Sotaro Tomikawa
 */
.pc {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
}
/**
 * @author Ryoya Wakuda
 */
/* vendor prefix for Safari */
@media screen and (-webkit-min-device-pixel-ratio:0) {
  _::-webkit-full-page-media, _:future, :root .pc {
    top: -40vh;
  }
}
</style>
