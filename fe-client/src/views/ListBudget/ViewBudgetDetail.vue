<template>
  <v-container>
    <v-row no-gutters>
      <!-- VIEW SUBMITTED BUDGET PLANNING -->
      <form-edit-budget-planning
        :form="form"
        :isView="isView"
        :dataAllBudget="dataAllBudget"
        :dataMasterCoa="dataMasterCoa"
        @editClicked="onEdit"
        @cancelClicked="onCancel"
        @submitClicked="onSubmit"
        @okClicked="onOK"
        @deleteClicked="onDelete"
        @cancelBudgetClicked="onCancelBudget"
        @restoreClicked="onRestore"
        class="view-my-budget-planning__detail"
      >
      </form-edit-budget-planning>

      <!-- LOG HISTORY -->
      <v-col xs="12" sm="6" md="6" lg="5">
        <v-container>
          <timeline-log :items="itemsHistory" v-if="itemsHistory">
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

    <success-error-alert
      :success="delete_alert.success"
      :show="delete_alert.show"
      :title="delete_alert.title"
      :subtitle="delete_alert.subtitle"
      @okClicked="onAlertDeleteOk"
    />

    <success-error-alert
      :success="cancel_alert.success"
      :show="cancel_alert.show"
      :title="cancel_alert.title"
      :subtitle="cancel_alert.subtitle"
      @okClicked="onAlertCancelOk"
    />

    <success-error-alert
      :success="restore_alert.success"
      :show="restore_alert.show"
      :title="restore_alert.title"
      :subtitle="restore_alert.subtitle"
      @okClicked="onAlertRestoreOk"
    />
  </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import FormEditBudgetPlanning from "@/components/MyProject/FormEditBudgetPlanning";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert";
import TimelineLog from "@/components/TimelineLog";
export default {
  name: "ViewBudgetDetail",
  components: {
    FormEditBudgetPlanning,
    SuccessErrorAlert,
    TimelineLog,
  },
  data: () => ({
    projectId: "",
    myProjectData: {},
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
        },
        project: {
          id: "",
          project_name: "",
        },
      },
    },

    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
    delete_alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
    cancel_alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
    restore_alert: {
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
    ...mapState("listProject", ["dataListProject"]),
  },
  methods: {
    ...mapActions("allBudget", [
      "patchAllBudget",
      "getAllBudgetById",
      "getHistory",
      "deleteAllBudgetById",
      "cancelAllBudgetById",
      "restoreAllBudgetById",
    ]),
    ...mapActions("listProject", ["getListProjectById"]),
    ...mapActions("masterCoa", ["getMasterCoa"]),

    getDetailItem() {
      console.log(this.$route.params.id_budget_planning);
      this.getAllBudgetById(this.$route.params.id_budget_planning).then(() => {
        this.setForm();
      });
    },
    setForm() {
      this.form = JSON.parse(
        JSON.stringify(this.$store.state.allBudget.edittedItem)
      );
    },
    setBreadcrumbs() {
      let param = this.isView ? "View Budget Planning" : "Edit Budget Planning";

      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Home",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "Home",
          },
        },
        {
          text: "Submitted List",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "SubmittedList",
          },
        },
        {
          text: "View Detail",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "ViewMyPlanning",
          },
        },
        {
          text: param,
          disabled: true,
        },
      ]);
    },

    onEdit() {
      this.isView = false;
      this.setBreadcrumbs();
    },
    onDelete() {
      this.deleteAllBudgetById(this.$route.params.id_budget_planning)
        .then(() => {
          this.onDeleteSuccess();
        })
        .catch((error) => {
          this.onDeleteError(error);
        });
    },
    onCancelBudget() {
      this.cancelAllBudgetById(this.$route.params.id_budget_planning)
        .then(() => {
          this.onCancelSuccess();
        })
        .catch((error) => {
          this.onCancelError(error);
        });
    },
    onRestore() {
      this.restoreAllBudgetById(this.$route.params.id_budget_planning)
        .then(() => {
          this.onRestoreSuccess();
        })
        .catch((error) => {
          this.onRestoreError(error);
        });
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
      this.alert.subtitle = "Edit Budget Planning has been saved successfully";
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
    onAlertDeleteOk() {
      this.delete_alert.show = false;
      this.$router.go(-1);
    },
    onDeleteSuccess() {
      this.delete_alert.show = true;
      this.delete_alert.success = true;
      this.delete_alert.title = "Delete Success";
      this.delete_alert.subtitle = "Budget has been deleted";
    },
    onDeleteError(error) {
      this.delete_alert.show = true;
      this.delete_alert.success = false;
      this.delete_alert.title = "Failed to delete";
      this.delete_alert.subtitle = error;
    },
    onAlertCancelOk() {
      this.cancel_alert.show = false;
      this.$router.go(-1);
    },
    onCancelSuccess() {
      this.cancel_alert.show = true;
      this.cancel_alert.success = true;
      this.cancel_alert.title = "Cancel Success";
      this.cancel_alert.subtitle = "Budget has been cancelled";
    },
    onCancelError(error) {
      this.cancel_alert.show = true;
      this.cancel_alert.success = false;
      this.cancel_alert.title = "Failed to cancel";
      this.cancel_alert.subtitle = error;
    },
    onAlertRestoreOk() {
      this.restore_alert.show = false;
      this.$router.go(-1);
    },
    onRestoreSuccess() {
      this.restore_alert.show = true;
      this.restore_alert.success = true;
      this.restore_alert.title = "Restore Success";
      this.restore_alert.subtitle = "Budget has been restored";
    },
    onRestoreError(error) {
      this.restore_alert.show = true;
      this.restore_alert.success = false;
      this.restore_alert.title = "Failed to restore";
      this.restore_alert.subtitle = error;
    },
    onOK() {
      return this.$router.go(-1);
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
.view-my-budget-planning__header {
  padding-top: 32px;
  padding-bottom: 32px;
  padding-left: 32px;
  font-size: 1.25rem;
  font-weight: 600;
  min-width: 80%;
}
.view-my-budget-planning__detail {
  border-radius: 8px;
  margin: 1% auto !important;
  width: 50%;
  height: 90%;
}
.view-my-budget-planning__input {
  padding: 10px 32px;
}
.view-my-budget-planning__btn {
  text-align: end;
  button {
    margin: 10px 32px;
  }
}
.view-my-budget-planning__container {
  padding: 24px 0px;
  box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
  border-radius: 8px;
  max-height: 90%;
}
.view-my-budget-planning__cardText {
  flex-grow: 4;
  max-height: 90%;
  overflow-y: scroll;
}
.view-my-budget-planning__field {
  min-width: 150px;
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #view-my-budget-planning {
    .view-my-budget-planning__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .view-my-budget-planning__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
