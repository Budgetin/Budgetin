<template>
  <v-card>
    <v-card-title class="mb-5">
      Add COA
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
        <!-- COA name -->
        <v-row no-gutters>
          <v-col cols="6"> COA <strong class="red--text">*</strong> </v-col>
          <v-col cols="6">
            <v-text-field
              outlined
              dense
              :disabled="isView"
              :rules="[validation.required]"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <!-- definition -->
        <v-row no-gutters>
          <v-col cols="6">
            Definition <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="6">
            <v-text-field
              outlined
              dense
              :disabled="isView"
              :rules="[validation.required]"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <!-- Hyperion -->
        <v-row no-gutters>
          <v-col cols="6">
            Hyperion <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="6">
            <v-text-field
              outlined
              dense
              :disabled="isView"
              :rules="[validation.required]"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <!-- Status -->
        <v-row no-gutters>
          <v-col cols="6"> Status <strong class="red--text">*</strong> </v-col>
          <v-col cols="6">
            <v-text-field
              outlined
              dense
              :disabled="isAdd"
              :rules="[validation.required]"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <!-- CAPEX -->
        <v-row no-gutters>
          <v-col cols="6" class="mb-5">
            <v-checkbox
              v-model="checkbox"
              :label="`Set This to CAPEX ?`"
            ></v-checkbox>
          </v-col>
        </v-row>

        <!-- Minimum Value -->
        <v-row no-gutters v-if="checkbox">
          <v-col cols="6"> Minimum Value </v-col>
          <v-col cols="6">
            <v-text-field
              outlined
              dense
              :disabled="isView"
              suffix="IDR"
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
  name: "FormCoa",
  props: ["isView","isAdd"],

  data: () => ({
    checkbox: false,
    validation: {
      required: (v) => !!v || "This field is required",
      // counterInitial: (v) => v.length <= 50 || "Max. 50 characters",
      // counterName: (v) => v.length <= 50 || "Max. 50 characters",
    },
  }),
};
</script>

<style lang="scss">
.v-card__text {
  color: unset !important;
}

.v-card-title {
  font-size: 1.25rem !important;
  font-weight: 600 !important;
}

button {
  min-width: 8rem;
}

.v-btn--rounded {
  min-width: 8rem !important;
}
</style>

<style>
  .FormCOA__checkbox{
    align-content:flex-start
  }
</style>
