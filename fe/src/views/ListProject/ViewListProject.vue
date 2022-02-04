<template>
    <v-app id="view-list-project">
        <!-- VIEW LIST PROJECT -->
        <v-container>
            <v-row no-gutters>
                <form-list-project
                :form="form"
                :isView="isView"
                :dataListProject="dataListProject"
                @okClicked="onOK"
                class="view-list-project__form">
                </form-list-project>
            </v-row>

            <v-card class="view-list-project__table">
                <table-project-details
                :projectDetail="projectDetail"
                v-if="projectDetail.project_detail">
                </table-project-details>
            </v-card>

            <v-card class="view-list-project__table">
                <table-budget-planning>
                </table-budget-planning>
            </v-card>
        </v-container>

        <!-- PROJECT DETAILS -->
        <!-- <v-container class="view-list-project__outer-container">
            <v-row no-gutters style="margin-top: 16px">
                <v-subheader class="view-list-project__header">Project Details</v-subheader>
            </v-row>

            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <v-data-table
                    :headers="dataTable.projectDetailsHeaders"
                    :loading="loadingGetListPlanning"
                    :items="dataListPlanning"
                    class="data-table">
                    </v-data-table>
                </v-col>
            </v-row>
        </v-container> -->

        <!-- BUDGET PLANNING -->
        <!-- <v-container class="view-list-project__outer-container">
            <v-row no-gutters style="margin-top: 16px">
                <v-subheader class="view-list-project__header">Budget Planning</v-subheader>
            </v-row>

            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <v-data-table
                    :headers="dataTable.budgetPlanningHeaders"
                    :loading="loadingGetListPlanning"
                    :items="dataListPlanning"
                    class="data-table">
                    </v-data-table>
                </v-col>
            </v-row>
        </v-container> -->

        <!-- BUDGET REALIZATION -->
        <!-- <v-container class="view-list-project__outer-container">
            <v-row no-gutters style="margin-top: 16px">
                <v-subheader class="view-list-project__header">Budget Realization</v-subheader>
            </v-row>

            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <v-data-table
                    :headers="dataTable.budgetRealizationHeaders"
                    :loading="loadingGetListPlanning"
                    :items="dataListPlanning"
                    class="data-table">
                    </v-data-table>
                </v-col>
            </v-row>
        </v-container> -->
    </v-app>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import FormListProject from '@/components/CompListProject/FormListProject';
import TableProjectDetails from '@/components/CompListProject/TableProjectDetails';
import TableBudgetPlanning from '@/components/CompListProject/TableBudgetPlanning';
export default {
    name: "ViewListProject",
    components: {
        FormListProject, TableProjectDetails, TableBudgetPlanning
    },
    data: () => ({
        isView: true,
        projectDetail: [],
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

        // dataTable: {
        //     budgetRealizationHeaders: [
        //         { text: "Year", value: "project_detail.planning.year", width: "10%" },
        //         { text: "Allocate", value: "allocate", width: "15%", align: "start" },
        //         { text: "Top Up", value: "top_up", width: "15%" },
        //         { text: "Return", value: "returns", width: "15%" },
        //         { text: "Switching In", value: "switching_in", width: "15%" },
        //         { text: "Switching Out", value: "switching_out", width: "15%" },
        //         { text: "January", value: "realization_jan", width: "15%" },
        //         { text: "February", value: "realization_feb", width: "15%" },
        //         { text: "March", value: "realization_mar", width: "15%" },
        //         { text: "April", value: "realization_apr", width: "15%" },
        //         { text: "May", value: "realization_may", width: "15%" },
        //         { text: "June", value: "realization_jun", width: "15%" },
        //         { text: "July", value: "realization_jul", width: "15%" },
        //         { text: "August", value: "realization_aug", width: "15%" },
        //         { text: "September", value: "realization_sep", width: "15%" },
        //         { text: "October", value: "realization_oct", width: "15%" },
        //         { text: "November", value: "realization_nov", width: "15%" },
        //         { text: "December", value: "realization_dec", width: "15%" },
        //     ],
        // },
    }),

    created() {
        this.getDetailItem();
        this.setBreadcrumbs();
    },

    computed: {
        ...mapState("listProject", ["loadingGetListProject", "dataListProject"]),
    },

    methods: {
        ...mapActions("listProject", ["getListProjectById"]),

        setBreadcrumbs() {
            let param = this.isView ? "View Detail Project" : "Edit Project";
            this.$store.commit("breadcrumbs/SET_LINKS", [
                {
                    text: "List of Projects",
                    link: true,
                    exact: true,
                    disabled: false,
                    to: {
                        name: "ListProject",
                    },
                },
                {
                    text: param,
                    disabled: true,
                },
            ]);
        },

        getDetailItem() {
            this.getListProjectById(this.$route.params.id).then(() => {
                // console.log(this.$route.params.id);
                
                this.projectDetail = JSON.parse(
                    JSON.stringify(this.$store.state.listProject.edittedItem)
                );
                this.setForm();
            });
        },

        // getEdittedItem() {
        //     this.getListProjectById(this.$route.params.id).then(() => {
        //         this.setForm();
        //     });
        // },
        setForm() {
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.listProject.edittedItem)
            );
            console.log(this.projectDetail)
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

#view-list-project {
    .view-list-project__header {
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
    }
    .view-list-project__form {
        border-radius: 8px;
        margin: 1% auto !important;
        padding-right: 3% !important;
        width: 97%;
    }
    .view-list-project__table {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 97%;
    }
    .view-list-project__input {
        padding: 10px 32px;
    }
    .view-list-project__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
    .view-list-project__container {
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
        max-height: 90%;
    }
    .view-list-project__outer-container {
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
#view-list-project {
    .view-list-project__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .view-list-project__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>
