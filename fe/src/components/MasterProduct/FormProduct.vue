<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} Product
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
        <!-- Product Code -->
        <v-row no-gutters>
          <v-col cols="6"> Product Code<strong class="red--text">*</strong> </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="form.product_code"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <!-- Product Name  -->
        <v-row no-gutters>
          <v-col cols="6">
            Product Name <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="form.product_name"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <!-- IT Strategy -->
        <v-row no-gutters>
          <v-col cols="6">
            IT Strategy <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="6">
            <v-select
              :items="dataMasterStrategy"
              v-model="form.strategy"
              item-text="name"
              item-value="id"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Select Strategy"
            ></v-select>
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
  name: "FormProduct",
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
          product_code : this.form.product_code,
          product_name : this.form.product_name,
          strategy : this.form.strategy,
        };
        console.log("strategy" + this.form.strategy)
        // console.log(payload)
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
