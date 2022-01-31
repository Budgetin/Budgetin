<template>
    <v-app id="view-status-monitoring">
        <v-container>
            <v-row no-gutters>
                <!-- MONITOR PLANNING -->
                <form-monitor-planning
                :form="form"
                :isView="isView"
                :dataMonitorPlanning="dataMonitorPlanning"
                @editClicked="onEdit"
                @cancelClicked="onCancel"
                @submitClicked="onSubmit"
                @okClicked="onOK"
                class="view-status-monitoring__detail">
                </form-monitor-planning>

                <!-- LOG HISTORY -->
                <v-col xs="12" sm="6" md="6" lg="5">
                    <v-container>
                        <timeline-log
                            :items="itemsHistory"
                            v-if="itemsHistory">
                        </timeline-log>
                    </v-container>
                </v-col>

                <!-- <form-log-history
                :form="form"
                @editClicked="onEdit"
                @cancelClicked="onCancel"
                @submitClicked="onSubmit"
                class="view-status-monitoring__logHistory">
                </form-log-history> -->
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
import { mapState, mapActions, mapGetters } from "vuex";
import FormMonitorPlanning from '@/components/CompStartPlanning/FormMonitorPlanning';
// import FormLogHistory from '@/components/CompStartPlanning/FormLogHistory';
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
import TimelineLog from "@/components/TimelineLog";
export default {
    name: "ViewStatusMonitoring",
    components: {
        FormMonitorPlanning, SuccessErrorAlert, TimelineLog
    },
    data: () => ({
        isView: true,
        itemsHistory: null,
        form: {
            id: "",
            biro: {
                ithc_biro: "",
                code: "",
                sub_group_code: "",
                group_code: "",
                name: "",
            },
            monitoring_status: "",
            is_deleted: "",
            planning_id: "",
            pic_employee_id: "",
            pic_initial: "",
            pic_display_name: "",
            updated_by: "",
            updated_at: "",
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
        // this.setBreadcrumbs();
    },

    computed: {
        ...mapState("monitorPlanning", ["loadingGetMonitorPlanning", "dataMonitorPlanning"]),
        ...mapState("allBiro", ["loadingGetAllBiro", "dataAllBiro"]),
    },

    methods: {
        ...mapActions("monitorPlanning", ["patchMonitorPlanning", "getMonitorPlanningDetailById", "getHistory"]),

        setBreadcrumbs() {
            let param = this.isView ? "View Monitor Planning Status" : "Edit Monitor Planning Status";
            this.$store.commit("breadcrumbs/SET_LINKS", [
                {
                    text: "Monitor Planning Status",
                    link: true,
                    exact: true,
                    disabled: false,
                    to: {
                        name: "MonitorPlanning",
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
                    JSON.stringify(this.$store.state.monitorPlanning.edittedItemHistories));
                    // console.log("Masuk JSON getHistory");
            });
        },
        getEdittedItem() {
            // console.log("Masuk Editted Item");
            this.getMonitorPlanningDetailById(this.$route.params.id).then(() => {
                // console.log("ParamID: "+this.$route.params.id);
                this.setForm();
            });
        },
        setForm() {
            // console.log("Masuk Set Form");
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.monitorPlanning.edittedItem)
            );
            // console.log(this.form);
        },
        onAdd() {
            this.dialog = !this.dialog;
        },
        onEdit() {
            // console.log("Masuk on Edit");
            this.isView = false;
            // this.isNew = false;
            this.setBreadcrumbs();
        }, 
        onCancel() {
            this.dialog = false;
            this.setBreadcrumbs();
        },
        onSubmit(e) {
            console.log(e);
            this.patchMonitorPlanning(e)
            .then(() => {
                console.log("Masuk Save Success");
                this.onSaveSuccess();
            })
            .catch((error) => {
                console.log("Masuk Save Error");
                this.onSaveError(error);
            });
        },
        onSaveSuccess() {
            this.dialog = false;
            this.alert.show = true;
            this.alert.success = true;
            this.alert.title = "Save Success";
            this.alert.subtitle = "Monitor Planning Status Data has been saved successfully";
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

#view-status-monitoring {
    .view-status-monitoring__header {
        padding-top: 32px;
        padding-bottom: 32px;
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
        min-width: 80%;
    }
    .view-status-monitoring__detail {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 50%;
        height: 90%;
    }
    .view-status-monitoring__input {
        padding: 10px 32px;
    }
    .view-status-monitoring__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
    .view-status-monitoring__container {
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
        max-height: 90%;
    }
    .view-status-monitoring__cardText {
        flex-grow: 4;
        max-height: 90%;
        overflow-y: scroll;
    }
    .view-status-monitoring__logHistory {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 40%;
        max-height: 600px;
        overflow-y: scroll;
    }
    .view-status-monitoring__field {
        min-width: 150px;
    }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#view-status-monitoring {
    .view-status-monitoring__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .view-status-monitoring__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>