<template>
  <v-card>
    <v-card-title class="text-h5" style="margin-bottom: 32px">
      {{ cardTitle }} a Monitoring Status
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="monitor-planning__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- GROUP -->
          <v-col cols="6"> Group <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="monitor-planning__field">
                <v-text-field
                  v-model="form.biro.group_code"
                  outlined
                  dense
                  disabled
                  :rules="validation.required">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- SUBGROUP -->
          <v-col cols="6"> Sub-Group <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="monitor-planning__field">
                <v-text-field
                  v-model="form.biro.sub_group_code"
                  outlined
                  dense
                  disabled
                  :rules="validation.required">
                </v-text-field>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <!-- BIRO -->  
        <v-row no-gutters>
          <v-col cols="6"> Biro <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="monitor-planning__field">
                <v-text-field
                  v-model="form.biro.code"
                  outlined
                  dense
                  disabled
                  :rules="validation.required">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- PIC -->
          <v-col cols="6"> PIC <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="monitor-planning__field">
                <v-text-field
                  v-model="form.pic_initial"
                  outlined
                  dense
                  disabled
                  :rules="validation.required">
                </v-text-field>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <!-- UPDATED DATE -->
        <v-row no-gutters>
          <v-col cols="6"> Updated Date <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="monitor-planning__field">
                <v-text-field
                  v-model="form.updated_at"
                  outlined
                  dense
                  disabled
                  :rules="validation.required">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- STATUS -->
          <v-col cols="6"> Status <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="monitor-planning__field">
                <v-select
                  v-model="form.status"
                  :items="monitorPlanning"
                  item-text="activeInactive"
                  label="Active"
                  outlined
                  return-object
                  :disabled="isView"
                  :rules="validation.required">
                </v-select>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <!-- BUTTONS -->
        <v-row no-gutters>
          <v-col no-gutters class="monitor-planning__btn">
            <v-btn rounded outlined class="primary--text" @click="onCancel" v-if="!isView" style="width: 8rem; margin-top: 120px; margin-left: 212px">
              Cancel
            </v-btn>
          </v-col>
          <v-col no-gutters>
            <v-btn rounded class="primary" @click="onSubmit" v-if="!isView" style="width: 8rem; margin-top: 120px">
              Submit
            </v-btn>
          </v-col>
          <v-col no-gutters class="monitor-planning__btn">
            <v-btn v-if="isView" rounded class="primary" @click="onOK" style="width: 8rem; margin-top: 120px">
              OK
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
  name: "FormMonitorPlanning",
  props: ["form", "isNew", "isView", "dataAllBiro"],
  
  data: () => ({
    validation: {
      required: [
        (v) => !!v || "This field is required"
      ],
      targetRule: [
        v => /^[0-9.,]+$/.test(v) || "This field is numbers only",
      ],
    },

    statusOptions: [
      {activeInactive: 'Active'},
      {activeInactive: 'Inactive'}
    ],
    status: null,
    
    closeOnContentClick: true,
  }),
  
  computed: {
    ...mapState("statusInfo", ["statusInfoPlanning"]),
    ...mapState("allBiro", ["getAllBiro"]),
    ...mapState("monitorPlanning", ["getMonitorPlanning"]),

    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
  },

  methods: {
    onSubmit() {
      let validate = this.$refs.form.validate();
      // let nominal = parseInt(this.form.minimum_item_origin.replace(/[~`!@#$%^&*()+={}\[\];:\'\"<>.,\/\\\?-_]/g, ''))
      if (validate) {
        const payload = {
          group: this.form.biro.group_code,
          subgroup: this.form.biro.sub_group_code,
          code: this.form.biro.code,
          pic: this.form.pic_initial,
          monitoring_status: this.form.monitoring_status,
        };
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
      }
    },
    onCancel() {
        return this.$router.go(-1);
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
  .monitor-planning__checkbox{
    align-content:flex-start
  }
  .monitor-planning__form{
    width: auto;
    margin-left: 2% !important;
  }
  .monitor-planning__select{
    min-width: 500px;
  }
  .monitor-planning__field {
    min-width: 165px;
  }
  .monitor-planning__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
</style>
