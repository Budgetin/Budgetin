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
            :headers="dataTable.headers"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
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
                    cols="12"
                    xs="12"
                    sm="6"
                    md="8"
                    lg="8"
                    no-gutters
                    class="list-planning__btn"
                  >
                    <v-btn rounded color="primary" @click="onAdd">
                      Add Planning
                    </v-btn>
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

          </v-data-table>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="dialog" persistent width="37.5rem">
          <form-planning
          :form="form"
          :isView="false"
          :isNew="true"
          :dataListPlanning="dataListPlanning"
          @editClicked="onEdit"
          @cancelClicked="onCancel"
          @submitClicked="onSubmit"
          ></form-planning>
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
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
export default {
  name: "ListPlanning",
  components: {FormPlanning,SuccessErrorAlert},
  watch: {},
  data: () => ({
    dialog: false,
    isEdit: false,
    search: "",
    dataTable: {
      headers: [
        { text: "For", value: "planning.year"},
        { text: "ID ITFAM", value: "project.itfam_id"},
        { text: "Project ID", value: "dcsp_id"},
        { text: "Project Name", value: "project.project_name"},
        { text: "Project Description", value: "project.project_description"},
        { text: "Tech / Non Tech", value: "project.is_tech"},
        { text: "Product ID", value: "project.product.product_code"},
        { text: "RCC", value: "project.rcc"},
        { text: "Project Type", value: "project_type"},
        { text: "Biro", value: "project.biro"},
        { text: "Is Budget", value: "project.budget.id"},
        { text: "COA", value: "project.budget.coa.name"},
        { text: "Capex/Opex", value: "project.budget.expense_type"},
        { text: "Start Year", value: "project.start_year"},
        { text: "End Year", value: "project.end_year"},
        { text: "Total Investment", value: "project.total_investment_value"},
        { text: "Budget This Year", value: ""},
        { text: "Q1", value: "project.budget.planning_q1"},
        { text: "Q2", value: "project.budget.planning_q2"},
        { text: "Q3", value: "project.budget.planning_q3"},
        { text: "Q4", value: "project.budget.planning_q4"},
        { text: "Strategy", value: "project.product.strategy.name"},
        { text: "Created By", value: "created_at"},
        { text: "Updated At", value: "updated_at"},
        { text: "Actions", value: "actions", align: "center", sortable: false },
      ]
    },
    form: {
      id: "",
      name: "",
      definition: "",
      hyperion_name: "",
      is_capex: "",
      minimum_item_origin: "",
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
    // this.setBreadcrumbs();
  },
  computed: {
    ...mapState("listPlanning", ["loadingGetListPlanning", "dataListPlanning"]),
  },
  methods: {
    ...mapActions("listPlanning", ["getListPlanning", "postListPlanning"]),
    onAdd() {
      this.dialog = !this.dialog;
    },
    onEdit(item) {
      this.$store.commit("listPlanning/SET_EDITTED_ITEM", item);
    },    
    onCancel() {
      this.dialog = false;
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
  }
}
</script>

<style>
button {
  min-width: 2rem;
}
table > tbody > tr > td:nth-child(1), 
table > thead > tr > th:nth-child(1) {
  position: sticky !important; 
  position: -webkit-sticky !important; 
  left: 0; 
  z-index: 9998;
  background: white;
}
table > thead > tr > th:nth-child(1) {
  z-index: 9999;
}
table > tbody > tr > td:nth-child(2), 
table > thead > tr > th:nth-child(2) {
  position: sticky !important; 
  position: -webkit-sticky !important; 
  left:5%; 
  z-index: 9998;
  background: white;
}
table > thead > tr > th:nth-child(2) {
  z-index: 9999;
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