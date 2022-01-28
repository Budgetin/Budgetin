<template>
  <v-app>
    <sidebar />
    <v-main>
      <app-bar />
      <router-view class="bg-grey"></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";
import AppBar from "../components/AppBar.vue";

import { mapGetters, mapActions } from "vuex";

export default {
  name: "Index",

  components: {
    Sidebar,
    AppBar,
  },
  computed: {
  },
  methods: {
  },
};
</script>
