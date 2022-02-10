<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} a Project Detail
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="EditProjectDetail__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- YEAR -->
            <v-col cols="6"> Year
                <div class="EditProjectDetail__field">
                    <v-text-field
                    v-model="form.planning.year"
                    outlined
                    return-object
                    dense
                    disabled>
                    </v-text-field>
                </div>
            </v-col>
        </v-row>

        <!-- PROJECT ID -->
        <v-row no-gutters>
          <v-col cols="6"> Project ID
              <div class="EditProjectDetail__field">
                <v-text-field
                  v-model="form.dcsp_id"
                  outlined
                  return-object
                  dense
                  disabled>
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- STATUS -->
        <v-row no-gutters>
          <v-col cols="6"> Status
              <div class="EditProjectDetail__field">
                <v-select
                v-model="form.planning.is_active"
                :items="statusInfoPlanning"
                item-text="label"
                item-value="id"
                placeholder="Choose Active/Inactive"
                outlined
                return-object
                dense
                disabled>
                </v-select>
              </div>
          </v-col>
        </v-row>

        <!-- DUE DATE -->  
        <v-row no-gutters>
          <v-col cols="6"> Due Date
              <div class="EditProjectDetail__field">
                <v-text-field
                  v-model="form.planning.due_date"
                  outlined
                  return-object
                  dense
                  disabled>
                </v-text-field>
              </div>
          </v-col>
        </v-row>

        <!-- PROJECT TYPE CARRY FORWARD/REGULAR -->
        <v-row no-gutters v-if="form.project_type != 'New'">
          <v-col cols="6"> Project Type <strong class="red--text">*</strong>
              <div class="EditProjectDetail__field">
                <v-select
                v-model="form.project_type"
                :items="projectTypeNotNew"
                item-text="name"
                item-value="name"
                placeholder="Choose Project Type"
                outlined
                return-object
                dense
                :disabled="isView"
                :rules="validation.required">
                </v-select>
              </div>
          </v-col>
        </v-row>

        <!-- PROJECT TYPE NEW -->
        <v-row no-gutters v-if="form.project_type == 'New'">
          <v-col cols="6"> Project Type <strong class="red--text">*</strong>
              <div class="EditProjectDetail__field">
                <v-select
                v-model="form.project_type"
                :items="projectTypeNew"
                item-text="name"
                item-value="name"
                placeholder="Choose Project Type"
                outlined
                return-object
                dense
                :disabled="isView"
                :rules="validation.required">
                </v-select>
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
export default {
  name: "FormEditProjectDetail",
  props: ["form", "isNew", "isView"],

  data: () => ({
    projectTypeNew: [
        {name: "New", id: 2}
    ],
    projectTypeNotNew: [
        {name: "Carry Forward", id: 1},
        {name: "Regular", id: 3},
    ],
    
    validation: {
      required: [
        (v) => !!v || "This field is required"
      ],
    },
  }),
  
  computed: {
    ...mapState("statusInfo", ["statusInfoPlanning"]),
    ...mapState("projectType", ["getAllProjectType", "dataProjectType"]),

    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
    // getProjectType(){
    //   return this.dataProjectType.find((x)=> x.name=="New");
    // },
    // isActive() {
    //   return this.form.planning.is_active ? "Active" : "Inactive";
    // },
  },

//   mounted(){
//     console.log(this.form);
//   },

  methods: {
    onSubmit() {
      let validate = this.$refs.form.validate();
      if (validate) {
        const payload = {
            id: this.form.id,
            planning: this.form.planning.id,
            dcsp_id: this.form.dcsp_id,
            project: this.form.project,
            project_type: this.form.project_type.id
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
  .EditProjectDetail__checkbox{
    align-content:flex-start
  }
  .EditProjectDetail__form{
    width: auto;
    margin-left: 2% !important;
  }
  .EditProjectDetail__select{
    min-width: 500px;
  }
  .EditProjectDetail__field {
    width: 90%;
  }
  .EditProjectDetail__btn {
    text-align: end;
    button {
      margin: 10px 32px;
      min-width: 8rem;
    }
  }
</style>
    
