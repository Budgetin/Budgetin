<template>
  <v-container>
    <v-row no-gutters style="margin-top: 16px">
      <v-subheader style="font-size: 1.25rem; font-weight: 600;">Budget Realization</v-subheader>
    </v-row>

    <v-row no-gutters>
      <v-col>
        <v-data-table
        :headers="dataTable.budgetRealizationHeaders"
        :loading="status"
        :items="budgetItem">
          <template v-slot:[`item.actions`]="{ item }">
            <!-- EDIT BUDGET REALIZATION -->
            <router-link
                style="text-decoration: none"
                :to="{
                    name: 'ViewMyBudgetRealization',
                    params: { id_budget_realization: item.id },
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
    name: "TableBudgetRealization",
    components: {BinaryStatusChip},
    props: ["budgetRealization"],
    data: () => ({
        isView: true,
        showItem: [],
        budgetItem: [],
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
                    Realization: {
                        id: "",
                        year: "",
                        is_active: "",
                        due_date: "",
                    },
                    budget: [
                        {
                            id: "",
                            expense_type: "",
                            Realization_q1: "",
                            Realization_q2: "",
                            Realization_q3: "",
                            Realization_q4: "",
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
                            is_active: ""
                        },
                    ],
                },
            ],
        },

        dataTable: {
            budgetRealizationHeaders: [
                { text: "Action", value: "actions", align: "center", sortable: false},
                { text: "Year", value: "year"},
                { text: "Budget Status", value: "is_active"},
                { text: "COA", value: "coa"},
                { text: "CAPEX/OPEX", value: "expense_type"},
                { text: "Allocate", value: "allocate"},
                { text: "Top Up", value: "top_up"},
                { text: "Return", value: "returns"},
                { text: "Switching In", value: "switching_in"},
                { text: "Switching Out", value: "switching_out"},
                { text: "January", value: "realization_jan"},
                { text: "February", value: "realization_feb"},
                { text: "March", value: "realization_mar"},
                { text: "April", value: "realization_apr"},
                { text: "May", value: "realization_may"},
                { text: "June", value: "realization_jun"},
                { text: "July", value: "realization_jul"},
                { text: "August", value: "realization_aug"},
                { text: "September", value: "realization_sep"},
                { text: "October", value: "realization_oct"},
                { text: "November", value: "realization_nov"},
                { text: "December", value: "realization_dec"},
            ],
        },
    }),

    mounted() {
        this.showItem = this.budgetRealization.project_detail;

        // console.log(this.showItem);
        this.budgetItem = [];
        for (let i = 0; i < this.showItem.length; i++) {
            for (let j = 0; j < this.showItem[i].budget.length; j++) {
                this.budgetItem.push(this.showItem[i].budget[j]);
            }
        }
        // console.log(this.budgetItem);
    },

    computed: {
        status: function () {
            return this.budgetRealization.project_detail ? false : true;
        },
    },
    methods: {
        onOK() {
            return this.$router.go(-1);
        },
        onEdit(item) {
          this.$store.commit("listProject/SET_EDITTED_ITEM", item);
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

#table-budget-Realization {
  .table-budget-Realization__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }
  .table-budget-Realization__detail {
    border-radius: 8px;
    margin: 1% auto !important;
    padding-right: 3% !important;
    width: 97%;
    height: 90%;
  }
  .table-budget-Realization__input {
    padding: 10px 32px;
  }
  .table-budget-Realization__btn {
    text-align: end;
    button {
      margin: 10px 32px;
    }
  }
  .table-budget-Realization__container {
    padding: 24px 0px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
    max-height: 90%;
  }
  .table-budget-Realization__outer-container {
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
  #table-budget-Realization {
    .table-budget-Realization__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .table-budget-Realization__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>