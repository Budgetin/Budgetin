<template>
  <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
    <v-card>

      <v-card-title>
        Plan Budget for...
        <v-spacer></v-spacer>
        <v-btn icon small @click="onCancel">
          <v-icon color="primary"> mdi-close </v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-row >
          <v-col cols="6" class="mt-2" >
            <div class="choose-project-type_box" align="center" justify="center" @click="onNewClick">
              <img :src="require('../../assets/new_project.png')" height="80rem" style="padding:0.2rem;"/><br>
              New Project
            </div>
          </v-col>
          <v-col cols="6" class="mt-2" align="center" justify="center">
            <div class="choose-project-type_box" align="center" justify="center" @click="onExistingClick">
              <img :src="require('../../assets/existing_project.png')" height="80rem" style="padding:0.2rem;"/><br>
              Existing Project
            </div>
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
      this.$emit("cancelClicked");
    }
  },
};
</script>

<style>
.choose-project-type_box{
  border:3px rgb(228, 228, 228) solid;
  border-radius:20px;
  padding:0.5rem;
  width: 10rem;
  font-weight: 600;
  cursor:pointer;
}

.choose-project-type_box:hover{
  border:3px rgb(93, 158, 243) solid;
  border-radius:20px;
  padding:0.5rem;
  width: 10rem;
  cursor:pointer;
}
</style>

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
