<template>
    <v-app id="view-status-monitoring">
        <v-container>
            <v-row no-gutters>
                <!-- MONITOR PLANNING -->
                <form-monitor-planning
                    :form="form"
                    :isView="true"
                    :isNew="false"
                    @editClicked="onEdit"
                    @cancelClicked="onCancel"
                    @submitClicked="onSubmit"
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
    </v-app>
</template>

<script>
import FormMonitorPlanning from '@/components/CompStartPlanning/FormMonitorPlanning';
import FormLogHistory from '@/components/CompStartPlanning/FormLogHistory';
export default {
    name: "CompStartPlanning",
    components: {
        FormMonitorPlanning, FormLogHistory
    },
    watch: {},
    data() {
        return {

        };
    },

    methods: {
        onAdd() {
            this.dialog = !this.dialog;
        },
        // onEdit(item) {
        //     this.$store.commit("masterCoa/SET_EDITTED_ITEM", item);
        // },    
        onCancel() {
            this.dialog = false;
        },
        onSubmit(e) {
            this.postStartPlanning(e)
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

    computed: {
        cardTitle() {
            return this.isNew ? "Add" : this.isView ? "View" : "Edit";
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