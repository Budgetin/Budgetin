<template>
  <v-card>
    <v-card-title>
      Upload File
      <v-spacer></v-spacer>
      <v-btn icon small @click="onCancel">
        <v-icon color="primary"> mdi-close </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-row no-gutters align="center">
        <v-col cols="12" class="mt-2">
          <a href="ImportTemplate.xlsx" download>Download Template Planning</a>
          <!-- <v-btn text @click="downloadTemplate" class="primary--text">Download Template Planning </v-btn> -->
        </v-col>
      </v-row>
      <v-form ref=form lazy-validation @submit.prevent="onSubmitUpload">
        <v-row no-gutters align="center">
          <v-col cols="12" class="mt-2">
            <v-file-input
              :rules="validation.uploadRule"
              accept=".xlsx"
              show-size
              label="Upload Planning"
              v-model="files"
            ></v-file-input>
          </v-col>
        </v-row>
        <v-row no-gutters class="text-right">
          <v-col cols="12" class="mt-2">
            <v-btn rounded class="primary ml-3" type="submit">
              Save
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
// import template from "@/assets/ImportTemplate.xlsx"
import { mapState, mapActions, mapGetters } from "vuex";
export default {
  name: "UploadFilePlanning",
  created() {
    //this.getAllProjectType();
  },
  data: () => ({
    name:"",
    files: [],
    validation: {
      uploadRule: [(v) => !!v || "Template is required"],
    },
  }),

  computed: {
    // ...mapState("projectType", ["loadingGetListPlanning",
    //   "dataProjectType"
    // ]),
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
  },
  methods: {
    onCancel() {
      this.$emit("cancelClicked");
    },
    onSubmitUpload() {
      let validate = this.$refs.form.validate();
      if (validate) {
        let data = {
          files: this.files,
        };
        this.$emit("uploadClicked", data);
        this.$refs.form.reset()
        this.onCancel();
      }
    },
  },
};
</script>

<style lang="scss" scopped>
.v-card__text {
  color: unset !important;
}

button {
  min-width: 8rem;
}

.v-btn--rounded {
  min-width: 8rem !important;
}
</style>

<style>
.FormPlanning__checkbox {
  align-content: flex-start;
}
</style>
