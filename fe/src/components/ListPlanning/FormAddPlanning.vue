<template>
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} Planning
      <v-spacer></v-spacer>
    </v-card-title>
  
    <v-card-text>
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
              v-model="form.planning"
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
              v-model="form.dcsp_id"
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
              v-model="form.project_type"
              outlined
              dense
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>
          </v-card-text>
        </v-card>

        <br>
        <v-card>
          <v-card-text>

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
              v-model="form.project_name"
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
              v-model="form.project_description"
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
              v-model="form.itfam_id"
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
              v-model="form.start_year"
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
              v-model="form.end_year"
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
              v-model="form.total_investment_value"
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
              v-model="form.is_tech"
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
              v-model="form.product"
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
              v-model="form.biro"
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
              v-model="rcc"
              outlined
              dense
              :disabled="isView"
              placeholder="Input Here"
            >
            </v-text-field>
          </v-col>
        </v-row>
        </v-card-text>
        </v-card>

        <br>

        <v-card>
          <v-card-text>
        <v-row no-gutters>
          <v-col cols="12" style="font-size:16px">
            <strong> Budget </strong>
          </v-col>
        </v-row>
        </v-card-text>
        </v-card>

        <br>

        <!-- List Budget -->

        <div v-for="budget in budgets" :key="budget.name">
          <v-card>
          <v-card-text>
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
              v-model="budget.coa"
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
              v-model="budget.expense_type"
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
              v-model="budget.planning_q1"
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
              v-model="budget.planning_q2"
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
              v-model="budget.planning_q3"
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
              v-model="budget.planning_q4"
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
              v-model="planning_nominal"
              outlined
              dense
              :disabled=true
              placeholder="Planning Total"
            >
            </v-text-field>
          </v-col>
        </v-row>
        </v-card-text>
        </v-card>
        <br>
        </div>

        <v-card>
          <v-card-text>
          <v-row no-gutters>
            <v-col cols="6" align="left">
              <v-btn rounded class="primary ml-3" @click="onAddNewBudget">
                Add Budget
              </v-btn>
            </v-col>
            <v-col cols="6" align="right">
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
          
          </v-card-text>
        </v-card>
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
        
      </v-form>
</template>

<script>
export default {
  name: "FormAddPlanning",
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
    budgets: []
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
      //let nominal = parseInt(this.form.minimum_item_origin.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''))
      if (validate) {
        const payload = {
            itfam_id : this.form.planning,
            project_name : this.form.project_name,
            project_description : this.form.project_description,
            biro : this.form.biro,
            start_year : this.form.start_year,
            end_year : this.form.end_year,
            total_investment_value : this.form.total_investment_value,
            product : this.form.product,
            is_tech : this.form.is_tech,
            planning : this.form.planning,
            project_type : this.form.project_type,
            dcsp_id : this.form.dcsp_id,
            budget: this.budgets
        };
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
      }
    },
    onAddNewBudget(){
      this.budgets.push({
          coa : "",
          expense_type : "",
          planning_q1 : "",
          planning_q2 : "",
          planning_q3 : "",
          planning_q4 : ""
      });
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
