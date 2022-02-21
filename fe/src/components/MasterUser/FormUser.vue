<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} User
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
        <!-- User Code -->
        <v-row no-gutters>
          <v-col cols="6"> Username<strong class="red--text">*</strong> </v-col>
          
          <v-col cols="6">
            <v-autocomplete
              :items="dataMasterEmployee"
              v-model="form.name"
              item-text="option"
              item-value="username"
              outlined
              dense
              :disabled="!isNew"
              :rules="validation.required"
              placeholder="Select Employee"
            ></v-autocomplete>
          </v-col>
        </v-row>
        <!-- Role  -->
        <v-row no-gutters>
          <v-col cols="6"> Role <strong class="red--text">*</strong> </v-col>
          <v-col cols="6">
            <v-select
              placeholder="Select Role"
              :items="type"
              v-model="form.role"
              outlined
              dense
              :disabled="isView"
              :rules="validation.typeRule"
            ></v-select>
          </v-col>
        </v-row>
        <!-- status -->
        <v-row no-gutters>
          <v-col cols="6"> Status<strong class="red--text"> *</strong> </v-col>
          <v-col cols="6">
            <v-select
              placeholder="Select status"
              :items="statusInfoMaster"
              v-model="form.status"
              item-text="label"
              item-value="id"
              outlined
              dense
              :disabled="isView"
              :rules="validation.statusRule"
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
import { mapState } from "vuex";
export default {
  name: "FormUser",
  props: ["form", "dataMasterEmployee", "isView", "isNew"],
  data: () => ({
    type: ["Admin"],
    validation: {
      required: [(v) => !!v || "This field is required"],
    },

  }),
  computed: {
    ...mapState("statusInfo", ["statusInfoMaster"]),
    ...mapState("masterEmployee", ["getMasterEmployee"]),

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
          username : this.form.name.username?this.form.name.username:this.form.name,
          role: this.form.role,
          is_active: this.form.status.id ? this.form.status.id : this.form.status ,
        };
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
        this.$refs.form.reset()
        this.form.name=""
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
