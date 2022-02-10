<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} a Budget Realization
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="EditBudgetRealization__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- YEAR -->
          <v-col cols="4"> Year 
              <div class="EditBudgetRealization__field">
                <v-text-field
                v-model="form.project_detail.planning.year"
                outlined
                return-object
                dense
                disabled
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- COA -->
          <v-col cols="4"> COA <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-select
                v-model="form.coa"
                :items="dataMasterCoa"
                item-text="name"
                item-value="name"
                placeholder="Choose COA"
                outlined
                dense
                return-object
                :disabled="isView"
                :rules="validation.required"
                class="mr-3">
                </v-select>
              </div>
          </v-col>

          <!-- CAPEX/OPEX -->
          <v-col cols="4"> Expense Type <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-select
                v-model="form.expense_type"
                :items="expenseType"
                item-text="label"
                item-value="value"
                placeholder="Choose Expense Type"
                outlined
                dense
                return-object
                :disabled="isView"
                :rules="validation.required"
                class="mr-3">
                </v-select>
              </div>
          </v-col>
        </v-row>

        <hr>
        <br>

        <!-- ALLOCATE -->  
        <v-row no-gutters>
          <v-col cols="4"> Allocate <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="allocateNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- TOP UP -->
          <v-col cols="4"> Top Up <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="topUpNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- RETURN -->
          <v-col cols="4"> Return <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="returnNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- SWITCHING IN -->  
        <v-row no-gutters>
          <v-col cols="4"> Switching In <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="switchingInNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- SWITCHING OUT -->
          <v-col cols="4"> Switching Out <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="switchingOutNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <hr>
        <br>

        <!-- JANUARY -->
        <v-row no-gutters>
          <v-col cols="4"> January <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="janNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- FEBRUARY -->
          <v-col cols="4"> February <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="febNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- MARCH -->
          <v-col cols="4"> March <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="marNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- APRIL -->
        <v-row no-gutters>
          <v-col cols="4"> April <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="aprNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- MAY -->
          <v-col cols="4"> May <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="mayNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- JUNE -->
          <v-col cols="4"> June <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="junNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- JULY -->
        <v-row no-gutters>
          <v-col cols="4"> July <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="julNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- AUGUST -->
          <v-col cols="4"> August <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="augNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- SEPTEMBER -->
          <v-col cols="4"> September <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="sepNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- OCTOBER -->
        <v-row no-gutters>
          <v-col cols="4"> October <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="octNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- NOVEMBER -->
          <v-col cols="4"> November <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="novNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
          </v-col>

          <!-- DECEMBER -->
          <v-col cols="4"> December <strong class="red--text">*</strong>
              <div class="EditBudgetRealization__field">
                <v-text-field
                suffix="IDR"
                v-model="decNominal"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule"
                class="mr-3">
                </v-text-field>
              </div>
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
              style="min-width: 8rem;">
              OK
            </v-btn>
            <v-btn
              rounded
              outlined
              class="primary--text"
              @click="$emit('cancelClicked')"
              v-if="!isView"
              style="min-width: 8rem;">
              Cancel
            </v-btn>
            <v-btn rounded class="primary ml-3" type="submit" v-if="!isView" style="min-width: 8rem;">
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
import formatting from "@/mixins/formatting";
export default {
  name: "FormEditBudgetRealization",
  props: ["form", "isNew", "isView"],
  mixins: [formatting],

  data: () => ({
    validation: {
      required: [
        (v) => !!v || "This field is required"
      ],
      targetRule: [
        v => /^[0-9.,]+$/.test(v) || "This field is numbers only",
      ],
    },

    expenseType: [
      {label: "CAPEX", value: "CAPEX"},
      {label: "OPEX", value: "OPEX"},
    ],
  }),
  
  computed: {
    ...mapState("masterCoa", ["getMasterCoa", "dataMasterCoa"]),

    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
    allocateNominal: {
      // getter
      get: function() {
        if(this.form.allocate){
          this.form.allocate = this.numberWithDots(this.form.allocate)
          return this.form.allocate;
        }
      },
      // setter
      set: function(newValue) {
        this.form.allocate = this.numberWithDots(newValue)
      }
    },
    topUpNominal: {
      // getter
      get: function() {
        if(this.form.top_up){
          this.form.top_up = this.numberWithDots(this.form.top_up)
          return this.form.top_up;
        }
      },
      // setter
      set: function(newValue) {
        this.form.top_up = this.numberWithDots(newValue)
      }
    },
    returnNominal: {
      // getter
      get: function() {
        if(this.form.return){
          this.form.return = this.numberWithDots(this.form.return)
          return this.form.return;
        }
      },
      // setter
      set: function(newValue) {
        this.form.return = this.numberWithDots(newValue)
      }
    },
    switchingInNominal: {
      // getter
      get: function() {
        if(this.form.switching_in){
          this.form.switching_in = this.numberWithDots(this.form.switching_in)
          return this.form.switching_in;
        }
      },
      // setter
      set: function(newValue) {
        this.form.switching_in = this.numberWithDots(newValue)
      }
    },
    switchingOutNominal: {
      // getter
      get: function() {
        if(this.form.switching_out){
          this.form.switching_out = this.numberWithDots(this.form.switching_out)
          return this.form.switching_out;
        }
      },
      // setter
      set: function(newValue) {
        this.form.switching_out = this.numberWithDots(newValue)
      }
    },
    janNominal: {
      // getter
      get: function() {
        if(this.form.realization_jan){
          this.form.realization_jan = this.numberWithDots(this.form.realization_jan)
          return this.form.realization_jan;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_jan = this.numberWithDots(newValue)
      }
    },
    febNominal: {
      // getter
      get: function() {
        if(this.form.realization_feb){
          this.form.realization_feb = this.numberWithDots(this.form.realization_feb)
          return this.form.realization_feb;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_feb = this.numberWithDots(newValue)
      }
    },
    marNominal: {
      // getter
      get: function() {
        if(this.form.realization_mar){
          this.form.realization_mar = this.numberWithDots(this.form.realization_mar)
          return this.form.realization_mar;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_mar = this.numberWithDots(newValue)
      }
    },
    aprNominal: {
      // getter
      get: function() {
        if(this.form.realization_apr){
          this.form.realization_apr = this.numberWithDots(this.form.realization_apr)
          return this.form.realization_apr;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_apr = this.numberWithDots(newValue)
      }
    },
    mayNominal: {
      // getter
      get: function() {
        if(this.form.realization_may){
          this.form.realization_may = this.numberWithDots(this.form.realization_may)
          return this.form.realization_may;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_may = this.numberWithDots(newValue)
      }
    },
    junNominal: {
      // getter
      get: function() {
        if(this.form.realization_jun){
          this.form.realization_jun = this.numberWithDots(this.form.realization_jun)
          return this.form.realization_jun;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_jun = this.numberWithDots(newValue)
      }
    },
    julNominal: {
      // getter
      get: function() {
        if(this.form.realization_jul){
          this.form.realization_jul = this.numberWithDots(this.form.realization_jul)
          return this.form.realization_jul;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_jul = this.numberWithDots(newValue)
      }
    },
    augNominal: {
      // getter
      get: function() {
        if(this.form.realization_aug){
          this.form.realization_aug = this.numberWithDots(this.form.realization_aug)
          return this.form.realization_aug;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_aug = this.numberWithDots(newValue)
      }
    },
    sepNominal: {
      // getter
      get: function() {
        if(this.form.realization_sep){
          this.form.realization_sep = this.numberWithDots(this.form.realization_sep)
          return this.form.realization_sep;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_sep = this.numberWithDots(newValue)
      }
    },
    octNominal: {
      // getter
      get: function() {
        if(this.form.realization_oct){
          this.form.realization_oct = this.numberWithDots(this.form.realization_oct)
          return this.form.realization_oct;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_oct = this.numberWithDots(newValue)
      }
    },
    novNominal: {
      // getter
      get: function() {
        if(this.form.realization_nov){
          this.form.realization_nov = this.numberWithDots(this.form.realization_nov)
          return this.form.realization_nov;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_nov = this.numberWithDots(newValue)
      }
    },
    decNominal: {
      // getter
      get: function() {
        if(this.form.realization_dec){
          this.form.realization_dec = this.numberWithDots(this.form.realization_dec)
          return this.form.realization_dec;
        }
      },
      // setter
      set: function(newValue) {
        this.form.realization_dec = this.numberWithDots(newValue)
      }
    },
  },

  methods: {
    onSubmit() {
      let validate = this.$refs.form.validate();
      if (validate) {
        const payload = {
            id: this.form.id,
            coa: this.form.coa.id,
            expense_type: this.form.expense_type.value,
            allocate: this.allocateNominal ? parseInt(this.form.allocate.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            top_up: this.topUpNominal ? parseInt(this.form.top_up.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            return: this.returnNominal ? parseInt(this.form.return.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            switching_in: this.switchingInNominal ? parseInt(this.form.switching_in.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            switching_out: this.switchingOutNominal ? parseInt(this.form.switching_out.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_jan: this.janNominal ? parseInt(this.form.realization_jan.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_feb: this.febNominal ? parseInt(this.form.realization_feb.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_mar: this.marNominal ? parseInt(this.form.realization_mar.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_apr: this.aprNominal ? parseInt(this.form.realization_apr.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_may: this.mayNominal ? parseInt(this.form.realization_may.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_jun: this.junNominal ? parseInt(this.form.realization_jun.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_jul: this.julNominal ? parseInt(this.form.realization_jul.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_aug: this.augNominal ? parseInt(this.form.realization_aug.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_sep: this.sepNominal ? parseInt(this.form.realization_sep.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_oct: this.octNominal ? parseInt(this.form.realization_oct.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_nov: this.novNominal ? parseInt(this.form.realization_nov.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            realization_dec: this.decNominal ? parseInt(this.form.realization_dec.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,        
        };
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
        this.$refs.form.reset();
      }
    },
    onCancel() {
      this.dialog = false;
    },
    onOK() {
      return this.$router.go(-1);
    },
  },
}
</script>

<style scoped>
  .sendTo {
    min-width: 90%;
  }
  .emailBody {
    min-width: 90%;
  }
</style>

<style lang="scss" scoped>
  .v-card__text {
    color: unset !important;
  }
  .EditBudgetRealization__checkbox{
    align-content:flex-start
  }
  .EditBudgetRealization__form{
    width: auto;
    margin-left: 2% !important;
  }
  .EditBudgetRealization__select{
    min-width: 500px;
  }
  .EditBudgetRealization__field {
    width: 100%;
  }
  .EditBudgetRealization__btn {
    text-align: end;
    button {
      margin: 10px 32px;
      min-width: 8rem;
    }
  }
</style>
    
