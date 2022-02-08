<template>
  <v-app>
    <sidebar v-if="routing!='Login'"/>
    <v-main>
      <app-bar v-if="routing!='Login'"/>
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
  computed : {
      routing : function(){ return this.$route.name}
    },
  methods: {
  },
};
</script>
