<template>
  <v-app>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>

<style>
/* GLOBAL FONT IMPORT */
@import url("https://fonts.googleapis.com/css2?family=Nunito&display=swap");
</style> 

<style lang="scss">
:root {
  --grey-bg: #f7f7f7;
}

/* GLOBAL TYPOGRAPHY  STYLING */
#app,
#goal-mpp,
#request-mpp,
#edit-status-request,
#setting-inputAccess,
#setting-notification,
#master-category,
#master-source,
#setting-pic {
  font-family: "Nunito", sans-serif !important;
}

.v-data-table {
  font-family: "Nunito", sans-serif !important;
}

</style>
