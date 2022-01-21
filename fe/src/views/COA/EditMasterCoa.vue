<template>
  <v-container>
    <v-row no-gutters justify="space-between">
      <!-- edit form -->
      <v-col xs="12" sm="6" md="6" lg="7">
        <v-container>
          <form-coa
            :form="form"
            :isView="isView"
            @editClicked="onEdit"
            @okClicked="onOK"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
          ></form-coa>
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
    <!-- <success-error-alert
      :success="alert.success"
      :show="alert.show"
      :title="alert.title"
      :subtitle="alert.subtitle"
      @okClicked="onAlertOk"
    /> -->
  </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import FormCoa from "@/components/MasterCOA/FormCoa";
export default {
  name: "EditMasterCoa",
  components: { FormCoa},
  created() {
    this.getEdittedItem();
  },
  methods: {
    ...mapActions("masterCoa", [
      "patchMasterCoa",
      "getMasterCoaById",
    ]),
    ...mapActions("masterStatus", ["getMasterStatus"]),
    setBreadcrumbs() {
      let param = this.isView ? "View Source" : "Edit Source";
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Master Source",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "MasterSource",
          },
        },
        {
          text: param,
          disabled: true,
        },
      ]);
    },
    getEdittedItem() {
      this.getMasterSourceById(this.$route.params.id).then(() => {
        this.getEdittedItemHistories();
        this.setForm();
      });
    },
    setForm() {
      this.form = JSON.parse(
        JSON.stringify(this.$store.state.masterSource.edittedItem)
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
      this.setBreadcrumbs();
      this.setForm();
    },
    onSubmit(e) {
      this.patchMasterSource(e)
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
      this.alert.subtitle = "Master Source has been saved successfully";
    },
    onSaveError(error) {
      this.alert.show = true;
      this.alert.success = false;
      this.alert.title = "Save Failed";
      this.alert.subtitle = error;
    },
    onAlertOk() {
      this.alert.show = false;
      if (this.alert.success) this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped>
#master-coa {
  width: 80%;
  margin: 0px auto;

  .master-coa__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .master-coa__input {
    padding: 10px 32px;
  }

  .master-coa__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .master-coa__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

  .master-coa__card {
    button {
      width: 8rem;
    }
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #master-coa {
    .master-coa__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .master-coa__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>