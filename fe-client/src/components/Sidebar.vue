<template>
  <div>
    <v-navigation-drawer
      expand-on-hover
      permanent
      dark
      class="gradient elevation-15"
      app
      mini-variant-width="5rem"
    >
      <v-list nav class="px-0 mx-0">
        <v-list-item class="px-0 mx-0">
          <v-list-item-icon class="px-2">
            <img src="../assets/LogoPutih.svg" height="40px" />
          </v-list-item-icon>
          <v-list-item-title>
            <img :src="require('../assets/TextPutih.png')" height="40px" />
          </v-list-item-title>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list shaped>
        <v-list-item link :to="'/home'">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        <v-list-item link :to="'/myBudget'" replace>
          <v-list-item-icon>
            <v-icon>mdi-format-list-bulleted </v-icon>
          </v-list-item-icon>
          <v-list-item-title>My Budget</v-list-item-title>
        </v-list-item>
        <v-list-item link :to="'/myProject'" replace>
          <v-list-item-icon>
            <v-icon>mdi-folder-network </v-icon>
          </v-list-item-icon>
          <v-list-item-title>My Project</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>
<script>
// import AppBar from "../components/AppBar.vue";
export default {
  name: "SideBar",
  components: {
    // AppBar,
  },
};
</script>

<style scoped>
.gradient {
  z-index: 15;
  background: rgb(14, 6, 83);
  background: linear-gradient(
    180deg,
    rgba(20, 143, 205, 1) 0%,
    /* rgba(47, 232, 253, 1) 20%, */
    rgb(109, 7, 185) 100%
  );
}

.v-list-item__title{
  font-size: 14px;
}

</style>
