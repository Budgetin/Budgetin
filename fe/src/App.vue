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

.v-dialog > .v-card > .v-card__title{
  font-size: 1.25rem !important;
  font-weight: 600 !important;
}

.v-card__title{
  font-size: 1.25rem !important;
  font-weight: 600 !important;
}
</style> 

<style lang="scss">
:root {
  --grey-bg: #f7f7f7;
}

/* GLOBAL TYPOGRAPHY  STYLING */
#app,
#master-coa,
#master-product,
#master-user,
#master-strategy,
#list-planning
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
  width: 90% !important;
  margin: 1% auto !important;
  background-color: white;
}

.v-input--is-disabled {
  .v-input__slot {
    background-color: var(--grey-bg) !important;
  }
}

a{
  background-color: white;
}

.rounded-card{
    border-radius:100%;
}

</style>
