<template>
  <img src="@/assets/coffee.png" alt="Coffee" class="coffee">
</template>

<style lang="scss" scoped>
/**
 * @author Sotaro Tomikawa
 */
.coffee {
  position: absolute;
  top: 30%;
  right: 0;
  width: 4em;
  transform: translateY(-50%);
}
/**
 * @author Ryoya Wakuda
 */
/* vendor prefix for Safari */
@media screen and (-webkit-min-device-pixel-ratio:0) {
  _::-webkit-full-page-media, _:future, :root .coffee {
    top: -28vh;
  }
}
</style>
