<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} Project
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')" class="mr-3">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
      <v-btn v-if="isView" icon small @click="$emit('logHistoryClicked')">
        <v-icon color="primary"> mdi-history </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="MyProject__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- PROJECT NAME -->
          <v-col cols="12" no-gutters> Project Name <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-text-field
                  v-model="form.project_name"
                  outlined
                  return-object
                  dense
                  disabled>
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- PROJECT DESCRIPTION -->
          <v-col cols="12" no-gutters> Project Description <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-textarea
                  v-model="form.project_description"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  placeholder="Fill the Project Description"
                  :rules="validation.required">
                </v-textarea>
              </div>
            <!-- </v-col> -->
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- PRODUCT ID -->
          <v-col cols="4" no-gutters> Product ID <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-select
                v-model="form.product"
                :items="dataMasterProduct"
                item-text="product_code"
                item-value="id"
                placeholder="Choose Product"
                disabled
                dense
                outlined
                return-object
                class="mr-3"
                :rules="validation.required">
                </v-select>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- PRODUCT NAME -->
          <v-col cols="4" no-gutters> Product Name <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-select
                v-model="form.product"
                :items="dataMasterProduct"
                item-text="product_name"
                item-value="id"
                placeholder="Choose Product"
                dense
                outlined
                disabled
                return-object
                class="mr-3"
                :rules="validation.required">
                </v-select>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- ITFAM ID -->
          <v-col cols="4" no-gutters> ITFAM ID <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-text-field
                  v-model="form.itfam_id"
                  outlined
                  return-object
                  dense
                  disabled
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- RCC -->
          <v-col cols="2" no-gutters> RCC <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-select
                v-model="form.biro"
                :items="dataAllBiro"
                item-text="rcc"
                item-value="id"
                placeholder="Choose Biro"
                disabled
                dense
                outlined
                return-object
                class="mr-3"
                :rules="validation.required">
                </v-select>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- BIRO -->
          <v-col cols="2" no-gutters> Biro <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-select
                v-model="form.biro"
                :items="dataAllBiro"
                item-text="code"
                item-value="id"
                placeholder="Choose Biro"
                disabled
                dense
                outlined
                return-object
                class="mr-3"
                :rules="validation.required">
                </v-select>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- TECH/NON-TECH -->
          <v-col cols="2" no-gutters> Tech/Non-Tech <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-select
                v-model="form.is_tech"
                :items="isTech"
                item-text="label"
                item-value="value"
                placeholder="Choose Tech/Non-Tech"
                :disabled="isView"
                dense
                outlined
                return-object
                class="mr-3"
                :rules="validation.techRule">
                </v-select>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- START YEAR -->
          <v-col cols="2" no-gutters> Start Year <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-text-field
                  v-model="form.start_year"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3"
                  :rules="validation.required">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- END YEAR -->
          <v-col cols="2" no-gutters> End Year
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-text-field
                  v-model="form.end_year"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- TOTAL INVESTMENT -->
          <v-col cols="2" no-gutters> Total Investment <strong class="red--text">*</strong>
            <!-- <v-col> -->
              <div class="MyProject__field">
                <v-text-field
                  v-model="nominal"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  suffix="IDR"
                  class="mr-3"
                  :rules="validation.targetRule">
                </v-text-field>
              </div>
            </v-col>
          <!-- </v-col> -->
        </v-row>

        <!-- BUTTONS -->
        <v-row no-gutters>
          <v-col cols="12" align="right">
            <!-- <v-btn
              rounded
              outlined
              class="primary--text"
              @click="$emit('okClicked')"
              v-if="isView"
              style="min-width: 8rem;">
              OK
            </v-btn> -->
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
  name: "FormMyProject",
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
      yearRule: [
        //if (!v.trim()) return true;
        v => { if (!isNaN(parseFloat(v)) && v >= 1000 && v <= 9999) return true;
        return 'Year has to be integer and contains 4 digits'; }
      ],
    },

    isTech: [
      { label: 'Tech', value: 1 },
      { label: 'Non-Tech', value: 0 },
    ],
  }),

  computed: {
    ...mapState("myProject", ["getMyProject", "dataMyProject"]),
    ...mapState("masterProduct", ["getMasterProduct", "dataMasterProduct"]),
    ...mapState("allBiro", ["getAllBiro", "dataAllBiro"]),

    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    nominal: {
      // getter
      get: function() {
        if(this.form.total_investment_value){
          this.form.total_investment_value = this.numberWithDots(this.form.total_investment_value)
          return this.form.total_investment_value;
        }
      },
      // setter
      set: function(newValue) {
        this.form.total_investment_value = this.numberWithDots(newValue)
      }
    },
    label: {
      get: function() {
        return this.form.is_tech ? "Tech" : "Non-Tech";
      }
    },
  },

  methods: {
    onSubmit() {
      let validate = this.$refs.form.validate();
      if (validate) {
        const payload = {
          id: this.form.id,
          project_name: this.form.project_name,
          project_description: this.form.project_description,
          product: this.form.product.id,
          start_year: this.form.start_year,
          end_year: this.form.end_year,
          total_investment_value: this.nominal ? parseInt(this.form.total_investment_value.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '')) : 0,
          biro: this.form.biro.id,
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
  }
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
  .MyProject__checkbox{
    align-content:flex-start
  }
  .MyProject__form{
    width: 100%;
    margin-left: 2% !important;
    margin-right: 2% !important;
  }
  .MyProject__select{
    min-width: 500px;
  }
  .MyProject__field {
    min-width: 100%;
  }
  .MyProject__btn {
    text-align: end;
    button {
      margin: 10px 32px;
      width: 8 rem;
    }
  }
</style>