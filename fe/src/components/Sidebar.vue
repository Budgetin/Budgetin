<template>
  <div>
    <v-navigation-drawer
      permanent
      dark
      class="gradient"
      app
      mini-variant-width="5rem"
      width="13rem"
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
        <v-list-item replace>
          <v-list-item-icon>
            <v-icon>mdi-chart-scatter-plot</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item link :to="'/startPlanning'" replace>
          <v-list-item-icon>
            <v-icon>mdi-play-circle </v-icon>
          </v-list-item-icon>
          <v-list-item-title>Start Planning</v-list-item-title>
        </v-list-item>
        <v-list-item link :to="'/listBudget'" replace>
          <v-list-item-icon>
            <v-icon>mdi-format-list-bulleted </v-icon>
          </v-list-item-icon>
          <v-list-item-title>List Budget</v-list-item-title>
        </v-list-item>
        <v-list-item link :to="'/listProject'" replace>
          <v-list-item-icon>
            <v-icon>mdi-folder-network </v-icon>
          </v-list-item-icon>
          <v-list-item-title>Project List</v-list-item-title>
        </v-list-item>
        <v-list-group
          :value="true"
          no-action
          active-class= "white--text">
         <template v-slot:activator>
              <v-list-item-icon>
                <v-icon>mdi-view-grid</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Master</v-list-item-title>
          </template>
          <v-list-item link :to="'/coa'" replace active-class= "white--text">
              <v-list-item-title>COA</v-list-item-title>
          </v-list-item>
          <v-list-item link :to="'/product'" replace active-class= "white--text">
              <v-list-item-title>Product</v-list-item-title>
          </v-list-item>
          <v-list-item link :to="'/strategy'" replace active-class= "white--text">
              <v-list-item-title>Strategy</v-list-item-title>
          </v-list-item>
          <v-list-item link :to="'/user'" replace active-class= "white--text">
              <v-list-item-title>User</v-list-item-title>
          </v-list-item>
        </v-list-group>
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
  background: rgb(14, 6, 83);
  background: linear-gradient(
    180deg,
    rgba(14, 6, 83, 1) 0%,
    rgba(14, 6, 83, 1) 15%,
    rgba(47, 232, 253, 1) 100%
  );
}

.v-list-item__title{
  font-size: 14px;
}

</style>
