<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} Planning
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
      <v-btn v-if="!isNew" icon small @click="$emit('deleteClicked')">
        <v-icon color="error"> mdi-delete </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
        <!-- Judul -->
        <v-row no-gutters>
          <v-col cols="12" style="font-size:16px">
            <strong> Project Detail </strong>
          </v-col>
        </v-row>

        <br>
        <!-- Nama nama -->
        <v-row no-gutters>
          <v-col cols="4">
            For <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="4">
            Project ID <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="4">
            Project Type <strong class="red--text">*</strong>
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters>
          <v-col cols="4">
            <v-text-field
              v-model="form.project_detail.planning.year"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="4"> 
            <v-text-field
              v-model="form.project_detail.dcsp_id"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="4">
            <v-text-field
              v-model="form.project_detail.project_type"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <hr>
        <br>

        <v-row no-gutters>
          <v-col cols="12" style="font-size:16px">
            <strong> Project </strong>
          </v-col>
        </v-row>

        <br>
        <!-- Project Name -->
        <v-row no-gutters>
          <v-col cols="12">
            Project Name <strong class="red--text">*</strong>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col cols="12">
            <v-text-field
              v-model="form.project_detail.project.project_name"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <!-- Project Description -->
        <v-row no-gutters>
          <v-col cols="12">
            Project Description <strong class="red--text">*</strong>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col cols="12">
            <v-textarea
              v-model="form.project_detail.project.project_description"
              outlined
              dense
              rows=4
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-textarea>
          </v-col>
        </v-row>

        <!-- Nama nama -->
        <v-row no-gutters>
          <v-col cols="3">
            ID-ITFAM
          </v-col>
          <v-col cols="3">
            Start Year <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="3">
            End Year
          </v-col>
          <v-col cols="3">
            Total Investment Value <strong class="red--text">*</strong>
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters >
          <v-col cols="3">
            <v-text-field
              v-model="form.project_detail.dcsp_id"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3"> 
            <v-text-field
              v-model="form.project_detail.project.start_year"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3">
            <v-text-field
              v-model="form.project_detail.project.end_year"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3">
            <v-text-field
              v-model="form.project_detail.project.total_investment_value"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <!-- Nama nama -->
        <v-row no-gutters>
          <v-col cols="3">
            Tech/Non-Tech <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="3">
            Product 
          </v-col>
          <v-col cols="3">
            Biro <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="3">
            RCC
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters >
          <v-col cols="3">
            <v-text-field
              v-model="form.project_detail.project.is_tech"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3"> 
            <v-text-field
              v-model="form.project_detail.project.product.product_code"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3">
            <v-text-field
              v-model="form.project_detail.project.biro.code"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3">
            <v-text-field
              v-model="form.project_detail.project.biro.rcc"
              outlined
              dense
              :disabled="isView"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <hr>
        <br>

        <v-row no-gutters>
          <v-col cols="12" style="font-size:16px">
            <strong> Budget </strong>
          </v-col>
        </v-row>

        <br>

        <!-- Nama nama -->
        <v-row no-gutters>
          <v-col cols="3">
            COA <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="3">
            CAPEX/OPEX
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters >
          <v-col cols="3">
            <v-text-field
              v-model="form.coa"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3"> 
            <v-text-field
              v-model="form.expense_type"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <!-- Nama nama -->
        <v-row no-gutters>
          <v-col cols="3">
            Q1
          </v-col>
          <v-col cols="3">
            Q2
          </v-col>
          <v-col cols="3">
            Q3
          </v-col>
          <v-col cols="3">
            Q4
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters >
          <v-col cols="3">
            <v-text-field
              v-model="form.planning_q1"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3"> 
            <v-text-field
              v-model="form.planning_q2"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3">
            <v-text-field
              v-model="form.planning_q3"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
              class="mr-2"
            >
            </v-text-field>
          </v-col>
          <v-col cols="3">
            <v-text-field
              v-model="form.planning_q4"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <v-row no-gutters>
          <v-col cols="3">
            
          </v-col>
          <v-col cols="3">
            
          </v-col>
          <v-col cols="3">
            
          </v-col>
          <v-col cols="3">
            Total
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters >
          <v-col cols="3">
            
          </v-col>
          <v-col cols="3"> 
            
          </v-col>
          <v-col cols="3">
            
          </v-col>
          <v-col cols="3">
            <v-text-field
              v-model="form.planning_nominal"
              outlined
              dense
              :disabled="isView"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <!-- CAPEX -->
        <!-- <v-row no-gutters>
          <v-col cols="6" class="mb-5">
            <v-checkbox
              v-model="form.is_capex"
              :label="`Set This to CAPEX ?`"
              :disabled="isView"
            ></v-checkbox>
          </v-col>
        </v-row> -->

        <!-- Minimum Value -->
        <!-- <v-row no-gutters v-if="form.is_capex">
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
        </v-row> -->
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
  name: "FormEditPlanning",
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
      let nominal = parseInt(this.form.minimum_item_origin.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''))
      if (validate) {
        const payload = {
          id: this.form?.id,
          name: this.form.name,
          definition : this.form.definition,
          hyperion_name: this.form.hyperion_name,
          is_capex: this.form.is_capex,
          minimum_item_origin: nominal ? nominal : 0
        };
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

<style>
  .FormPlanning__checkbox{
    align-content:flex-start
  }
</style>