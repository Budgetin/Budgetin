<template>
  <v-app>
    <sidebar />
    <v-main>
      <!-- MAIN VIEW -->
      <!-- <app-bar /> -->
      <router-view class="bg-grey"></router-view>
    </v-main>
    <!-- <div v-if="isActive" v-click-outside="TOOGLE_DRAWER">
      <drawer-matrix-summary />
    </div> -->
  </v-app>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";
// import AppBar from "../components/AppBar.vue";
// import DrawerMatrixSummary from "../components/DrawerMatrixSummary.vue";

import { mapGetters, mapActions } from "vuex";

export default {
  name: "Index",

  components: {
    Sidebar,
    // AppBar,
    // DrawerMatrixSummary,
  },
  computed: {
    // ...mapGetters("requestMpp", ["isActive"]),
  },
  methods: {
  },
};
</script>
