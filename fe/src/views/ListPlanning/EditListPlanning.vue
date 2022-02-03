<template>
  <v-container>
    <v-row no-gutters justify="space-between">
      <!-- edit form -->
      <v-col xs="12" sm="10" md="10" lg="10">
        <v-container>
          <form-planning
            :form="form"
            :isView="isView"
            @editClicked="onEdit"
            @okClicked="onOK"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
          ></form-planning>
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
import FormPlanning from "@/components/ListPlanning/FormPlanning";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
export default {
  name: "EditListPlanning",
  components: { FormPlanning,SuccessErrorAlert},
  created() {
    this.getEdittedItem();
  },
  methods: {
    ...mapActions("listPlanning", [
      "patchListPlanning",
      "getListPlanningById",
    ]),
    getEdittedItem() {
      this.getListPlanningById(this.$route.params.id).then(() => {
        this.setForm();
      });
    },
    setForm() {
      this.form = JSON.parse(
        JSON.stringify(this.$store.state.listPlanning.edittedItem)
      );
    },
    onEdit() {
      this.isView = false;
    },
    onOK() {
      this.$router.go(-1);
    },
    onCancel() {
      this.isView = true;
      this.setForm();
    },
    onSubmit(e) {
      this.patchListPlanning(e)
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
      this.alert.subtitle = "List Planning has been saved successfully";
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
    },
  },
  data: () => ({
    isView: true,
    form: {
    id: "",
    is_budget: "",
    expense_type: "",
    planning_nominal: "",
    planning_q1: "",
    planning_q2: "",
    planning_q3: "",
    planning_q4: "",
    realization_jan: "",
    realization_feb: "",
    realization_mar: "",
    realization_apr: "",
    realization_may: "",
    realization_jun: "",
    realization_jul: "",
    realization_aug: "",
    realization_sep: "",
    realization_oct: "",
    realization_nov: "",
    realization_dec: "",
    switching_in: "",
    switching_out: "",
    top_up: "",
    returns: "",
    allocate: "",
    coa: "",
    project_detail: {
        id: "",
        dcsp_id: "",
        planning: {
            id: "",
            year: "",
            due_date: "",
            is_active: ""
        },
        project: {
            id: "",
            project_name: "",
            project_description: "",
            itfam_id: "",
            is_tech: "",
            start_year: "",
            end_year: "",
            total_investment_value: "",
            product: {
                id: "",
                product_code: "",
                strategy: ""
            },
            biro: {
                id: "",
                code: "",
                name: "",
                rcc: ""
            }
        },
        project_type: ""
    },
    created_by: "",
    updated_by: "",
    created_at: "",
    updated_at: ""
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