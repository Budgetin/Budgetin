<template>
  <v-container>
    <v-row no-gutters justify="space-between">
      <!-- edit form -->
      <v-col xs="12" sm="6" md="6" lg="7">
        <v-container>
          <form-Strategy
            :form="form"
            :isView="isView"
            @editClicked="onEdit"
            @deleteClicked="onDelete"
            @okClicked="onOK"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
          ></form-Strategy>
        </v-container>
      </v-col>

     <!-- log timeline -->
      <v-col xs="12" sm="6" md="6" lg="5">
        <v-container>
          <timeline-log
            :items="items"
            v-if="items"
          ></timeline-log>
        </v-container>
      </v-col>
    </v-row>
    <!-- <pre>{{ cleanHistories }}</pre> -->
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
  </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import FormStrategy from "@/components/MasterStrategy/FormStrategy";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
import TimelineLog from "@/components/TimelineLog";

export default {
  name: "EditMasterStrategy",
  components: {TimelineLog, FormStrategy,SuccessErrorAlert},
  created() {
    this.getEdittedItem();
    this.getHistoryItem();
    this.setBreadcrumbs();
  },
  methods: {
    ...mapActions("masterStrategy", ["patchMasterStrategy","getMasterStrategyById","deleteMasterStrategyById","getHistory"]),
    setBreadcrumbs() {
      let param = this.isView ? "View Strategy" : "Edit Strategy";
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Master Strategy",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "MasterStrategy",
          },
        },
        {
          text: param,
          disabled: true,
        },
      ]);
    },
    getEdittedItem() {
      this.getMasterStrategyById(this.$route.params.id).then(() => {
        this.setForm();
      });
    },
    getHistoryItem() {
      this.getHistory(this.$route.params.id).then(() => {
        this.items = JSON.parse(
        JSON.stringify(this.$store.state.masterStrategy.dataHistoryMasterStrategy))
      });
    },
    setForm() {
      this.form = JSON.parse(
        JSON.stringify(this.$store.state.masterStrategy.dataMasterStrategyById)
      );
    },
    onEdit() {
      this.isView = false;
      this.setBreadcrumbs();
    },
    onDelete(){
      this.deleteMasterStrategyById(this.$route.params.id)
        .then(() => {
          this.onDeleteSuccess();
        })
        .catch((error) => {
          this.onDeleteError(error);
        });
    },
    onOK() {
      this.$router.go(-1);
    },
    onCancel() {
      this.isView = true;
      this.setForm();
      this.setBreadcrumbs();
    },
    onSubmit(e) {
      this.patchMasterStrategy(e)
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.onSaveError(error);
        });
    },
    onSaveSuccess() {
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Save Success";
      this.alert.subtitle = "Master Strategy has been saved successfully";
    },
    onSaveError(error) {
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
    onAlertDeleteOk() {
      this.delete_alert.show = false;
      this.$router.go(-1);
    },
    onDeleteSuccess() {
      this.delete_alert.show = true;
      this.delete_alert.success = true;
      this.delete_alert.title = "Save Success";
      this.delete_alert.subtitle = "Master Coa has been saved deleted";
    },
    onDeleteError(error) {
      this.delete_alert.show = true;
      this.delete_alert.success = false;
      this.delete_alert.title = "Failed to Delete";
      this.delete_alert.subtitle = error;
    },
  },
  data: () => ({
    isView: true,
    items:null,
    form: {
      id: "",
      name:""
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
  }),
};
</script>

<style lang="scss" scoped>
#master-Strategy {
  width: 80%;
  margin: 0px auto;

  .master-Strategy__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .master-Strategy__input {
    padding: 10px 32px;
  }

  .master-Strategy__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .master-Strategy__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

  .master-Strategy__card {
    button {
      width: 8rem;
    }
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #master-Strategy {
    .master-Strategy__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .master-Strategy__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>