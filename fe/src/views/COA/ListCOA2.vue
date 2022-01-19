<template>
  <v-app id="master-coa">
    <v-container class="master-coa__container outer-container">
      <!-- <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-subheader class="master-coa__header"> Master COA </v-subheader>
        </v-col>
      </v-row> -->

      <v-card class="rounded-xl pa-2">
        <v-card-title>
          Master COA
        </v-card-title>
        <v-card-subtitle>
          <v-row no-gutters>
            <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
              <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search"
                  hide-details>
              </v-text-field>
            </v-col>
            <v-col cols="12" xs="12" sm="6" md="8" lg="8" no-gutters class="d-flex justify-end">
              <v-btn rounded color="primary">
                Add COA
              </v-btn>
            </v-col>
          </v-row>
        </v-card-subtitle>

        <v-row no-gutters class="ma-2">
          
        </v-row>
        <v-data-table
          :headers="headers"
          :items="desserts"
          :search="search"
        ></v-data-table>
      </v-card>

    </v-container>
  </v-app>
</template>
<script>
export default {
  data() {
    return {
      search: "",
      headers: [
        {
          text: "ID",
          align: "start",
          sortable: true,
          value: "id",
        },
        { text: "COA", value: "coa" },
        { text: "Hyperion Name", value: "hyperion" },
        { text: "Update By", value: "update_by" },
        { text: "Update Date", value: "update_date" },
        { text: "Status", value: "status" },
        { text: "Actions", value: "actions", align: "center", sortable: false }
      ],
      desserts: [
        {
          id: 1,
          coa: 159,
          hyperion: 6.0,
          update_by: 24,
          update_date: 4.0,
          status: "1%",
        }
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
#master-coa {
  .master-coa__btn {
    text-align: end;
  }
}
