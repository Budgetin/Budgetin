<template>
  <v-container>
    <v-row no-gutters justify="space-between">
      <v-col xs="12" sm="12" md="12" lg="12">
        <v-container>
          <form-budget-new
            :form="form"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
          ></form-budget-new>
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
import FormBudgetNew from "@/components/Home/FormBudgetNew";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
export default {
  name: "AddNewProjectBudget",
  components: {FormBudgetNew,SuccessErrorAlert},
  created() {
    this.setBreadcrumbs();
    this.getTaskInformationById();
  },
  methods: {
...mapActions("home", ["getTaskById","submitPlanning"]),
    setBreadcrumbs() {
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
          text: "Add New Project Budget",
          disabled: true,
        },
      ]);
    },
    getTaskInformationById() {
      let param = this.$route.params.id;
      this.getTaskById(param).then(() => {
        if(this.$store.state.home.dataTaskById.length > 1){
          return this.$router.push("/home/");
        }
        else if (!this.$store.state.home.dataTaskById.planning.is_active || this.$store.state.home.dataTaskById.monitoring_status =='Submitted') {
          return this.$router.push("/home/"+param+"/Submitted/");
        }{
        this.setForm();
        }
      });
    },
    setForm(){
        this.form.planning =  JSON.parse(
          JSON.stringify(this.$store.state.home.dataTaskById.planning));
        this.form.biro =  JSON.parse(
          JSON.stringify(this.$store.state.home.dataTaskById.biro));
    },
    onCancel() {
      this.$router.go(-1);
    },
    onSubmit(e) {
      console.log(e)
      this.submitPlanning(e)
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
      this.alert.subtitle = "Planning has been saved successfully";
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
    form: {
        itfam_id : "",
        project_name : "",
        project_description : "",
        biro : 
          {
            code: "",
            id: "",
          },
        start_year : "",
        end_year : "",
        total_investment_value : "",
        product : "",
        is_tech : "",
        planning : 
          {
            id:"",
            year:""
          },
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
#list-budget {
  width: 80%;
  margin: 0px auto;

  .list-budget__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .list-budget__input {
    padding: 10px 32px;
  }

  .list-budget__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .list-budget__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

  .list-budget__card {
    button {
      width: 8rem;
    }
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #list-budget {
    .list-budget__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .list-budget__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>