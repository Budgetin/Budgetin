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
          name: "Frozen Yogurt",
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: "1%",
        },
        {
          name: "Ice cream sandwich",
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          iron: "1%",
        },
        {
          name: "Eclair",
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0,
          iron: "7%",
        },
        {
          name: "Cupcake",
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3,
          iron: "8%",
        },
        {
          name: "Gingerbread",
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9,
          iron: "16%",
        },
        {
          name: "Jelly bean",
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0,
          iron: "0%",
        },
        {
          name: "Lollipop",
          calories: 392,
          fat: 0.2,
          carbs: 98,
          protein: 0,
          iron: "2%",
        },
        {
          name: "Honeycomb",
          calories: 408,
          fat: 3.2,
          carbs: 87,
          protein: 6.5,
          iron: "45%",
        },
        {
          name: "Donut",
          calories: 452,
          fat: 25.0,
          carbs: 51,
          protein: 4.9,
          iron: "22%",
        },
        {
          name: "KitKat",
          calories: 518,
          fat: 26.0,
          carbs: 65,
          protein: 7,
          iron: "6%",
        },
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
