<template>
    <v-app id="view-status-monitoring">
        <v-container>
            <v-row no-gutters>
                <!-- MONITOR PLANNING -->
                <form-monitor-planning
                :form="form"
                :isView="isView"
                @editClicked="onEdit"
                @cancelClicked="onCancel"
                @submitClicked="onSubmit"
                @okClicked="onOK"
                class="view-status-monitoring__detail">
                </form-monitor-planning>

                <!-- LOG HISTORY -->
                <form-log-history
                :form="form"
                @editClicked="onEdit"
                @cancelClicked="onCancel"
                @submitClicked="onSubmit"
                class="view-status-monitoring__logHistory">
                </form-log-history>
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
import FormLogHistory from '@/components/CompStartPlanning/FormLogHistory';
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
export default {
    name: "ViewStatusMonitoring",
    components: {
        FormMonitorPlanning, FormLogHistory, SuccessErrorAlert
    },
    created() {
        this.getEdittedItem();
    },
    watch: {},
    data: () => ({
        isView: true,

        form: {
            biro: {
                ithc_biro: "",
                code: "",
                subgroup: "",
                group: "",
                pic: "",
            },
            monitoring_status_id: "",
            is_deleted: "",
            planning_id: "",
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

    methods: {
        ...mapActions("monitorPlanning", [
            "patchMonitorPlanning",
            "getMonitorPlanningById",
        ]),
        getEdittedItem() {
            this.getMonitorPlanningById(this.$route.params.id).then(() => {
                this.setForm();
            });
        },
        setForm() {
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.monitorPlanning.edittedItem)
            );
        },
        onAdd() {
            this.dialog = !this.dialog;
        },
        onEdit() {
            this.isView = false;
            this.isNew = false;
        }, 
        onCancel() {
            this.dialog = false;
        },
        onSubmit(e) {
            this.postMonitorPlanning(e)
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
            this.alert.subtitle = "Start Planning Data has been saved successfully";
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