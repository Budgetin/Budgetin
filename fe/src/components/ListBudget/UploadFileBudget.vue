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
          <!-- <a href="Template Budget.xlsx" download>Download Template Budget</a> -->
          <v-btn text @click="onDownloadTemplate" class="primary--text">Download Template Budget</v-btn>
        </v-col>
      </v-row>
      <v-form ref=form lazy-validation @submit.prevent="onSubmitUpload">
        <v-row no-gutters align="center">
          <v-col cols="12" class="mt-2">
            <v-file-input
              :rules="validation.uploadRule"
              accept=".xlsx"
              show-size
              label="Upload Budget"
              v-model="files"
            ></v-file-input>
          </v-col>
        </v-row>
        <v-row no-gutters class="text-right">
          <v-col cols="12" class="mt-2">
            <v-btn rounded class="primary ml-3" type="submit">
              Submit
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
  name: "UploadFileBudget",
  created() {
  },
  data: () => ({
    name:"",
    files: [],
    validation: {
      uploadRule: [
        v => !!v || "File is required",
        v => (v && v.size > 0) || 'File is required',
      ],
    },
  }),

  computed: {
  },
  methods: {
    onDownloadTemplate() {
      this.$emit("downloadClicked");
    },
    onCancel() {
      this.$emit("cancelClicked");
    },
    onSubmitUpload() {
      let validate = this.$refs.form.validate();
      console.log(validate)
      console.log(this.files)

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
