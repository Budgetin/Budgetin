<template>
    <v-container>
        <v-row no-gutters style="margin-top: 16px">
            <v-subheader>Budget Planning</v-subheader>
        </v-row>

        <v-row no-gutters>
            <v-col >
                <v-data-table
                :headers="dataTable.budgetPlanningHeaders"
                :loading="loadingGetListProject"
                :items="dataListProject">
                </v-data-table>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
export default {
    name: "TableBudgetPlanning",
    data: () => ({
        isView: true,
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
                name: ""
            },
            product: {
                id: "",
                product_name: "",
                product_code: "",
                strategy: ""
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
                        due_date: ""
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
                            project_detail: "",
                            coa: ""
                        },
                    ]
                },
            ]
        },

        dataTable: {
            budgetPlanningHeaders: [
                { text: "Year", value: "project_detail[0].planning.year", width: "10%" },
                { text: "Strategy", value: "project_detail[0].project.product.strategy.name", width: "25%" },
                { text: "COA", value: "coa", width: "20%" },
                { text: "CAPEX/OPEX", value: "expense_type", width: "15%" },
                { text: "Budget This Year", value: "allocate", width: "25%" },
                { text: "Q1", value: "planning_q1", width: "25%" },
                { text: "Q2", value: "planning_q2", width: "25%" },
                { text: "Q3", value: "planning_q3", width: "25%" },
                { text: "Q4", value: "planning_q4", width: "25%" },
            ],
        },
    }),

    created() {
        this.getEdittedItem();
        this.getListProjectById(this.$route.params.id);
    },

    computed: {
        ...mapState("listProject", ["loadingGetListProject", "dataListProject"]),
    },

    methods: {
        ...mapActions("listProject", ["getListProjectById"]),

        getEdittedItem() {
            this.getListProjectById(this.$route.params.id).then(() => {
                this.setForm();
            });
        },
        setForm() {
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.listProject.edittedItem)
            );
        },
        onOK() {
            return this.$router.go(-1);
        }
    }
}
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