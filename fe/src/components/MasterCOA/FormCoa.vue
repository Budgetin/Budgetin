<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} COA
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
        <a-popconfirm
          title="Are you sure delete this ?"
          ok-text="Yes"
          cancel-text="No"
          @confirm="$emit('deleteClicked')"
        >
          <v-icon color="error" v-if="!isNew"> mdi-delete </v-icon>
        </a-popconfirm>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
        <!-- COA name -->
        <v-row no-gutters>
          <v-col cols="6"> COA <strong class="red--text">*</strong> </v-col>
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
        <!-- definition -->
        <v-row no-gutters>
          <v-col cols="6">
            Definition <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="form.definition"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
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
              v-model="form.hyperion_name"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <!-- CAPEX -->
        <v-row no-gutters>
          <v-col cols="6" class="mb-5">
            <v-checkbox
              v-model="form.is_capex"
              :label="`Set This to CAPEX ?`"
              :disabled="isView"
            ></v-checkbox>
          </v-col>
        </v-row>

        <!-- Minimum Value -->
        <v-row no-gutters v-if="form.is_capex">
          <v-col cols="6"> Minimum Value </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="nominal"
              outlined
              dense
              :disabled="isView"
              suffix="IDR"
              :rules="validation.targetRule"
              placeholder="Number Only"
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
  props: ["form", "isView", "isNew"],
  data: () => ({
    validation: {
      required: [
        (v) => !!v || "This field is required"
      ],
      targetRule: [
        v => /^[0-9.,]+$/.test(v) ||"This field is numbers only",
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
    nominal:{
      // getter
      get: function() {
        if(this.form.minimum_item_origin){
          this.form.minimum_item_origin = this.form.minimum_item_origin.toString().replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '');
          this.form.minimum_item_origin = this.form.minimum_item_origin.toString().split( /(?=(?:\d{3})+(?:\.|$))/g ).join( "," );
        }
          return this.form.minimum_item_origin;
      },
      // setter
      set: function(newValue) {
        this.form.minimum_item_origin = newValue.toString().replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '');
        this.form.minimum_item_origin = this.form.minimum_item_origin.toString().split( /(?=(?:\d{3})+(?:\.|$))/g ).join( "," );
      }
    }
  },
  methods: {
    onSubmit() {
      let validate = this.$refs.form.validate();
      if (validate) {
        const payload = {
          id: this.form?.id,
          name: this.form.name,
          definition : this.form.definition,
          hyperion_name: this.form.hyperion_name,
          is_capex: this.form.is_capex ? 1 : 0 ,
          minimum_item_origin: this.nominal ? parseInt(this.form.minimum_item_origin.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0
        };
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
        this.$refs.form.reset()
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
  .FormCOA__checkbox{
    align-content:flex-start
  }
</style>
