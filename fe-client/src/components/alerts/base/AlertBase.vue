<template>
  <v-dialog width="25rem" v-model="show" :persistent="persistent">
    <v-container class="white">
      <a-result :status="status" :title="shownTitle" :sub-title="shownSubtitle">
        <template #extra>
          <slot name="content"></slot>
        </template>
      </a-result>
    </v-container>
  </v-dialog>
</template>
<script>
export default {
  /**
   * possible status:
   * success, info, warning, error, 403, 404, 500
   *
   * possible title subtitle:
   * any string
   *
   * possible show:
   * boolean
   */
  name: "AlertBase",
  props: ["show", "title", "subtitle", "status", "persistent"],
  computed: {
    shownTitle() {
      return this.title ? this.title : "";
    },
    shownSubtitle() {
      return this.subtitle ? this.subtitle : "";
    },
  },
};
</script>