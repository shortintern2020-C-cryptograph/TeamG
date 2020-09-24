<template>
  <span class="tech">
    {{ skill }}
  </span>
</template>

<script lang="ts">
/**
 * @author Kenya Sugimoto
 */
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Tech extends Vue {
  @Prop({ required: true })
  skill!: string;
}
</script>

<style lang="scss" scoped>
  .tech {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 6em;
    height: 6em;
    background: var(--main);
    color: #fff;
    border-radius: 50%;
    font-size: 1.5em;

    overflow-wrap: anywhere;
  }
</style>
