<template>
  <v-container>
    <v-row no-gutters style="margin-top: 16px">
      <v-subheader style="font-size: 1.25rem; font-weight: 600;">Budget Planning</v-subheader>
    </v-row>

    <v-row no-gutters>
      <v-col>
        <!-- :headers="dataTable.budgetPlanningHeaders" -->
        <v-data-table
        :headers="dataTable.budgetPlanningHeaders"
        :loading="status"
        :items="budgetItem">
          <template v-slot:[`item.actions`]="{ item }">
            <!-- EDIT BUDGET PLANNING -->
            <router-link
                style="text-decoration: none"
                :to="{
                    name: route_to,
                    params: { id_budget_planning: item.id },
                }">
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

          <template v-slot:[`item.is_active`]="{ item }">
              <binary-status-chip :boolean="item.is_active"></binary-status-chip>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import BinaryStatusChip from "@/components/chips/BinaryStatusChip";
export default {
  name: "TableBudgetPlanning",
  components: {BinaryStatusChip},
  props: ["budgetPlanning","route_to"],
  data: () => ({
    isView: true,
    showItem: [],
    budgetItem: [],
    planningItem: [],
    form: {
      id: "",
      created_by: "",
      updated_by: "",
      created_at: "",
      updated_at: "",
      itfam_id: "",
      project_name: "",
      project_description: "",
      start_year: "",
      end_year: "",
      is_tech: "",
      total_investment_value: "",
      biro: {
        id: "",
        rcc: "",
        code: "",
        name: "",
      },
      product: {
        id: "",
        product_name: "",
        product_code: "",
        strategy: "",
      },
      project_detail: [
        {
          id: "",
          dcsp_id: "",
          project_type: "",
          planning: {
            id: "",
            year: "",
            is_active: "",
            due_date: "",
          },
          budget: [
            {
              id: "",
              expense_type: "",
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
              is_active: "",
            },
          ],
        },
      ],
    },

    dataTable: {
      budgetPlanningHeaders: [
        { text: "Action", value: "actions", align: "center", sortable: false },
        // { text: "ID", value: "id"},
        { text: "Year", value: "year"},
        { text: "Budget Status", value: "is_active"},
        { text: "COA", value: "coa"},
        { text: "CAPEX/OPEX", value: "expense_type"},
        { text: "Budget This Year", value: "planning_nominal"},
        { text: "Q1", value: "planning_q1"},
        { text: "Q2", value: "planning_q2"},
        { text: "Q3", value: "planning_q3"},
        { text: "Q4", value: "planning_q4"},
      ],
    },
  }),

  mounted() {
    this.showItem = this.budgetPlanning.project_detail;
    this.budgetItem = [];
    for (let i = 0; i < this.showItem.length; i++) {
        for (let j = 0; j < this.showItem[i].budget.length; j++) {
            this.budgetItem.push(this.showItem[i].budget[j]);
        }
    }

    this.planningItem = [];
    for (let i = 0; i < this.showItem.length; i++) {
        this.planningItem.push(this.showItem[i].planning);
    }
  },
  computed: {
    status: function () {
      return this.budgetPlanning.project_detail ? false : true;
    },
    // headers() {
    //   const headers = [
    //     { text: "Year", value: "year"},
    //     { text: "Budget Status", value: "is_active"},
    //     { text: "COA", value: "coa"},
    //     { text: "CAPEX/OPEX", value: "expense_type"},
    //     { text: "Budget This Year", value: "planning_nominal"},
    //     { text: "Q1", value: "planning_q1"},
    //     { text: "Q2", value: "planning_q2"},
    //     { text: "Q3", value: "planning_q3"},
    //     { text: "Q4", value: "planning_q4"},
    //   ]
    //   for(let i = 0; i < this.planningItem.length; i++) {
    //     // console.log("IS ACTIVE PLANNING");
    //     // console.log(this.planningItem[i].is_active);
    //     if(this.planningItem[i].is_active == true) {
    //       // console.log(headers.length);
    //       let j = headers.length;
    //       while(j > 0) {
    //         headers.pop();
    //         j--;
    //       }

    //       headers.push(
    //         { text: "Action", value: "actions", align: "center", sortable: false },
    //         { text: "Year", value: "year"},
    //         { text: "Budget Status", value: "is_active"},
    //         { text: "COA", value: "coa"},
    //         { text: "CAPEX/OPEX", value: "expense_type"},
    //         { text: "Budget This Year", value: "planning_nominal"},
    //         { text: "Q1", value: "planning_q1"},
    //         { text: "Q2", value: "planning_q2"},
    //         { text: "Q3", value: "planning_q3"},
    //         { text: "Q4", value: "planning_q4"},
    //       );
    //     };
    //   };

    //   return headers
    // }
  },
  methods: {
    onOK() {
      return this.$router.go(-1);
    },
    onEdit(item) {
      this.$store.commit("listProject/GET_SUCCESS_LIST_PROJECT_BY_ID", item);
    },
  },
};
</script>

<style lang="scss" scoped>
.searchBar {
  width: 400px;
}
.data-table {
  margin: 40px;
}

#table-budget-planning {
  .table-budget-planning__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }
  .table-budget-planning__detail {
    border-radius: 8px;
    margin: 1% auto !important;
    padding-right: 3% !important;
    width: 97%;
    height: 90%;
  }
  .table-budget-planning__input {
    padding: 10px 32px;
  }
  .table-budget-planning__btn {
    text-align: end;
    button {
      margin: 10px 32px;
    }
  }
  .table-budget-planning__container {
    padding: 24px 0px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
    max-height: 90%;
  }
  .table-budget-planning__outer-container {
    width: 90% !important;
    margin: 1% auto !important;
    background-color: white;
    padding: 24px 0px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
    max-height: 90%;
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #table-budget-planning {
    .table-budget-planning__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .table-budget-planning__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>