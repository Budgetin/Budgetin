<template>
  <v-app id="submitted-planning">
    <v-container class="submitted-planning__container outer-container">
      <v-row no-gutters>
          <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
              <v-subheader class="submitted-planning__header">Submitted Planning</v-subheader>
          </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <!-- <v-data-table
            :items="dataListBudget"
            :loading="loadingGetListBudget"
            :headers="listColumn"
            :search="search"
          > -->
          <v-data-table
            :headers="listColumn"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="3" lg="3" no-gutters>
                    <v-text-field
                      class="submitted-planning__input"
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Search"
                      hide-details
                    >
                    </v-text-field>
                  </v-col>

                  <v-col
                    cols="12"
                    xs="12"
                    sm="6"
                    md="8"
                    lg="8"
                    no-gutters
                    class="submitted-planning__btn"
                  >
                    <v-btn rounded color="#16B1FF">Existing</v-btn>
                    <v-btn rounded color="#7E73FF">New</v-btn>
                    <v-btn rounded outlined>
                          Download
                    </v-btn>
                  </v-col>
                  
                </v-row>
              </v-toolbar-title>
            </template>

            <!-- <template v-slot:[`item.is_budget`]="{ item }">
                <binary-yes-no-chip :boolean="item.is_budget"> </binary-yes-no-chip>
            </template>
            <template v-slot:[`item.project_detail.project.is_tech`]="{ item }">
                <binary-yes-no-chip :boolean="item.project_detail.project.is_tech"> </binary-yes-no-chip>
            </template> -->
          </v-data-table>
        </v-col>
      </v-row>

      <v-row no-gutters>
          <v-dialog v-model="isLoading" persistent width="25rem">
            <v-card >
              <v-card-title class="d-flex justify-center">
                Loading
              </v-card-title>

              <v-card-text>
                <v-row no-gutters class="d-flex justify-center">
                  <v-progress-circular
                    :size="70"
                    :width="7"
                    color="purple"
                    indeterminate
                  ></v-progress-circular>
                </v-row>
              </v-card-text>
            </v-card>
          </v-dialog>
      </v-row>
    </v-container>

    <success-error-alert
      :success="alert.success"
      :show="alert.show"
      :title="alert.title"
      :subtitle="alert.subtitle"
      @okClicked="onAlertOk"
    />
  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert";
import BinaryYesNoChip from "@/components/chips/BinaryYesNoChip";
export default {
  name: "ListBudget",
  components: {SuccessErrorAlert,BinaryYesNoChip},
  watch: {},
  data: () => ({
    search: "",
    dataTable: {
      selectedHeader: [],
      Listheader: [
        { text: "Project ID", value: "project_detail.dcsp_id", width: "7rem" },
        { text: "Project Name", value: "project_detail.project.project_name", width: "8rem" },
        { text: "Biro", value: "project_detail.project.biro.code", width: "5rem" },
        { text: "ID ITFAM", value: "project_detail.project.itfam_id", width: "7rem" },
        {
          text: "Project Description",
          value: "project_detail.project.project_description",
          width: "10rem",
        },
        { text: "Tech / Non Tech", value: "project_detail.project.is_tech", width: "9rem" },
        {
          text: "Product ID",
          value: "project_detail.project.product.product_code",
          width: "7rem",
        },
        { text: "RCC", value: "project_detail.project.biro.rcc", width: "5rem" },
        { text: "Project Type", value: "project_detail.project_type", width: "9rem" },
        { text: "Is Budget", value: "is_budget", width: "7rem" },
        { text: "COA", value: "coa", width: "5rem" },
        {
          text: "Capex/Opex",
          value: "expense_type",
          width: "8rem",
        },
        { text: "Start Year", value: "project_detail.project.start_year", width: "7rem" },
        { text: "End Year", value: "project_detail.project.end_year", width: "7rem" },
        {
          text: "Total Investment",
          value: "project_detail.project.total_investment_value",
          width: "9rem",
        },
        {
          text: "Budget This Year",
          value: "budget_nominal",
          width: "9rem",
        },
        { text: "Planning Q1", value: "planning_q1", width: "5rem" },
        { text: "Planning Q2", value: "planning_q2", width: "5rem" },
        { text: "Planning Q3", value: "planning_q3", width: "5rem" },
        { text: "Planning Q4", value: "planning_q4", width: "5rem" },
        { text: "Realization Jan", value: "realization_jan", width: "5rem" },
        { text: "Realization Feb", value: "realization_feb", width: "5rem" },
        { text: "Realization Mar", value: "realization_mar", width: "5rem" },
        { text: "Realization Apr", value: "realization_apr", width: "5rem" },
        { text: "Realization May", value: "realization_may", width: "5rem" },
        { text: "Realization Jun", value: "realization_jun", width: "5rem" },
        { text: "Realization Jul", value: "realization_jul", width: "5rem" },
        { text: "Realization Aug", value: "realization_aug", width: "5rem" },
        { text: "Realization Sep", value: "realization_sep", width: "5rem" },
        { text: "Realization Oct", value: "realization_oct", width: "5rem" },
        { text: "Realization Nov", value: "realization_nov", width: "5rem" },
        { text: "Realization Dec", value: "realization_dec", width: "5rem" },
        {
          text: "Strategy",
          value: "project_detail.project.product.strategy",
          width: "6rem",
        },
        { text: "Created By", value: "created_by", width: "7rem" },
        { text: "Updated At", value: "updated_at", width: "8rem" },
      ],
    },
    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
  }),
  created() {
    this.setBreadcrumbs();
  },
  computed: {
    // ...mapState("listBudget", ["loadingGetListBudget", "loadingGetListInactiveBudget", "dataListBudget", "dataListInactiveBudget", "isLoading"]),
    // ...mapState("choosedColumn", ["listColumn"]),
  },
  methods: {
    // ...mapActions("listBudget", ["getListBudget", "getListInactiveBudget", "postListBudget","importBudget","importRealization"]),
    setBreadcrumbs() {
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Home",
          link: false,
          exact: true,
          disabled: true,
        },
      ]);
    },
    onSaveSuccess() {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Save Success";
      this.alert.subtitle = "Budget has been saved successfully";
    },
    onSaveError(error) {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = false;
      this.alert.title = "Save Failed";
      this.alert.subtitle = error;
    },
    onAlertOk() {
      this.alert.show = false;
    },
  }
};
</script>

