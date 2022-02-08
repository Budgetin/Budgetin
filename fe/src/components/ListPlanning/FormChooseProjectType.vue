<template>
  <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
    <v-card>
      <v-card-title class="mb-5">
        Add New Planning
        <v-spacer></v-spacer>
        <v-btn icon small @click="onCancel">
          <v-icon color="primary"> mdi-close </v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Judul -->
        <v-row no-gutters>
          <v-col cols="12" style="font-size:20px;">
            <strong> Pick Project Type </strong>
          </v-col>
        </v-row>

        <v-btn-toggle
          v-model="chosenProjectType"
          color="deep-purple accent-3"
          group
          >
          <v-btn v-for="pt in dataProjectType" :key="pt.name" :value="pt.name">
            {{pt.name}}
          </v-btn>
        </v-btn-toggle>

        
        <v-col cols="12" style="text-align:right;">
            <v-btn rounded color="primary" @click="onNextClick"> Next </v-btn>
          </v-col>
      </v-card-text>
    </v-card>

  </v-form>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
export default {
  name: "FormChooseProjectType",
  created() {
    this.getAllProjectType();
  },
  data: () => ({
    chosenProjectType: ""
  }),
  computed: {
    ...mapState("projectType", [
      "dataProjectType"
    ]),
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
  },
  methods: {
    ...mapActions("projectType", [
      "getAllProjectType"
    ]),
    onNextClick() {
      if(this.chosenProjectType == "Carry Forward" || this.chosenProjectType == "Regular"){
        this.$emit("existingClicked");
      }else{
        this.$emit("newClicked");
      }
    },
    onCancel(){
      this.$emit("cancelClicked");
    }
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
  .FormPlanning__checkbox{
    align-content:flex-start
  }
</style>
