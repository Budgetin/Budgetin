<template>
  <v-container>
    <v-row no-gutters justify="space-between">
      <!-- edit form -->
      <v-col xs="12" sm="6" md="6" lg="7">
        <v-container>
          <form-User
            :form="form"
            :isView="isView"
            :dataEmployee="dataEmployee"
            @editClicked="onEdit"
            @okClicked="onOK"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
          ></form-User>
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
  </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import FormUser from "@/components/MasterUser/FormUser";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
import TimelineLog from "@/components/TimelineLog";

export default {
  name: "EditMasterUser",
  components: { TimelineLog,FormUser,SuccessErrorAlert},
  created() {
    this.getEdittedItem();
    this.getEmployee();
    this.getHistoryItem();
    this.setBreadcrumbs();
  },
  computed: {
    ...mapState("masterEmployee", ["loadingGetEmployee", "dataEmployee"]),
  },
  methods: {
    ...mapActions("masterUser", ["patchMasterUser","getMasterUserById","getHistory"]),
    ...mapActions("masterEmployee", ["getEmployee"]),
    setBreadcrumbs() {
      let param = this.isView ? "View User" : "Edit User";
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Master User",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "MasterUser",
          },
        },
        {
          text: param,
          disabled: true,
        },
      ]);
    },
    getEdittedItem() {
      this.getMasterUserById(this.$route.params.id).then(() => {
        this.setForm();
      });
    },
    getHistoryItem() {
      this.getHistory(this.$route.params.id).then(() => {
        this.items = JSON.parse(
        JSON.stringify(this.$store.state.masterUser.dataHistoryMasterUser))
      });
    },
    setForm() {
      this.form = JSON.parse(
        JSON.stringify(this.$store.state.masterUser.dataUserById)
      );
    },
    onEdit() {
      this.isView = false;
      this.setBreadcrumbs();
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
      this.patchMasterUser(e)
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
      this.alert.subtitle = "Master User has been saved successfully";
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
  },
  data: () => ({
    isView: true,
    items:null,
    form: {
      id: "",
      name: {
        username:"",
        option:""
      },
      role: "",
      status:{
        id:"",
        label:""
      },
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
#master-User {
  width: 80%;
  margin: 0px auto;

  .master-User__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .master-User__input {
    padding: 10px 32px;
  }

  .master-User__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .master-User__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

  .master-User__card {
    button {
      width: 8rem;
    }
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #master-User {
    .master-User__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .master-User__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>