<style scoped>
::v-deep button {
  min-width: 2rem;
}

::v-deep table > tbody > tr:hover td:nth-child(1),
::v-deep table > tbody > tr:hover td:nth-child(2),
::v-deep table > tbody > tr:hover td:nth-child(3),
::v-deep table > tbody > tr:hover td:nth-child(4){
  background: #EEEEEE;
}

::v-deep table > tbody > tr > td:nth-child(1),
::v-deep table > thead > tr > th:nth-child(1) {
  position: sticky !important;
  position: -webkit-sticky !important;
  /* max-width: 4.1rem; */
  left: 0;
  z-index: 9;
  background: white;
}
::v-deep table > thead > tr > th:nth-child(1) {
  z-index: 10;
}
::v-deep table > tbody > tr > td:nth-child(2),
::v-deep table > thead > tr > th:nth-child(2) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 5rem;
  z-index: 9;
  background: white;
}
::v-deep table > thead > tr > th:nth-child(2) {
  z-index: 10;
}
::v-deep table > tbody > tr > td:nth-child(3),
::v-deep table > thead > tr > th:nth-child(3) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left:12rem;
  z-index: 9;
  background: white;
}
::v-deep table > thead > tr > th:nth-child(3) {
  z-index: 10;
}
::v-deep table > tbody > tr > td:nth-child(4),
::v-deep table > thead > tr > th:nth-child(4) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 20rem;
  z-index: 9;
  background: white;
}
::v-deep table > thead > tr > th:nth-child(4) {
  z-index: 10;
}

::v-deep .choose-project-type_box{
  border:3px rgb(228, 228, 228) solid;
  border-radius:20px;
  padding:0.5rem;
  width: 10rem;
  font-weight: 600;
  cursor:pointer;
}

::v-deep .choose-project-type_box:hover{
  border:3px rgb(93, 158, 243) solid;
  border-radius:20px;
  padding:0.5rem;
  width: 10rem;
  cursor:pointer;
}

</style>

<style lang="scss" scoped>
#submitted-planning {
  .submitted-planning__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .submitted-planning__input {
    padding: 10px 32px;
  }

  .submitted-planning__btn {
    text-align: end;

    button {
      margin: 10px 10px;
    }
  }

  .submitted-planning__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #submitted-planning {
    .submitted-planning__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .submitted-planning__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
