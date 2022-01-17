<template>
  <v-app>
    <sidebar />
    <v-main style="padding: 0 10%;">
      <router-view class="bg-grey"></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";

import { mapGetters, mapActions } from "vuex";

export default {
  name: "Index",

  components: {
    Sidebar,
  },
  computed: {
  },
  methods: {
  },
};
</script>
