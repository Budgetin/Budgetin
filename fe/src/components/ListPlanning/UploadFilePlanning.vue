<template>
  <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
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
            <a href="ImportTemplate.xlsx" download
              >Download Template Planning</a
            >
            <!-- <v-btn text @click="downloadTemplate" class="primary--text">Download Template Planning </v-btn> -->
          </v-col>
        </v-row>
        <v-row no-gutters align="center">
          <v-col cols="12" class="mt-2">
            <v-file-input show-size label="File input"></v-file-input>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-form>
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
    // item:template
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
      console.log(this.dataProjectType);
      this.$emit("cancelClicked");
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
