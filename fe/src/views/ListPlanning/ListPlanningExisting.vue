<template>
  <v-container>
    <v-row no-gutters justify="space-between">
      <!-- edit form -->
      <v-col xs="12" sm="10" md="10" lg="10">
        <v-container>
          <form-planning-existing
            :form="form"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
          ></form-planning-existing>
        </v-container>
      </v-col>

      <!-- log timeline -->
      <!-- <v-col xs="12" sm="6" md="6" lg="5">
        <v-container>
          <timeline-log
            v-if="cleanHistories"
            :items="cleanHistories"
            topic="Category"
          ></timeline-log>
        </v-container>
      </v-col> -->
    </v-row>
    <!-- <pre>{{ cleanHistories }}</pre> -->
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
import FormPlanningExisting from "@/components/ListPlanning/FormPlanningExisting";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
export default {
  name: "ListPlanningExisting",
  components: {FormPlanningExisting,SuccessErrorAlert},
  created() {

  },
  methods: {
    ...mapActions("listPlanning", [
      "postNewPlanning",
    ]),
    onCancel() {
      this.$router.go(-1);
    },
    onSubmit(e) {
      this.postNewPlanning(e)
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
      this.alert.subtitle = "Budget has been saved successfully";
    },
    onSaveError(error) {
      this.alert.show = true;
      this.alert.success = false;
      this.alert.title = "Save Failed";
      this.alert.subtitle = error;
    },
    onAlertOk() {
      this.alert.show = false;
      this.$router.go(-1);
    },
  },
  data: () => ({
    isView: true,
    activePlanning: [],
    form: {
        project : "",
        project_name : "",
        project_description : "",
        biro : "",
        rcc : "",
        start_year : "",
        end_year : "",
        total_investment_value : "",
        product : "",
        is_tech : "",
        planning : "",
        project_type : "",
        dcsp_id : "",
        budget:[
            {
                coa : "",
                expense_type : "",
                planning_q1 : "",
                planning_q2 : "",
                planning_q3 : "",
                planning_q4 : ""
            },
            {
                coa : "",
                expense_type : "",
                planning_q2 : "",
                planning_q1 : "",
                planning_q3 : "",
                planning_q4 : ""
            },
        ]
    },
    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
  }),
};
</script>

<style lang="scss" scoped>
#list-planning {
  width: 80%;
  margin: 0px auto;

  .list-planning__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .list-planning__input {
    padding: 10px 32px;
  }

  .list-planning__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .list-planning__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

  .list-planning__card {
    button {
      width: 8rem;
    }
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #list-planning {
    .list-planning__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .list-planning__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>