<template>
  <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
    <v-card>
      <v-card-title>
        <strong style="margin-left:1rem;"> Project</strong>
      </v-card-title>
      <v-card-text>
        <v-divider></v-divider><br />
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
              rows="4"
              :disabled="isView"
              :rules="validation.required"
              placeholder="Input Here"
            >
            </v-textarea>
          </v-col>
        </v-row>

        <!-- Nama nama -->
        <v-row no-gutters>
          <v-col cols="3"> ID-ITFAM </v-col>
          <v-col cols="3">
            Start Year <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="3"> End Year </v-col>
          <v-col cols="3">
            Total Investment Value <strong class="red--text">*</strong>
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters>
          <v-col cols="3">
            <v-text-field
              v-model="form.itfam_id"
              outlined
              dense
              :disabled="true"
              placeholder="Auto Generated"
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
            Tech/Non-Tech <strong class="red--text">*</strong>
          </v-col>
          <v-col cols="3"> Product </v-col>
          <v-col cols="3"> Biro <strong class="red--text">*</strong> </v-col>
          <v-col cols="3"> RCC </v-col>
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

    <br />
    
    <v-card>
      <v-card-title>
        <strong style="margin-left:1rem;"> Project Detail</strong>
      </v-card-title>
      <v-card-text>
        <v-divider></v-divider><br />
        <!-- Nama nama -->
        <v-row no-gutters>
          <v-col cols="4"> For <strong class="red--text">*</strong></v-col>
          <v-col cols="4"> Project ID </v-col>
          <v-col cols="4"> Project Type <strong class="red--text">*</strong>
          </v-col>
        </v-row>

        <!-- Kolom kolom -->
        <v-row no-gutters>
          <v-col cols="4">
            <div>
              <v-select
                v-model="form.planning"
                :items="planningItem"
                item-text="year"
                item-value="id"
                placeholder="Year"
                outlined
                disabled
                :rules="validation.required"
                class="mr-2"
                :dense=true>
              </v-select>
            </div>
          </v-col>
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
                v-model="getProjectType"
                :items="dataProjectType"
                item-text="name"
                item-value="id"
                placeholder="Type"
                outlined
                return-object
                :rules="validation.required"
                class="mr-2"
                disabled
                :dense="true"
              >
              </v-select>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- List Budget -->

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

    <br />
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
  name: "FormBudgetNew",
  props: ["form", "isView", "isNew"],
  mixins: [formatting],
  created() {
    this.getAllProjectType();
    this.getAllBiro();
    this.getMasterProduct();
    this.getMasterCoa();
  },
  data: () => ({
    validation: {
      hasUpdated: false,
      required: [(v) => !!v || "This field is required"],
      targetRule: [
        v => /(^[0-9.,]+$|^$|[null])/.test(v) || "This field is numbers only",
      ],
    },
    budgets: [],
  }),
  computed: {
    ...mapState("projectType", ["dataProjectType"]),
    ...mapState("statusInfo", ["statusTechNonTech"]),
    ...mapState("allBiro", ["dataAllBiro"]),
    ...mapState("masterProduct", ["dataMasterProduct"]),
    ...mapState("masterCoa", ["dataMasterCoa"]),
    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
    getProjectType() {
      return this.dataProjectType.find((x) => x.name == "New");
    },
    planningItem(){
      return [this.form.planning,]
    },
    getRCC() {
      if(this.form.biro){
        let codeBiro =  this.form.biro.code;
        let found = this.dataAllBiro.find((x) => x.code == codeBiro);
        if (found) {
          return found.rcc ? found.rcc : '-';
        }
        else{
          return '-';
        }
      }
      else{
        return '-';
      }
    },
  },
  methods: {
    ...mapActions("projectType", ["getAllProjectType"]),
    ...mapActions("allBiro", ["getAllBiro"]),
    ...mapActions("masterProduct", ["getMasterProduct"]),
    ...mapActions("masterCoa", ["getMasterCoa"]),
    total_investment_input() {
      this.form.total_investment_value = this.numberWithDots(
        this.form.total_investment_value
      );
    },

    onInput(budget) {
      budget.planning_q1 = this.numberWithDots(budget.planning_q1);
      budget.planning_q2 = this.numberWithDots(budget.planning_q2);
      budget.planning_q3 = this.numberWithDots(budget.planning_q3);
      budget.planning_q4 = this.numberWithDots(budget.planning_q4);
      budget.planning_nominal =
        parseInt(
          budget.planning_q1.replace(
            /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
            ""
          )
        ) +
        parseInt(
          budget.planning_q2.replace(
            /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
            ""
          )
        ) +
        parseInt(
          budget.planning_q3.replace(
            /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
            ""
          )
        ) +
        parseInt(
          budget.planning_q4.replace(
            /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
            ""
          )
        );
      budget.planning_nominal = this.numberWithDots(String(budget.planning_nominal));

      if (budget.coa) {
        if (
          budget.coa.is_capex &&
          parseInt(
            budget.planning_nominal.replace(
              /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
              ""
            )
          ) >= budget.coa.minimum_item_origin
        ) {
          budget.expense_type = "CAPEX";
        } else {
          budget.expense_type = "OPEX";
        }
      }
    },
    popBudgetByIndex(index) {
      this.budgets.splice(index, 1);
    },
    onSubmit() {
      let validate = this.$refs.form.validate();
      //let nominal = parseInt(this.form.minimum_item_origin.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''))
      if (validate) {
        const tempBudgets = JSON.parse(JSON.stringify(this.budgets)); //make a temporary budget object
        tempBudgets.forEach((element) => {
          element.planning_q1 = parseInt(
            element.planning_q1.replace(
              /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
              ""
            )
          );
          element.planning_q2 = parseInt(
            element.planning_q2.replace(
              /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
              ""
            )
          );
          element.planning_q3 = parseInt(
            element.planning_q3.replace(
              /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
              ""
            )
          );
          element.planning_q4 = parseInt(
            element.planning_q4.replace(
              /[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g,
              ""
            )
          );
          element.coa = element.coa.id;
          delete element.planning_nominal;
        });

        const payload = {
          itfam_id: this.form.itfam_id,
          project_name: this.form.project_name,
          project_description: this.form.project_description,
          biro: this.form.biro.id,
          start_year: this.form.start_year?this.form.start_year:null,
          end_year: this.form.end_year?this.form.end_year:null,
          total_investment_value: this.form.total_investment_value? parseInt(this.form.total_investment_value.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')):0,
          product: this.form.product.id,
          is_tech: (this.form.is_tech.id = 1 ? true : false),
          planning: this.form.planning.id,
          project_type: this.getProjectType.id,
          dcsp_id: this.form.dcsp_id,
          budget: tempBudgets,
        };
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
      }
    },
    onAddNewBudget() {
      this.budgets.push({
        coa: "",
        expense_type: "",
        planning_q1: "0",
        planning_q2: "0",
        planning_q3: "0",
        planning_q4: "0",
        planning_nominal: "0",
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
.FormPlanning__checkbox {
  align-content: flex-start;
}
</style>
