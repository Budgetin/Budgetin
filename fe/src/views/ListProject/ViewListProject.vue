<template>
    <!-- VIEW Project List -->
    <v-container>
        <v-row no-gutters>
            <form-list-project
            :form="form"
            :isView="isView"
            :dataListProject="dataListProject"
            :dataAllBiro="dataAllBiro"
            :dataMasterProduct="dataMasterProduct"
            @logHistoryClicked="onLogHistory"
            @editClicked="onEdit"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
            @okClicked="onOK"
            class="view-list-project__detail">
            </form-list-project>
        </v-row>

        <v-row no-gutters>
            <v-card class="view-list-project__table">
                <table-project-details
                :projectDetail="projectDetail"
                v-if="projectDetail.project_detail">
                </table-project-details>
            </v-card>
        </v-row>

        <v-row no-gutters>
            <v-card class="view-list-project__table">
                <table-budget-planning
                :budgetPlanning="budgetPlanning"
                v-if="budgetPlanning.project_detail"
                :route_to="route">
                </table-budget-planning>
            </v-card>
        </v-row>

        <v-row no-gutters>
            <v-card class="view-list-project__table">
                <table-budget-realization
                :budgetRealization="budgetRealization"
                v-if="budgetRealization.project_detail">
                </table-budget-realization>
            </v-card>
        </v-row>

        <v-row no-gutters>
            <v-dialog v-model="dialog"  width="40rem">
                <timeline-log
                :items="itemsHistory"
                v-if="itemsHistory"
                @cancelClicked="onCancelHistory">
                </timeline-log>
            </v-dialog>
        </v-row>

        <success-error-alert
        :success="alert.success"
        :show="alert.show"
        :title="alert.title"
        :subtitle="alert.subtitle"
        @okClicked="onAlertOk"
        />
    </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import FormListProject from '@/components/CompListProject/FormListProject';
import TableProjectDetails from '@/components/CompListProject/TableProjectDetails';
import TableBudgetPlanning from '@/components/CompListProject/TableBudgetPlanning';
import TableBudgetRealization from '@/components/CompListProject/TableBudgetRealization';
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
import TimelineLog from "@/components/TimelineLog";
export default {
    name: "ViewListProject",
    components: {
        FormListProject, TableProjectDetails, TableBudgetPlanning, TableBudgetRealization, SuccessErrorAlert, TimelineLog
    },
    data: () => ({
        route:'ViewMyBudgetPlanning',
        dialog: false,
        isView: true,
        itemsHistory: null,
        projectDetail: [],
        budgetPlanning: [],
        budgetRealization: [],
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
                            coa: "",
                            is_active: "",
                        },
                    ]
                },
            ]
        },

        alert: {
            show: false,
            success: null,
            title: null,
            subtitle: null,
        },
    }),
    created() {
        this.getDetailItem();
        this.getHistoryItem();
        this.setBreadcrumbs();
        this.getMasterProduct();
        this.getAllBiro();
    },
    computed: {
        ...mapState("listProject", ["loadingGetListProject", "dataListProject"]),
        ...mapState("allBiro", ["loadingGetAllBiro", "dataAllBiro"]),
        ...mapState("masterProduct", ["loadingGetMasterProduct", "dataMasterProduct"]),
    },
    methods: {
        ...mapActions("listProject", ["patchListProject", "getListProjectById", "getHistoryListProject"]),
        ...mapActions("masterProduct", ["getMasterProduct"]),
        ...mapActions("allBiro", ["getAllBiro"]),

        setBreadcrumbs() {
            let param = this.isView ? "View Project" : "Edit Project Detail";
            this.$store.commit("breadcrumbs/SET_LINKS", [
                {
                    text: "Project List",
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
                this.projectDetail = JSON.parse(
                    JSON.stringify(this.$store.state.listProject.dataListProjectById)
                );
                this.budgetPlanning = JSON.parse(
                    JSON.stringify(this.$store.state.listProject.dataListProjectById)
                );
                this.budgetRealization = JSON.parse(
                    JSON.stringify(this.$store.state.listProject.dataListProjectById)
                );
                this.setForm();
            });
        },
        setForm() {
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.listProject.dataListProjectById)
            );
        },
        getHistoryItem() {
            // console.log("Masuk getHistoryItem");
            this.getHistoryListProject(this.$route.params.id).then(() => {
                this.itemsHistory = JSON.parse(
                    JSON.stringify(this.$store.state.listProject.dataHistoryListProject));
            });
        },
        onEdit() {
            this.isView = false;
            this.setBreadcrumbs();
        },
        onLogHistory() {
            this.dialog = !this.dialog;
            this.getHistoryItem();
        },
        onCancelHistory() {
            this.dialog = false;
        },
        onCancel() {
            this.isView = true;
            this.setForm();
            this.setBreadcrumbs();
        },
        onSubmit(e) {
            this.patchListProject(e)
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
            this.alert.subtitle = "Edit Project has been saved successfully";
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
            this.isView = true;
            this.getDetailItem();
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
.view-list-project__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
}
.view-list-project__detail {
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