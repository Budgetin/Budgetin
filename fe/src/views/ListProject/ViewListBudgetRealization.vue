<template>
    <v-container>
        <v-row no-gutters>
            <!-- VIEW LIST BUDGET REALIZATION -->
            <form-edit-budget-realization
            :form="form"
            :isView="isView"
            :dataAllBudget="dataAllBudget"
            :dataMasterCoa="dataMasterCoa"
            @editClicked="onEdit"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
            @okClicked="onOK"
            class="view-list-budget-realization__detail">
            </form-edit-budget-realization>
            
            <!-- LOG HISTORY -->
            <v-col xs="12" sm="6" md="6" lg="5">
                <v-container>
                    <timeline-log
                        :items="itemsHistory"
                        v-if="itemsHistory">
                    </timeline-log>
                </v-container>
            </v-col>
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
import FormEditBudgetRealization from '@/components/CompListProject/FormEditBudgetRealization';
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert";
import TimelineLog from "@/components/TimelineLog";
export default {
    name: "ViewListBudgetRealization",
    components: {
        FormEditBudgetRealization, SuccessErrorAlert, TimelineLog
    },
    data: () => ({
        isView: true,
        itemsHistory: null,
        form: {
            allocate: "",
            coa: "",
            created_at: "",
            created_by: "",
            expense_type: "",
            id: "",
            is_active: "",
            is_budget: "",
            planning_nominal: "",
            planning_q1: "",
            planning_q2: "",
            planning_q3: "",
            planning_q4: "",
            realization_apr: "",
            realization_aug: "",
            realization_dec: "",
            realization_feb: "",
            realization_jan: "",
            realization_jul: "",
            realization_jun: "",
            realization_mar: "",
            realization_may: "",
            realization_nov: "",
            realization_oct: "",
            realization_sep: "",
            returns: "",
            switching_in: "",
            switching_out: "",
            top_up: "",
            updated_at: "",
            updated_by: "",
            project_detail: {
                dcsp_id: "",
                id: "",
                planning: {
                    due_date: "",
                    id: "",
                    is_active: "",
                    year: "",
               }
            }
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
        this.getMasterCoa();
    },
    computed: {
        ...mapState("allBudget", ["loadingGetAllBudget", "dataAllBudget"]),
        ...mapState("masterCoa", ["dataMasterCoa"]),
    },
    methods: {
        ...mapActions("allBudget", ["patchAllBudget", "getAllBudgetById", "getHistory"]),
        ...mapActions("masterCoa", ["getMasterCoa"]),
        
        setBreadcrumbs() {
            let param = this.isView ? "View Budget Realization" : "Edit Budget Realization";
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
        getHistoryItem() {
            this.getHistory(this.$route.params.id).then(() => {
                this.itemsHistory = JSON.parse(
                    JSON.stringify(this.$store.state.allBudget.edittedItemHistories));
                for(let i=0; i<this.itemsHistory.length; i++) {
                    this.itemsHistory[i].table = "budgetRealization"
                    // console.log(this.itemsHistory[i]);
                }
            });
        },
        getDetailItem() {
            this.getAllBudgetById(this.$route.params.id).then(() => {
                this.setForm();
            });
        },
        setForm() {
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.allBudget.edittedItem)
            );
        },
        onEdit() {
            this.isView = false;
            this.setBreadcrumbs();
        },
        onCancel() {
            this.isView = true;
            this.setForm();
            this.setBreadcrumbs();
        },
        onSubmit(e) {
            this.patchAllBudget(e)
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
            this.alert.subtitle = "Edit Budget Realization has been saved successfully";
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
            this.getHistoryItem();
        },
        onOK() {
            return this.$router.go(-1);
        }
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
.view-list-budget-realization__header {
    padding-top: 32px;
    padding-bottom: 32px;
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
    min-width: 80%;
}
.view-list-budget-realization__detail {
    border-radius: 8px;
    margin: 1% auto !important;
    width: 50%;
    height: 90%;
}
.view-list-budget-realization__input {
    padding: 10px 32px;
}
.view-list-budget-realization__btn {
    text-align: end;
    button {
        margin: 10px 32px;
    }
}
.view-list-budget-realization__container {
    padding: 24px 0px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
    max-height: 90%;
}
.view-list-budget-realization__cardText {
    flex-grow: 4;
    max-height: 90%;
    overflow-y: scroll;
}
.view-list-budget-realization__field {
    min-width: 150px;
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#view-list-budget-realization {
    .view-list-budget-realization__btn {
        text-align: center;
        padding: 0px 32px;

        button {
            width: 100%;
            margin: 0px 0px 32px 0px;
        }
    }
    .view-list-budget-realization__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>