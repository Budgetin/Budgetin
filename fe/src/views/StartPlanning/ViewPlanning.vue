<template>
    <v-app id="view-planning">
        <v-container>
            <v-row no-gutters>
                <!-- START PLANNING -->
                <form-start-planning
                    :form="form"
                    :isView="isView"
                    @editClicked="onEdit"
                    @cancelClicked="onCancel"
                    @submitClicked="onSubmit"
                    @okClicked="onOK"
                    class="view-planning__detail">
                </form-start-planning>

                <!-- LOG HISTORY -->
                <form-log-history
                    :form="form"
                    @editClicked="onEdit"
                    @cancelClicked="onCancel"
                    @submitClicked="onSubmit"
                    class="view-planning__logHistory">
                </form-log-history>
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
import FormLogHistory from '@/components/CompStartPlanning/FormLogHistory';
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
export default {
    name: "ViewPlanning",
    components: {
        FormStartPlanning, FormLogHistory, SuccessErrorAlert
    },
    created() {
        this.getEdittedItem();
    },
    watch: {},
    data: () => ({
        isView: true,

        form: {
            year: "",
            is_active: "",
            created_by: "",
            updated_by: "",
            updated_at: "",
            due_date: "",
            notification: "",
        },
        alert: {
            show: false,
            success: null,
            title: null,
            subtitle: null,
        },
    }),

    methods: {
        ...mapActions("startPlanning", [
            "patchStartPlanning",
            "getStartPlanningById",
        ]),
        getEdittedItem() {
            this.getStartPlanningById(this.$route.params.id).then(() => {
                this.setForm();
            });
        },
        setForm() {
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.startPlanning.edittedItem)
            );
        },
        onEdit() {
            this.isView = false;
            this.isNew = false;
        },
        onAdd() {
            this.dialog = !this.dialog;
        }, 
        onCancel() {
            this.isView = true;
            this.setForm();
        },
        onSubmit(e) {
            this.patchStartPlanning(e)
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
            this.isView = true;
            this.getEdittedItem();
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
    .view-planning__logHistory {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 40%;
        max-height: 600px;
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