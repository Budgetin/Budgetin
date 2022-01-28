<template>
  <v-app-bar class="bg-grey" prominent flat app dense>
    <v-toolbar-title>
      <v-breadcrumbs
        :items="links"
        large
        class="font-weight-bold pt-6"
      ></v-breadcrumbs>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-avatar
      color="blue"
      size="50"
      class="elevation-3"
      style="margin: auto 0px"
    >
      <!-- <span class="text-caption">photo</span> -->
      <span class="white--text text-h6">FNA</span>
    </v-avatar>

    <v-btn icon style="margin: auto 0px">
      <v-icon color="red">mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
// import formatting from "@/mixins/formatting";
import { mapState } from "vuex";
export default {
  name: "AppBar",
  computed: {
    ...mapState("breadcrumbs", ["links"]),
  },
  // mixins: [formatting],
};
</script>

<style lang="scss">
</style>