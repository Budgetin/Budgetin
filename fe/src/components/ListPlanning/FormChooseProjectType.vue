<template>
  <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
    <v-card>
      <v-card-title>
        Pick Project Type
        <v-spacer></v-spacer>
        <v-btn icon small @click="onCancel">
          <v-icon color="primary"> mdi-close </v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-row no-gutters>
          <v-col cols="12" align="center" style="font-size:20px;">
            <v-btn-toggle
            v-model="chosenProjectType"
            rounded
            mandatory
            light
            color="deep-purple accent-3"
            >
          <v-btn v-for="pt in dataProjectType" :key="pt.name" :value="pt.name">
            {{pt.name}}
          </v-btn>
        </v-btn-toggle>
          </v-col>
        </v-row>

        <v-col cols="12" align="center" class="mt-2">
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
    ...mapState("projectType", ["loadingGetListPlanning",
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
      console.log(this.dataProjectType);
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
