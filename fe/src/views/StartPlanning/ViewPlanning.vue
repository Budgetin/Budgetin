<template>
    <v-app id="view-planning">
        <v-container>
            <v-row no-gutters>
                <!-- VIEW PLANNING -->
                <form-start-planning
                :form="form"
                :isView="isView"
                :dataStartPlanning="dataStartPlanning"
                :dataAllBiro="dataAllBiro"
                @editClicked="onEdit"
                @cancelClicked="onCancel"
                @submitClicked="onSubmit"
                @okClicked="onOK"
                class="view-planning__detail">
                </form-start-planning>
                
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
    </v-app>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import FormStartPlanning from '@/components/CompStartPlanning/FormStartPlanning';
//import FormLogHistory from '@/components/CompStartPlanning/FormLogHistory';
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
import TimelineLog from "@/components/TimelineLog";
export default {
    name: "ViewPlanning",
    components: {
        FormStartPlanning, SuccessErrorAlert, TimelineLog
    },
    data: () => ({
        isView: true,
        itemsHistory: null,
        form: {
            id: "",
            year: "",
            is_active: {
                id: "",
                label: ""
            },
            created_by: "",
            updated_by: "",
            updated_at: "",
            due_date: "",
            notification: {
                id: "",
                label: ""   
            },
            biros: [],
            body: "",
        },
        alert: {
            show: false,
            success: null,
            title: null,
            subtitle: null,
        },
    }),

    created() {
        this.getEdittedItem();
        this.getHistoryItem();
        this.setBreadcrumbs();
    },

    computed: {
        ...mapState("startPlanning", ["loadingGetStartPlanning", "dataStartPlanning"]),
        ...mapState("allBiro", ["loadingGetAllBiro", "dataAllBiro"]),
    },

    methods: {
        ...mapActions("startPlanning", ["patchStartPlanning", "getStartPlanningById", "getHistory"]),
        
        setBreadcrumbs() {
            let param = this.isView ? "View Planning" : "Edit Planning";
            this.$store.commit("breadcrumbs/SET_LINKS", [
                {
                    text: "Start Planning",
                    link: true,
                    exact: true,
                    disabled: false,
                    to: {
                        name: "StartPlanning",
                    },
                },
                {
                    text: param,
                    disabled: true,
                },
            ]);
        },

        getHistoryItem() {
            // console.log("Masuk getHistoryItem");
            this.getHistory(this.$route.params.id).then(() => {
                // console.log("Masuk getHistory");
                this.itemsHistory = JSON.parse(
                    JSON.stringify(this.$store.state.startPlanning.edittedItemHistories));
                    // sconsole.log("Masuk JSON getHistory");
            });
        },
        getEdittedItem() {
            console.log("Masuk Editted Item");
            this.getStartPlanningById(this.$route.params.id).then(() => {
                console.log("ParamID: "+this.$route.params.id);
                this.setForm();
            });
        },
        setForm() {
            // console.log("Masuk Set Form");
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.startPlanning.edittedItem)
            );
            // console.log(this.form);
        },
        onEdit() {
            // console.log("Masuk on Edit");
            this.isView = false;
            this.setBreadcrumbs();
        },
        onCancel() {
            this.isView = true;
            this.setForm();
            this.setBreadcrumbs();
        },
        onSubmit(e) {
            console.log(e);
            this.patchStartPlanning(e)
            .then(() => {
                // console.log("Masuk Save Success");
                this.onSaveSuccess();
            })
            .catch((error) => {
                // console.log("Masuk Save Error");
                this.onSaveError(error);
            });
        },
        onSaveSuccess() {
            // console.log("Masuk Save Success LAGI");
            this.dialog = false;
            this.alert.show = true;
            this.alert.success = true;
            this.alert.title = "Save Success";
            this.alert.subtitle = "Edit Planning Data has been saved successfully";
        },
        onSaveError(error) {
            // console.log("Masuk Save Error LAGI");
            this.dialog = false;
            this.alert.show = true;
            this.alert.success = false;
            this.alert.title = "Save Failed";
            this.alert.subtitle = error;
        },
        onAlertOk() {
            this.alert.show = false;
            this.isView = true;
            this.getEdittedItem();
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

#view-planning {
    .view-planning__header {
        padding-top: 32px;
        padding-bottom: 32px;
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
        min-width: 80%;
    }
    .view-planning__detail {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 50%;
        height: 90%;
    }
    .view-planning__input {
        padding: 10px 32px;
    }
    .view-planning__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
    .view-planning__container {
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
        max-height: 90%;
    }
    .view-planning__cardText {
        flex-grow: 4;
        max-height: 90%;
        overflow-y: scroll;
    }
    .view-planning__field {
        min-width: 150px;
    }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#view-planning {
    .view-planning__btn {
        text-align: center;
        padding: 0px 32px;

        button {
            width: 100%;
            margin: 0px 0px 32px 0px;
        }
    }
    .view-planning__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>