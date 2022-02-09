<template>
  <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
    <v-card>

      <v-card-title>
        Plan for...
        <v-spacer></v-spacer>
        <v-btn icon small @click="onCancel">
          <v-icon color="primary"> mdi-close </v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-row no-gutters align="center">
          <v-col cols="12" class="mt-2" align="center">
            <img :src="require('../../assets/account.png')" width="200rem" />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-text>
        <v-row no-gutters align="center">
          <v-col cols="6" class="mt-2">
            <v-btn rounded color="primary" @click="onNewClick"> New Project </v-btn>
          </v-col>
          <v-col cols="6" class="mt-2">
            <v-btn rounded color="primary" @click="onExistingClick"> Existing Project </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-form>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
export default {
  name: "FormChooseProjectType",
  created() {
    //this.getAllProjectType();
  },
  data: () => ({}),
  computed: {
    // ...mapState("projectType", ["loadingGetListPlanning",
    //   "dataProjectType"
    // ]),
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
  },
  methods: {
    // ...mapActions("projectType", [
    //   "getAllProjectType"
    // ]),
    onNewClick(){
      this.$emit("newClicked");
    },
    onExistingClick() {
      this.$emit("existingClicked");
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
