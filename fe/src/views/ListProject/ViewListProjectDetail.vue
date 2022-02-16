<template>
    <v-container>
        <v-row no-gutters>
            <!-- VIEW Project List DETAIL -->
            <form-edit-project-detail
            :form="form"
            :isView="isView"
            :dataProjectDetail="dataProjectDetail"
            :dataProjectType="dataProjectType"
            @editClicked="onEdit"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
            @okClicked="onOK"
            class="view-list-project-detail__detail">
            </form-edit-project-detail>
            
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
import FormEditProjectDetail from '@/components/CompListProject/FormEditProjectDetail';
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert";
import TimelineLog from "@/components/TimelineLog";
export default {
    name: "ViewListProjectDetail",
    components: {
        FormEditProjectDetail, SuccessErrorAlert, TimelineLog
    },
    data: () => ({
        isView: true,
        itemsHistory: null,
        form: {
            created_at: "",
            created_by: "",
            dcsp_id: "",
            deleted_at: "",
            id: "",
            is_deleted: false,
            planning: {
                id: "",
                is_active: "",
                notification: "",
                created_by: "",
                updated_by: "",
                year: "",
                due_date:""
            },
            project: "",
            project_type: "",
            updated_at: "",
            updated_by: ""
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
        this.getAllProjectType();
    },
    computed: {
        ...mapState("projectDetail", ["loadingGetProjectDetail", "dataProjectDetail"]),
        ...mapState("projectType", ["dataProjectType"]),
    },
    methods: {
        ...mapActions("projectDetail", ["patchProjectDetail", "getProjectDetailById", "getHistory"]),
        ...mapActions("projectType", ["getAllProjectType"]),
        
        setBreadcrumbs() {
            let param = this.isView ? "View Project Detail" : "Edit Project Detail";
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
                    text: "View Project",
                    link: true,
                    exact: true,
                    disabled: false,
                    to: {
                        name: "ViewListProject",
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
                    JSON.stringify(this.$store.state.projectDetail.edittedItemHistories));
            });
        },
        getDetailItem() {
            this.getProjectDetailById(this.$route.params.id).then(() => { 
                this.setForm();
            });
        },
        setForm() {
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.projectDetail.edittedItem)
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
            this.patchProjectDetail(e)
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
            this.alert.subtitle = "Edit Project Detail has been saved successfully";
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
.view-list-project-detail__header {
    padding-top: 32px;
    padding-bottom: 32px;
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
    min-width: 80%;
}
.view-list-project-detail__detail {
    border-radius: 8px;
    margin: 1% auto !important;
    width: 50%;
    height: 90%;
}
.view-list-project-detail__input {
    padding: 10px 32px;
}
.view-list-project-detail__btn {
    text-align: end;
    button {
        margin: 10px 32px;
    }
}
.view-list-project-detail__container {
    padding: 24px 0px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
    max-height: 90%;
}
.view-list-project-detail__cardText {
    flex-grow: 4;
    max-height: 90%;
    overflow-y: scroll;
}
.view-list-project-detail__field {
    min-width: 150px;
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#view-list-project-detail {
    .view-list-project-detail__btn {
        text-align: center;
        padding: 0px 32px;

        button {
            width: 100%;
            margin: 0px 0px 32px 0px;
        }
    }
    .view-list-project-detail__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>