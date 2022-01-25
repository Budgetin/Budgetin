<template>
    <v-app id="edit-planning">
        <v-container>
            <v-row no-gutters style="max-height: 90%;">
                <!-- START PLANNING -->
                <form-start-planning
                    :form="form"
                    :isView="false"
                    :isNew="false"
                    @editClicked="onEdit"
                    @cancelClicked="onCancel"
                    @submitClicked="onSubmit"
                    class="edit-planning__detail">
                </form-start-planning>

                <!-- LOG HISTORY -->
                <form-log-history
                    :form="form"
                    @editClicked="onEdit"
                    @cancelClicked="onCancel"
                    @submitClicked="onSubmit"
                    class="edit-planning__logHistory">
                </form-log-history>
            </v-row>
        </v-container>
    </v-app>
</template>

<script>
import FormStartPlanning from '@/components/CompStartPlanning/FormStartPlanning';
import FormLogHistory from '@/components/CompStartPlanning/FormLogHistory';
export default {
    name: "CompStartPlanning",
    components: {
        FormStartPlanning, FormLogHistory
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
            return this.$router.go(-1);
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

#edit-planning {
    .edit-planning__header {
        padding-top: 32px;
        padding-bottom: 32px;
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
        min-width: 80%;
    }
    .edit-planning__detail {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 50%;
        height: 90%;
    }
    .edit-planning__input {
        padding: 10px 32px;
    }
    .edit-planning__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
    .edit-planning__container {
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
        max-height: 90%;
    }
    .edit-planning__cardText {
        flex-grow: 4;
        max-height: 90%;
        overflow-y: scroll;
    }
    .edit-planning__logHistory {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 40%;
        max-height: 600px;
        overflow-y: scroll;
    }
    .edit-planning__field {
        min-width: 150px;
    }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#edit-planning {
    .edit-planning__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .edit-planning__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>