<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} Budget Planning
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')" class="mr-3">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>

      <!-- DELETE BUDGET, CANNOT BE RESTORED -->
      <a-popconfirm
      v-if="form.is_active == true && form.project_detail.planning.is_active == true"
      title="Are you sure you want to delete this budget?"
      ok-text="Yes"
      cancel-text="No"
      @confirm="$emit('deleteClicked')"
      class="mr-2">
        <v-icon color="error" v-if="!isNew"> mdi-delete </v-icon>
      </a-popconfirm>

      <!-- CANCEL BUDGET -->
      <a-popconfirm
      v-if="form.is_active == true && form.project_detail.planning.is_active == false"
      title="Are you sure you want to cancel this budget?"
      ok-text="Yes"
      cancel-text="No"
      @confirm="$emit('cancelBudgetClicked')"
      class="mr-2">
        <a-popover>
          <template slot="content">
            <p>Cancel Budget</p>
          </template>
          <v-icon color="error" v-if="!isNew"> mdi-file-cancel-outline </v-icon>
        </a-popover>
      </a-popconfirm>

      <!-- RESTORE BUDGET THAT HAS BEEN CANCELLED -->
      <a-popconfirm
      v-if="form.is_active == false && form.project_detail.planning.is_active == false"
      title="Are you sure you want to restore this budget?"
      ok-text="Yes"
      cancel-text="No"
      @confirm="$emit('restoreClicked')"
      class="mr-2">
        <v-icon color="primary" v-if="!isNew"> mdi-file-restore-outline </v-icon>
      </a-popconfirm>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="EditBudgetPlanning__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- YEAR -->
          <v-col cols="4"> Year 
              <div class="EditBudgetPlanning__field">
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
              <div class="EditBudgetPlanning__field">
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
              <div class="EditBudgetPlanning__field">
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

        <!-- BUDGET THIS YEAR -->  
        <v-row no-gutters>
          <v-col cols="12"> Budget This Year <strong class="red--text">*</strong>
              <div class="EditBudgetPlanning__field">
                <v-text-field
                suffix="IDR"
                v-model="planningNominal"
                outlined
                dense
                disabled
                :rules="validation.targetRule">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- Q1 -->
        <v-row no-gutters>
          <v-col cols="12"> Q1 <strong class="red--text">*</strong>
              <div class="EditBudgetPlanning__field">
                <v-text-field
                suffix="IDR"
                v-model="planningQ1"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- Q2 -->
        <v-row no-gutters>
          <v-col cols="12"> Q2 <strong class="red--text">*</strong>
              <div class="EditBudgetPlanning__field">
                <v-text-field
                suffix="IDR"
                v-model="planningQ2"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- Q3 -->
        <v-row no-gutters>
          <v-col cols="12"> Q3 <strong class="red--text">*</strong>
              <div class="EditBudgetPlanning__field">
                <v-text-field
                suffix="IDR"
                v-model="planningQ3"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule">
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- Q4 -->
        <v-row no-gutters>
          <v-col cols="12"> Q4 <strong class="red--text">*</strong>
              <div class="EditBudgetPlanning__field">
                <v-text-field
                suffix="IDR"
                v-model="planningQ4"
                outlined
                dense
                :disabled="isView"
                :rules="validation.targetRule">
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
  name: "FormEditBudgetPlanning",
  props: ["form", "isNew", "isView"],
  mixins: [formatting],

  data: () => ({
    validation: {
      required: [
        (v) => !!v || "This field is required"
      ],
      targetRule: [
        v => /(^[0-9.,]+$|^$|[null])/.test(v) || "This field is numbers only",
      ],
    },

    expenseType: [
      {label: "CAPEX", value: "CAPEX"},
      {label: "OPEX", value: "OPEX"},
    ],
  }),
  
  // mounted() {
  //   this.planningItem = [];
  //   for (let i = 0; i < this.showItem.length; i++) {
  //       this.planningItem.push(this.showItem[i].planning);
  //   }
  // },
  computed: {
    ...mapState("masterCoa", ["getMasterCoa", "dataMasterCoa"]),

    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
    planningNominal: {
      // getter
      get: function() {
        if(this.form.planning_nominal){
          this.form.planning_nominal = this.numberWithDots(this.form.planning_nominal)
          return this.form.planning_nominal;
        }
      },
      // setter
      set: function(newValue) {
        this.form.planning_nominal = this.numberWithDots(newValue)
      }
    },
    planningQ1: {
      // getter
      get: function() {
        if(this.form.planning_q1){
          this.form.planning_q1 = this.numberWithDots(this.form.planning_q1)
          return this.form.planning_q1;
        }
      },
      // setter
      set: function(newValue) {
        this.form.planning_q1 = this.numberWithDots(newValue)
      }
    },
    planningQ2: {
      // getter
      get: function() {
        if(this.form.planning_q2){
          this.form.planning_q2 = this.numberWithDots(this.form.planning_q2)
          return this.form.planning_q2;
        }
      },
      // setter
      set: function(newValue) {
        this.form.planning_q2 = this.numberWithDots(newValue)
      }
    },
    planningQ3: {
      // getter
      get: function() {
        if(this.form.planning_q3){
          this.form.planning_q3 = this.numberWithDots(this.form.planning_q3)
          return this.form.planning_q3;
        }
      },
      // setter
      set: function(newValue) {
        this.form.planning_q3 = this.numberWithDots(newValue)
      }
    },
    planningQ4: {
      // getter
      get: function() {
        if(this.form.planning_q4){
          this.form.planning_q4 = this.numberWithDots(this.form.planning_q4)
          return this.form.planning_q4;
        }
      },
      // setter
      set: function(newValue) {
        this.form.planning_q4 = this.numberWithDots(newValue)
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
            planning_nominal: this.planningNominal ? parseInt(this.form.planning_nominal.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            planning_q1: this.planningQ1 ? parseInt(this.form.planning_q1.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            planning_q2: this.planningQ2 ? parseInt(this.form.planning_q2.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            planning_q3: this.planningQ3 ? parseInt(this.form.planning_q3.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
            planning_q4: this.planningQ4 ? parseInt(this.form.planning_q4.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
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
  .EditBudgetPlanning__checkbox{
    align-content:flex-start
  }
  .EditBudgetPlanning__form{
    width: auto;
    margin-left: 2% !important;
  }
  .EditBudgetPlanning__select{
    min-width: 500px;
  }
  .EditBudgetPlanning__field {
    width: 100%;
  }
  .EditBudgetPlanning__btn {
    text-align: end;
    button {
      margin: 10px 32px;
      min-width: 8rem;
    }
  }
</style>
    
