<template>
  <v-app id="list-planning">
    <v-container class="list-planning__container outer-container">
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-subheader class="list-planning__header">List Planning</v-subheader>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-data-table
            :items="dataListPlanning"
            :loading="loadingGetListPlanning"
            :headers="listColumn"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="3" lg="3" no-gutters>
                    <v-text-field
                      class="list-planning__input"
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Search"
                      hide-details
                    >
                    </v-text-field>
                  </v-col>

                  <v-col
                    cols="6"
                    xs="6"
                    sm="2"
                    md="1"
                    lg="1"
                    no-gutters
                    class="column__btn"
                  >
                    <v-btn class="mt-2" color="primary" @click="chooseColumn">
                      <v-icon>mdi-table-column-plus-before</v-icon>
                    </v-btn>
                  </v-col>

                  <v-col
                    cols="12"
                    xs="12"
                    sm="6"
                    md="8"
                    lg="8"
                    no-gutters
                    class="list-planning__btn"
                  >
                    <v-btn rounded color="primary"> Add Planning </v-btn>
                  </v-col>
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'EditListPlanning',
                  params: { id: item.id },
                }"
              >
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" color="primary" @click="onEdit(item)">
                      mdi-eye
                    </v-icon>
                  </template>
                  <span>View/Edit</span>
                </v-tooltip>
              </router-link>
            </template>
            <template v-slot:[`item.is_budget`]="{ item }">
                <binary-yes-no-chip :boolean="item.is_budget"> </binary-yes-no-chip>
            </template>
            <template v-slot:[`item.project_detail.project.is_tech`]="{ item }">
                <binary-yes-no-chip :boolean="item.project_detail.project.is_tech"> </binary-yes-no-chip>
            </template>
          </v-data-table>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="dialog" scrollable persistent width="37.5rem">
          <column-option
            :data="dataTable.Listheader"
            :selectedColumn="listColumn"
            @closeClicked="onClose"
          />
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
import FormPlanning from "@/components/ListPlanning/FormPlanning";
import ColumnOption from "@/components/ListPlanning/ColumnOption";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
import BinaryYesNoChip from "@/components/chips/BinaryYesNoChip";
export default {
  name: "ListPlanning",
  components: {FormPlanning,SuccessErrorAlert,ColumnOption,BinaryYesNoChip},
  watch: {},
  data: () => ({
    dialog: false,
    isEdit: false,
    search: "",
    dataTable: {
      selectedHeader: [],
      Listheader: [
        { text: "Project ID", value: "project_detail.dcsp_id", width: "7rem" },
        { text: "Project Name", value: "project_detail.project.project_name", width: "8rem" },
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
        { text: "Biro", value: "project_detail.project.biro.code", width: "5rem" },
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
          value: "planning_nominal",
          width: "9rem",
        },
        { text: "Q1", value: "planning_q1", width: "5rem" },
        { text: "Q2", value: "planning_q2", width: "5rem" },
        { text: "Q3", value: "planning_q3", width: "5rem" },
        { text: "Q4", value: "planning_q4", width: "5rem" },
        {
          text: "Strategy",
          value: "project_detail.project.product.strategy",
          width: "6rem",
        },
        { text: "Created By", value: "created_by", width: "7rem" },
        { text: "Updated At", value: "updated_at", width: "8rem" },
      ],
    },
    form: {
    id: "",
    is_budget: "",
    expense_type: "",
    planning_nominal: "",
    planning_q1: "",
    planning_q2: "",
    planning_q3: "",
    planning_q4: "",
    realization_jan: "",
    realization_feb: "",
    realization_mar: "",
    realization_apr: "",
    realization_may: "",
    realization_jun: "",
    realization_jul: "",
    realization_aug: "",
    realization_sep: "",
    realization_oct: "",
    realization_nov: "",
    realization_dec: "",
    switching_in: "",
    switching_out: "",
    top_up: "",
    returns: "",
    allocate: "",
    coa: "",
    project_detail: {
        id: "",
        dcsp_id: "",
        planning: {
            id: "",
            year: "",
            due_date: "",
            is_active: ""
        },
        project: {
            id: "",
            project_name: "",
            project_description: "",
            itfam_id: "",
            is_tech: "",
            start_year: "",
            end_year: "",
            total_investment_value: "",
            product: {
                id: "",
                product_code: "",
                strategy: ""
            },
            biro: {
                id: "",
                code: "",
                name: "",
                rcc: ""
            }
        },
        project_type: ""
    },
    created_by: "",
    updated_by: "",
    created_at: "",
    updated_at: ""
},
    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
  }),
  created() {
    this.getListPlanning();
    this.getSelectedHeader();
    this.setBreadcrumbs();
  },
  computed: {
    ...mapState("listPlanning", ["loadingGetListPlanning", "dataListPlanning"]),
    ...mapState("choosedColumn", ["listColumn"]),
  },
  methods: {
    ...mapActions("listPlanning", ["getListPlanning", "postListPlanning"]),
    getSelectedHeader() {
      if (this.listColumn.length == 2) {
        this.dataTable.selectedHeader = [].concat(this.dataTable.Listheader);
        this.dataTable.selectedHeader.splice(0, 0, {
          text: "Actions",
          value: "actions",
          align: "center",
          sortable: false,
          width: "4.55rem",
        });
        this.dataTable.selectedHeader.splice(1, 0, {
          text: "For",
          value: "project_detail.planning.year",
          width: "5rem",
        });
        this.setColumn(this.dataTable.selectedHeader);
      }
    },
    setBreadcrumbs() {
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "List Planning",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "ListPlanning",
          },
        }
      ]);
    },
    setColumn(list) {
      this.$store.commit("choosedColumn/SET_LIST", list);
    },
    chooseColumn() {
      //this.dataTable.selectedHeader.splice(0, 2);
      this.dialog = !this.dialog;
    },
    onEdit(item) {
      this.$store.commit("listPlanning/SET_EDITTED_ITEM", item);
    },
    onCancel() {
      this.dialog = false;
    },
    onClose(e) {
      this.dataTable.selectedHeader.splice(0, 2);
      this.dialog = false;
      if (e.length > 0) {
        this.dataTable.selectedHeader = [];
        for (let i = 0; i < e.length; i++) {
          this.dataTable.selectedHeader.push(e[i]);
        }
        this.dataTable.selectedHeader.splice(0, 0, {
          text: "Actions",
          value: "actions",
          align: "center",
          sortable: false,
          width: "4.55rem",
        });
        this.dataTable.selectedHeader.splice(1, 0, {
          text: "For",
          value: "project_detail.planning.year",
          width: "5rem",
        });
        this.setColumn(this.dataTable.selectedHeader);
      }
    },
    onSubmit(e) {
      this.postListPlanning(e)
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.onSaveError(error);
        });
    },
    onSaveSuccess() {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Save Success";
      this.alert.subtitle = "List Source has been saved successfully";
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
  },
};
</script>

