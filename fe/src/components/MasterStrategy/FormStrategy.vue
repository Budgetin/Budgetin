<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} Strategy
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
        <!-- Strategy Name -->
        <v-row no-gutters>
          <v-col cols="6">Strategy Name<strong class="red--text">*</strong> </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="form.name"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <!-- BUTTONS -->
        <v-row no-gutters>
          <v-col cols="12" align="right">
            <v-btn
              rounded
              outlined
              class="primary--text"
              @click="$emit('okClicked')"
              v-if="isView"
            >
              OK
            </v-btn>
            <v-btn
              rounded
              outlined
              class="primary--text"
              @click="$emit('cancelClicked')"
              v-if="!isView"
            >
              Cancel
            </v-btn>
            <v-btn rounded class="primary ml-3" type="submit" v-if="!isView">
              Save
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "FormStrategy",
  props: ["form","dataMasterStrategy", "isView", "isNew"],
  data: () => ({
    validation: {
      required: [
        (v) => !!v || "This field is required"
      ],
    },
  }),
  computed: {
    cardTitle() {
      console.log(this.form)
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
  },
  methods: {
    onSubmit() {
      let validate = this.$refs.form.validate();
      if (validate) {
        const payload = {
          id: this.form?.id,
          name : this.form.name,
        };
        console.log(payload)
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
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
