<template>
    <router-view class="bg-grey"></router-view>
</template>

<script>

export default {
  name: 'App',
  components: {},
  data: () => ({}),
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
#app
{
  font-family: "Nunito", sans-serif !important;
}

.v-data-table {
  font-family: "Nunito", sans-serif !important;
}

.bg-grey {
  background-color: var(--grey-bg) !important;
}

.outer-container {
  width: 80% !important;
  margin: 1% auto !important;
  background-color: white;
}

.v-btn--rounded {
  min-width: 8rem !important;
}

.v-input--is-disabled {
  .v-input__slot {
    background-color: var(--grey-bg) !important;
  }
}
</style>
