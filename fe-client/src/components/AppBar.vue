<template>
  <v-app-bar id="app-bar" class="bg-grey elevation-0" prominent flat app dense>
    <v-toolbar-title >
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
      <!-- v-if="userInitial=='Admin'" -->
      <!-- <span class="white--text text-h6" >{{ getInitial }}</span> -->
      <span class="white--text text-h6" v-if="userInitial">{{ userInitial }}</span>
    </v-avatar>

    <v-btn icon style="margin: auto 0px" @click="logout">
      <v-icon color="red">mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
import { mapState,mapActions } from "vuex";
export default {
  name: "AppBar",
  created(){
    this.getInitial();
  },
  computed: {
    ...mapState("breadcrumbs", ["links"]),
    ...mapState("login", ["userInitial"]),
  },
  methods: {
    ...mapActions("login", ["logOut","setInitial"]),
    logout() {
      this.logOut();
    },
    getInitial(){
      if(!this.userInitial){
        this.setInitial();
      };
    }
  },
};
</script>
<style scoped>
#app-bar{
   z-index: 14;
}
</style>

<style lang="scss"></style>