<style>
button {
  min-width: 2rem;
}

table > tbody > tr > td:nth-child(1),
table > thead > tr > th:nth-child(1) {
  position: sticky !important;
  position: -webkit-sticky !important;
  /* max-width: 4.1rem; */
  left: 0;
  z-index: 9;
  background: white;
}
table > thead > tr > th:nth-child(1) {
  z-index: 10;
}
table > tbody > tr > td:nth-child(2),
table > thead > tr > th:nth-child(2) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 4.55rem;
  z-index: 9;
  background: white;
}
table > thead > tr > th:nth-child(2) {
  z-index: 10;
}
table > tbody > tr > td:nth-child(3),
table > thead > tr > th:nth-child(3) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 9.55rem;
  z-index: 9;
  background: white;
}
table > thead > tr > th:nth-child(3) {
  z-index: 10;
}
table > tbody > tr > td:nth-child(4),
table > thead > tr > th:nth-child(4) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 16.55rem;
  z-index: 9;
  background: white;
}
table > thead > tr > th:nth-child(4) {
  z-index: 10;
}
</style>

<style lang="scss" scoped>
#list-planning {
  .list-planning__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .list-planning__input {
    padding: 10px 32px;
  }

  .list-planning__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .list-planning__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #list-planning {
    .list-planning__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .list-planning__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
