<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} Project Detail
      <v-spacer></v-spacer>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="ListProject__form">
        <v-row no-gutters>
          <!-- PROJECT NAME -->
          <v-col cols="12" no-gutters> Project Name
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.project_name"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- PROJECT DESCRIPTION -->
          <v-col cols="12" no-gutters> Project Description
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-textarea
                  v-model="form.project_description"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-textarea>
              </div>
            <!-- </v-col> -->
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- PRODUCT ID -->
          <v-col cols="4" no-gutters> Product ID
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.product.product_code"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- PRODUCT NAME -->
          <v-col cols="4" no-gutters> Product Name
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.product.product_name"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- ITFAM ID -->
          <v-col cols="4" no-gutters> ITFAM ID
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.itfam_id"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- RCC -->
          <v-col cols="2" no-gutters> RCC
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.biro.rcc"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- BIRO -->
          <v-col cols="2" no-gutters> Biro
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.biro.code"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- TECH/NON-TECH -->
          <v-col cols="2" no-gutters> Tech/Non-Tech
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="label"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- START YEAR -->
          <v-col cols="2" no-gutters> Start Year
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.start_year"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  class="mr-3">
                </v-text-field>
              </div>
            <!-- </v-col> -->
          </v-col>

          <!-- END YEAR -->
          <v-col cols="2" no-gutters> End Year
            <!-- <v-col> -->
              <div class="ListProject__field">
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
          <v-col cols="2" no-gutters> Total Investment
            <!-- <v-col> -->
              <div class="ListProject__field">
                <v-text-field
                  v-model="nominal"
                  outlined
                  return-object
                  dense
                  :disabled="isView"
                  suffix="IDR"
                  class="mr-3">
                </v-text-field>
              </div>
            </v-col>
          <!-- </v-col> -->
        </v-row>

        <!-- BUTTONS -->
        <v-row no-gutters>
          <v-col cols="12" align="right">
            <v-btn
              rounded
              outlined
              class="primary--text ListProject__btn"
              @click="$emit('okClicked')"
              v-if="isView">
              OK
            </v-btn>
            <v-btn
              rounded
              outlined
              class="primary--text ListProject__btn"
              @click="$emit('cancelClicked')"
              v-if="!isView">
              Cancel
            </v-btn>
            <v-btn rounded class="primary ml-3 ListProject__btn" type="submit" v-if="!isView">
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
  name: "FormListProject",
  props: ["form", "isNew", "isView"],

  computed: {
    ...mapState("listProject", ["getListProject", "dataListProject"]),

    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },

    nominal: {
      // getter
      get: function() {
        if(this.form.total_investment_value) {
          this.form.total_investment_value = this.form.total_investment_value.toString().replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, '');
          this.form.total_investment_value = this.form.total_investment_value.toString().split( /(?=(?:\d{3})+(?:\.|$))/g ).join( "," );
        }
        return this.form.total_investment_value;
      },
    },

    label: {
      get: function() {
        return this.form.is_tech ? "Tech" : "Non-Tech";
      }
    },
  },

  methods: {
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
  .ListProject__checkbox{
    align-content:flex-start
  }
  .ListProject__form{
    width: 100%;
    margin-left: 2% !important;
    margin-right: 2% !important;
  }
  .ListProject__select{
    min-width: 500px;
  }
  .ListProject__field {
    min-width: 100%;
  }
  .ListProject__btn {
    text-align: end;
    button {
      margin: 10px 32px;
      width: 8 rem;
    }
  }
</style>