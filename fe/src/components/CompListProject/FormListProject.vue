<template>
  <v-card>
    <v-card-title class="text-h5" style="margin-bottom: 32px">
      {{ cardTitle }} a Project
      <v-spacer></v-spacer>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="ListProject__form">
        <v-row no-gutters>
          <!-- PROJECT NAME -->
          <v-col no-gutters> Project Name
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.project_name"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- PROJECT DESCRIPTION -->
          <v-col no-gutters> Project Description
            <v-col>
              <div class="ListProject__field">
                <v-textarea
                  v-model="form.project_description"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-textarea>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- PRODUCT ID -->
          <v-col no-gutters> Product ID
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.product.product_code"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- PRODUCT NAME -->
          <v-col no-gutters> Product Name
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.product.product_name"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- ITFAM ID -->
          <v-col no-gutters> ITFAM ID
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.itfam_id"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <v-row no-gutters>
          <!-- RCC -->
          <v-col no-gutters> RCC
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.biro.rcc"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- BIRO -->
          <v-col no-gutters> Biro
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.biro.code"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- TECH/NON-TECH -->
          <v-col no-gutters> Tech/Non-Tech
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.is_tech"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- START YEAR -->
          <v-col no-gutters> Start Year
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.start_year"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- END YEAR -->
          <v-col no-gutters> End Year
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.end_year"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- TOTAL INVESTMENT -->
          <v-col no-gutters> Total Investment
            <v-col>
              <div class="ListProject__field">
                <v-text-field
                  v-model="form.total_investment_value"
                  outlined
                  return-object
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
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
              v-if="isView">
              OK
            </v-btn>
            <v-btn
              rounded
              outlined
              class="primary--text"
              @click="$emit('cancelClicked')"
              v-if="!isView">
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
  name: "FormListProject",
  props: ["form", "isNew", "isView"],

  data:() => ({
    
  }),

  // created() {
  //   this.getListPlanningById(this.$route.params.id);
  // },

  computed: {
    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
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

  .cancelBtn {
    width: 200px;
  }
  .saveBtn {
    width: 200px;
  }
  .saveBtn--text /deep/ label {
    color: white;
  }
</style>

<style lang="scss">
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
    min-width: 90%;
  }
  .ListProject__btn {
    text-align: end;
    button {
      margin: 10px 32px;
    }
  }
</style>