<template>
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
        <h1 style="font-weight:bold;">Create Budget Planning for Existing Project</h1>
        <v-card>
          <v-card-title>
              <strong> Project</strong>
        </v-card-title>
          <v-card-text>
        <v-divider></v-divider><br>
        <!-- Project Name -->
        <v-row no-gutters>
          <v-col cols="12">
            Project Name <strong class="red--text">*</strong>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col cols="12">
              <v-combobox
                hide-selected
                v-model="form.project"
                :items="dataMyProject"
                item-text="project_name"
                item-value="id"
                placeholder="Search Project..."
                outlined
                return-object
                :rules="validation.required"
                :dense=true
                @input="onSelectProject">
              </v-combobox>
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
              placeholder=""
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
          <v-col cols="3"> End Year </v-col>
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
              readonly
              disabled
              placeholder="-"
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
              :rules="validation.targetRule"
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
              :rules="validation.targetRule"
              placeholder="Input Here"
              suffix="IDR"
              @input="total_investment_input"
            >
            </v-text-field>
          </v-col>
        </v-row>

        <!-- Nama nama -->
        <v-row no-gutters>
          <v-col cols="3">
            Tech/Non-Tech
          </v-col>
          <v-col cols="3">
            Product 
          </v-col>
          <v-col cols="3">
            Biro
          </v-col>
          <v-col cols="3">
            RCC
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters>
          <v-col cols="3">
            <div>
              <v-select
                v-model="form.is_tech"
                :items="statusTechNonTech"
                item-text="label"
                item-value="id"
                placeholder="Choose Tech"
                outlined
                return-object
                :rules="validation.required"
                class="mr-2"
                :dense="true"
              >
              </v-select>
            </div>
          </v-col>
          <v-col cols="3">
            <div>
              <v-combobox
                hide-selected
                v-model="form.product"
                :items="dataMasterProduct"
                item-text="product_name"
                item-value="id"
                placeholder="Choose Product"
                outlined
                return-object
                class="mr-2"
                :dense="true"
              >
              </v-combobox>
            </div>
          </v-col>
          <v-col cols="3">
            <div>
              <v-select
                v-model="form.biro"
                :items="dataAllBiro"
                item-text="code"
                item-value="id"
                placeholder="Choose Biro"
                outlined
                disabled
                :rules="validation.required"
                class="mr-2"
                :dense="true"
              >
              </v-select>
            </div>
          </v-col>
          <v-col cols="3">
            <v-text-field
              v-model="getRCC"
              outlined
              dense
              :disabled="true"
              placeholder="Auto Input"
            >
            </v-text-field>
          </v-col>
        </v-row>
        </v-card-text>
        </v-card>
        <!-- List Budget -->
        <br>
        <v-card>
          <v-card-title>
              <strong> Project Detail </strong>
        </v-card-title>
          <v-card-text>
          <v-divider></v-divider><br>
          <v-row no-gutters>
            <v-col cols="4">
              For <strong class="red--text">*</strong>
            </v-col>
            <!-- <v-spacer></v-spacer> -->
            <v-col cols="4">
              Project ID
            </v-col>
            <v-col cols="4">
              Project Type <strong class="red--text">*</strong>
            </v-col>
          </v-row>

          <!-- Kolom kolom -->
          <v-row no-gutters>
            <v-col cols="4">
                <div>
                  <v-select
                    v-model="form.planning"
                    :items="dataActiveListBudget"
                    item-text="year"
                    item-value="id"
                    placeholder="Year"
                    outlined
                    return-object
                    :rules="validation.required"
                    class="mr-2"
                    :dense=true
                    @change="onSelectFor">
                  </v-select>
                </div>
              </v-col>
              
            <!-- <v-col cols="4">
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
            </v-col> -->
            <!-- <v-spacer></v-spacer> -->
            
            <v-col cols="4"> 
              <v-text-field
                v-model="form.dcsp_id"
                outlined
                dense
                :disabled="true"
                placeholder="Auto Input"
                class="mr-2"
              >
              </v-text-field>
            </v-col>
            <v-col cols="4">
                <div>
                  <v-select
                    v-model="form.project_type"
                    :items="listProjectType"
                    item-text="name"
                    item-value="id"
                    placeholder="Type"
                    outlined
                    return-object
                    :rules="validation.required"
                    :dense=true
                    :disabled="!projectTypeEnable">
                  </v-select>
                </div>
              </v-col>
          </v-row>
          </v-card-text>
        </v-card>


        <div v-if="budget_table.length > 0">
        <br>
        <v-card>
          <v-card-title>
            Budget List
          </v-card-title>
          <v-card-text>
            <v-data-table
            :headers="dataTable.budgetPlanningHeaders"
            :loading="status"
            :items="budget_table">
              <template v-slot:[`item.actions`]="{ item }">
                <!-- EDIT BUDGET PLANNING -->
                <router-link
                    style="text-decoration: none"
                    :to="{
                      name: 'ViewMyBudgetPlanning',
                      params: { 
                                id: form.project.id,
                                id_budget_planning: item.id
                              },
                    }">
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                            <v-icon v-on="on" color="primary">
                                mdi-eye
                            </v-icon>
                        </template>
                        <span>View/Edit</span>
                    </v-tooltip>
                </router-link>
              </template>

            </v-data-table>
          </v-card-text>
        </v-card>
        </div>

        <div v-for="(budget, index) in budgets" :key="budget.name">
      <br />
      <v-card>
        <v-card-title>
          <strong> Budget {{ "#" + (index + 1) }}</strong>
          <v-spacer></v-spacer>
          <v-btn icon small @click="popBudgetByIndex(index)">
            <v-icon color="primary"> mdi-close </v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-divider></v-divider><br />

          <!-- Nama nama -->
          <v-row no-gutters>
            <v-col cols="9"> COA <strong class="red--text">*</strong> </v-col>
            <v-col cols="3"> Expense Type </v-col>
          </v-row>

          <!-- Kolom kolom -->
          <v-row no-gutters>
            <v-col cols="9">
              <div>
                <v-combobox
                  hide-selected
                  v-model="budget.coa"
                  :items="dataMasterCoa"
                  item-text="name"
                  item-value="id"
                  placeholder="Select"
                  outlined
                  return-object
                  :rules="validation.required"
                  class="mr-2"
                  :dense="true"
                  @input="onInput(budget)"
                >
                <template v-slot:item="{ item, attrs, on }">
                  <v-list-item v-on="on" v-bind="attrs">
                    <v-list-item-content>
                      <v-list-item-title>
                        <v-row no-gutters align="center">
                        <span>{{ item.name }}</span>
                        <v-spacer></v-spacer>
                        <span style="opacity:0.7">{{ item.definition }}</span>
                        </v-row>
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>

                </v-combobox>
              </div>
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="budget.expense_type"
                outlined
                dense
                :disabled="true"
                placeholder="Auto Input"
              >
              </v-text-field>
            </v-col>
          </v-row>

          <!-- Nama nama -->
          <v-row no-gutters>
            <v-col cols="3"> Q1 </v-col>
            <v-col cols="3"> Q2 </v-col>
            <v-col cols="3"> Q3 </v-col>
            <v-col cols="3"> Q4 </v-col>
          </v-row>

          <!-- Kolom kolom -->
          <v-row no-gutters>
            <v-col cols="3">
              <v-text-field
                v-model="budget.planning_q1"
                outlined
                dense
                :disabled="isView"
                suffix="IDR"
                :rules="validation.targetRule"
                placeholder="Plan for Q1"
                class="mr-2"
                @input="onInput(budget)"
              >
              </v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="budget.planning_q2"
                outlined
                dense
                :disabled="isView"
                suffix="IDR"
                :rules="validation.targetRule"
                placeholder="Plan for Q2"
                class="mr-2"
                @input="onInput(budget)"
              >
              </v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="budget.planning_q3"
                outlined
                dense
                :disabled="isView"
                suffix="IDR"
                :rules="validation.targetRule"
                placeholder="Plan for Q3"
                class="mr-2"
                @input="onInput(budget)"
              >
              </v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="budget.planning_q4"
                outlined
                dense
                :disabled="isView"
                suffix="IDR"
                :rules="validation.targetRule"
                placeholder="Plan for Q4"
                @input="onInput(budget)"
              >
              </v-text-field>
            </v-col>
          </v-row>

          <v-row no-gutters>
            <v-col cols="3"> </v-col>
            <v-col cols="3"> </v-col>
            <v-col cols="3"> </v-col>
            <v-col cols="3"> Total </v-col>
          </v-row>

          <!-- Kolom kolom -->
          <v-row no-gutters>
            <v-col cols="3"> </v-col>
            <v-col cols="3"> </v-col>
            <v-col cols="3"> </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="budget.planning_nominal"
                outlined
                dense
                :disabled="true"
                placeholder="Planning Total"
                suffix="IDR"
                @change="onInput(budget)"
              >
              </v-text-field>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>

        <br>
        <v-card>
          <v-card-text>
          <v-row no-gutters>
          <v-col cols="6" align="left">
              <v-btn class="white--text ml-3" style="margin-left:1rem;" color='#7E73FF' @click="onAddNewBudget">
                Add Budget
              </v-btn>
          </v-col>
          <v-col cols="6" align="right">
            <v-btn
              rounded
              outlined
              class="light-blue--text"
              @click="$emit('cancelClicked')"
            >
              Cancel
            </v-btn>
            <v-btn rounded color="#16B1FF" class="white--text ml-3" type="submit"> Save </v-btn>
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
import { mapState, mapActions, mapGetters } from "vuex";
import formatting from "@/mixins/formatting";
export default {
  name: "FormBudgetExisting",
  props: ["form", "isView", "isNew"],
  mixins: [formatting],
  created() {
    this.getMyProject();
    this.getListActivePlanning();
    this.getAllProjectType();
    this.getAllBiro();
    this.getMasterProduct();
    this.getMasterCoa();
  },
  data: () => ({
    validation: {
      hasUpdated: false,
      required: [
        (v) => !!v || "This field is required"
      ],
      targetRule: [
        v => /(^[0-9.,]+$|^$|[null])/.test(v) || "This field is numbers only",
      ],
    },
    budgets: [],
    budget_table: [],
    listProjectType: [],
    projectTypeEnable: false,
    dataTable: {
      budgetPlanningHeaders: [
        { text: "Action", value: "actions", align: "center", sortable: false, width: "3%"},
        { text: "Year", value: "year", width: "9%" },
        { text: "COA", value: "coa", width: "15%" },
        { text: "CAPEX/OPEX", value: "expense_type", width: "10%" },
        { text: "Budget This Year", value: "planning_nominal", width: "15%" },
        { text: "Planning Q1", value: "planning_q1", width: "12%" },
        { text: "Planning Q2", value: "planning_q2", width: "12%" },
        { text: "Planning Q3", value: "planning_q3", width: "12%" },
        { text: "Planning Q4", value: "planning_q4", width: "12%" },
      ],
    },
  }),
  computed: {
    ...mapState("myProject", [
      "dataMyProject",
      "dataMyProjectById"
    ]),
    ...mapState("listBudget", [
      "dataActiveListBudget"
    ]),
    ...mapState("projectType", [
      "dataProjectType",
    ]),
    ...mapState("statusInfo", [
      "statusTechNonTech"
    ]),
    ...mapState("allBiro", [
      "dataAllBiro"
    ]),
    ...mapState("masterProduct", [
      "dataMasterProduct"
    ]),
    ...mapState("masterCoa", [
      "dataMasterCoa"
    ]),
    status: function () {
      return this.budget_table ? false : true;
    },
    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
    getRCC(){
      if(this.form.biro.id && this.form.biro.rcc != null){
        return this.form.biro.rcc;
      }else{
        return "-";
      }
    },
    nominal:{
      // getter
      get: function() {
        if(this.form.minimum_item_origin){
          this.form.minimum_item_origin = this.numberWithDots(this.form.minimum_item_origin)
          return this.form.minimum_item_origin;
        }
      },
      // setter
      set: function(newValue) {
        this.form.minimum_item_origin = this.numberWithDots(newValue)
      }
    }
  },
  methods: {
    ...mapActions("myProject", [
      "getMyProject",
      "getMyProjectById"
    ]),
    ...mapActions("listBudget", [
      "getListActivePlanning"
    ]),
    ...mapActions("projectType", [
      "getAllProjectType",
    ]),
    ...mapActions("allBiro", [
      "getAllBiro"
    ]),
    ...mapActions("masterProduct", [
      "getMasterProduct"
    ]),
    ...mapActions("masterCoa", [
      "getMasterCoa"
    ]),
    total_investment_input(){
      this.form.total_investment_value = this.numberWithDots(this.form.total_investment_value);
    },
    onSelectProject(){
      if(this.form.project && this.form.project.id){
        this.form.project_description = this.form.project.project_description;
        this.form.itfam_id = this.form.project.itfam_id;
        this.form.start_year = this.form.project.start_year;
        this.form.end_year = this.form.project.end_year;
        this.form.total_investment_value = this.numberWithDots(this.form.project.total_investment_value);

        var tech = this.form.project.is_tech == true ? this.statusTechNonTech.find((x)=> x.label=="Tech") :
                    this.statusTechNonTech.find((x)=> x.label=="Non-Tech");
        this.form.is_tech = tech;

        this.form.product = this.form.project.product;
        this.form.biro = this.form.project.biro;
        this.form.rcc = this.form.project.biro.rcc;
      } else{
        this.form.project_description = "";
        this.form.itfam_id = "";
        this.form.start_year = "";
        this.form.end_year = "";
        this.form.total_investment_value = "";
        this.form.is_tech = "";
        this.form.product = "";
        this.form.biro = "";
        this.form.rcc = "";
        this.form.project_type = "";
        this.projectTypeEnable = false;
      }

      this.onSelectFor();
    },

    onSelectFor(){
      if(this.form.project && this.form.project.id && this.form.planning && this.form.planning.id){
        this.getMyProjectById(this.form.project.id).then(() => {
          var project_detail = this.dataMyProjectById.project_detail.find((x)=> x.planning.id==this.form.planning.id);
          if(project_detail){
            this.projectTypeEnable = false;
            const result = this.dataProjectType.filter((project_type) => {
              return project_type.name == project_detail.project_type;
            });
            
            this.listProjectType = JSON.parse(JSON.stringify(result));
            this.form.project_type = this.listProjectType[0];
            this.budget_table = project_detail.budget;

          }else{
            this.budget_table = [];
            this.form.project_type = "";
            this.projectTypeEnable = true;
            const cleanData = JSON.parse(JSON.stringify(this.dataProjectType));
            var index = cleanData.findIndex(function(o){
              return o.name === 'New';
            });
            if (index !== -1) cleanData.splice(index, 1);
            this.listProjectType = cleanData;
          }
        });
      }
    },
    onInput(budget){
      budget.planning_q1 = this.numberWithDots(budget.planning_q1);
      budget.planning_q2 = this.numberWithDots(budget.planning_q2);
      budget.planning_q3 = this.numberWithDots(budget.planning_q3);
      budget.planning_q4 = this.numberWithDots(budget.planning_q4);
      budget.planning_nominal = parseInt(budget.planning_q1.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) +
      parseInt(budget.planning_q2.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) +
      parseInt(budget.planning_q3.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) +
      parseInt(budget.planning_q4.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''));

      budget.planning_nominal = this.numberWithDots(String(budget.planning_nominal));

      if(budget.coa){
        if(budget.coa.is_capex && parseInt(budget.planning_nominal.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) >= budget.coa.minimum_item_origin){
          budget.expense_type = "CAPEX"
        }else{
          budget.expense_type = "OPEX"
        }
      }
      

    },
    popBudgetByIndex(index){
      this.budgets.splice(index,1);
    },
    onSubmit() {
      let validate = this.$refs.form.validate();
      if (validate) {
        const tempBudgets = JSON.parse(JSON.stringify(this.budgets)); //make a temporary budget object
        tempBudgets.forEach(element => {
          element.planning_q1 = parseInt(element.planning_q1.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''));
          element.planning_q2 = parseInt(element.planning_q2.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''));
          element.planning_q3 = parseInt(element.planning_q3.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''));
          element.planning_q4 = parseInt(element.planning_q4.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''));
          element.coa = element.coa.id;
          delete element.planning_nominal;
        });

        var start_year = null;
        var end_year = null;

        try{
          start_year = parseInt(this.form.start_year);
        }catch{};
        try{
          end_year = parseInt(this.form.end_year);
        }catch{};

        const payload = {
            project_id : this.form.project.id,
            project_name : this.form.project.project_name, //refer ke object project
            project_description : this.form.project_description, //refer ke inputan form
            biro : this.form.project.biro.id,
            start_year: this.form.start_year?this.form.start_year:null,
            end_year: this.form.end_year?this.form.end_year:null,
            total_investment_value: this.form.total_investment_value? parseInt(this.form.total_investment_value.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')):0,
            product : this.form.product.id,
            is_tech : this.form.is_tech.label == "Tech" ? true : false,
            planning : this.form.planning.id,
            project_type : this.form.project_type.id,
            budget: tempBudgets
        };
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
      }
    },
    onAddNewBudget(){
      this.budgets.push({
          coa : "",
          expense_type : "",
          planning_q1 : "0",
          planning_q2 : "0",
          planning_q3 : "0",
          planning_q4 : "0",
          planning_nominal : "0"
      });
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
