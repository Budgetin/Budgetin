<template>
  <v-card>
    <v-card-title class="text-h5">
      {{ cardTitle }} a Monitoring Status
      <v-spacer></v-spacer>
      <!-- <v-btn v-if="isView" icon small @click="$emit('editClicked')"> -->
      <v-btn v-if="isView" icon small link :to="'/startPlanning/editStatusMonitor'">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form class="monitor-planning__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- GROUP -->
          <v-col cols="6"> Group <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="monitor-planning__field">
                <v-text-field
                    v-if="isView || (!isView && !isNew)"
                    outlined
                    dense
                    disabled
                    label="GAQ">
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
                    v-if="isView || (!isView && !isNew)"
                    outlined
                    dense
                    disabled
                    label="ARC">
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
                    v-if="isView || (!isView && !isNew)"
                    outlined
                    dense
                    disabled
                    label="ARC A">
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
                    v-if="isView || (!isView && !isNew)"
                    outlined
                    dense
                    disabled
                    label="Jumas Ranope">
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
                    v-if="isView || (!isView && !isNew)"
                    outlined
                    dense
                    disabled
                    label="2022-11-25">
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
                  v-if="isView"
                  v-model="status"
                  :items="statusOptions"
                  item-text="activeInactive"
                  label="Active"
                  outlined
                  return-object
                  disabled>
                </v-select>
                <v-select
                  v-if="!isView"
                  v-model="status"
                  :items="statusOptions"
                  item-text="activeInactive"
                  label="Active/Inactive"
                  outlined
                  return-object>
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
export default {
  name: "FormMonitorPlanning",
  props: ["isNew", "isView"],
  
  data: () => ({
    date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    menu: false,

    validation: {
      required: (v) => !!v || "This field is required",
    },

    yearOptions: [
      {yearValue: '2023'},
      {yearValue: '2024'},
      {yearValue: '2025'},
      {yearValue: '2026'},
      {yearValue: '2027'},
      {yearValue: '2028'},
      {yearValue: '2029'},
      {yearValue: '2030'},
      {yearValue: '2031'},
      {yearValue: '2032'},
      {yearValue: '2033'}
    ],
    year: null,

    statusOptions: [
      {activeInactive: 'Active'},
      {activeInactive: 'Inactive'}
    ],
    status: null,

    notifOptions: [
      {option: 'Yes'},
      {option: 'No'}
    ],
    notif: false,

    biroGsit: [
      {biroGsitName: 'GSIT ARC A', biroGsitEmail: 'gsit_arc_a_00@intra.bca'},
      {biroGsitName: 'GSIT CTS A', biroGsitEmail: 'gsit_cts_a_00@intra.bca'},
      {biroGsitName: 'GSIT CTS B', biroGsitEmail: 'gsit_cts_b_00@intra.bca'},
      {biroGsitName: 'GSIT CTS C', biroGsitEmail: 'gsit_cts_c_00@intra.bca'},
      {biroGsitName: 'GSIT CTS D', biroGsitEmail: 'gsit_cts_d_00@intra.bca'},
      {biroGsitName: 'GSIT CTS E', biroGsitEmail: 'gsit_cts_e_00@intra.bca'},
      {biroGsitName: 'GSIT DIS A', biroGsitEmail: 'gsit_dis_a_00@intra.bca'},
      {biroGsitName: 'GSIT DIS B', biroGsitEmail: 'gsit_dis_b_00@intra.bca'},
      {biroGsitName: 'GSIT DTM A', biroGsitEmail: 'gsit_dtm_a_00@intra.bca'},
      {biroGsitName: 'GSIT DTM B', biroGsitEmail: 'gsit_dtm_b_00@intra.bca'},
      {biroGsitName: 'GSIT DTM C', biroGsitEmail: 'gsit_dtm_c_00@intra.bca'},
      {biroGsitName: 'GSIT IBO A', biroGsitEmail: 'gsit_ibo_a_00@intra.bca'},
      {biroGsitName: 'GSIT IBO B', biroGsitEmail: 'gsit_ibo_b_00@intra.bca'},
      {biroGsitName: 'GSIT IBO C', biroGsitEmail: 'gsit_ibo_c_00@intra.bca'},
      {biroGsitName: 'GSIT IBO D', biroGsitEmail: 'gsit_ibo_d_00@intra.bca'},
      {biroGsitName: 'GSIT IBO E', biroGsitEmail: 'gsit_ibo_e_00@intra.bca'},
      {biroGsitName: 'GSIT IBO F', biroGsitEmail: 'gsit_ibo_f_00@intra.bca'},
      {biroGsitName: 'GSIT IBO G', biroGsitEmail: 'gsit_ibo_g_00@intra.bca'},
      {biroGsitName: 'GSIT IMO A', biroGsitEmail: 'gsit_imo_a_00@intra.bca'},
      {biroGsitName: 'GSIT IMO B', biroGsitEmail: 'gsit_imo_b_00@intra.bca'},
      {biroGsitName: 'GSIT IMO C', biroGsitEmail: 'gsit_imo_c_00@intra.bca'},
      {biroGsitName: 'GSIT IMO D', biroGsitEmail: 'gsit_imo_d_00@intra.bca'},
      {biroGsitName: 'GSIT ISO A', biroGsitEmail: 'gsit_iso_a_00@intra.bca'},
      {biroGsitName: 'GSIT ISO B', biroGsitEmail: 'gsit_iso_b_00@intra.bca'},
      {biroGsitName: 'GSIT ISO C', biroGsitEmail: 'gsit_iso_c_00@intra.bca'},
      {biroGsitName: 'GSIT ITX A', biroGsitEmail: 'gsit_itx_a_00@intra.bca'},
      {biroGsitName: 'GSIT ITX B', biroGsitEmail: 'gsit_itx_b_00@intra.bca'},
      {biroGsitName: 'GSIT ITX C', biroGsitEmail: 'gsit_itx_c_00@intra.bca'},
      {biroGsitName: 'GSIT ITX D', biroGsitEmail: 'gsit_itx_d_00@intra.bca'},
      {biroGsitName: 'GSIT ITX E', biroGsitEmail: 'gsit_itx_e_00@intra.bca'},
      {biroGsitName: 'GSIT ITX F', biroGsitEmail: 'gsit_itx_f_00@intra.bca'},
      {biroGsitName: 'GSIT ITX G', biroGsitEmail: 'gsit_itx_g_00@intra.bca'},
      {biroGsitName: 'GSIT NIS A', biroGsitEmail: 'gsit_nis_a_00@intra.bca'},
      {biroGsitName: 'GSIT NIS B', biroGsitEmail: 'gsit_nis_b_00@intra.bca'},
      {biroGsitName: 'GSIT NIS C', biroGsitEmail: 'gsit_nis_c_00@intra.bca'},
      {biroGsitName: 'GSIT NIS D', biroGsitEmail: 'gsit_nis_d_00@intra.bca'},
      {biroGsitName: 'GSIT NIS E', biroGsitEmail: 'gsit_nis_e_00@intra.bca'},
      {biroGsitName: 'GSIT SAQ A', biroGsitEmail: 'gsit_saq_a_00@intra.bca'},
      {biroGsitName: 'GSIT SAQ B', biroGsitEmail: 'gsit_saq_b_00@intra.bca'},
      {biroGsitName: 'GSIT SAQ C', biroGsitEmail: 'gsit_saq_c_00@intra.bca'},
      {biroGsitName: 'GSIT SIS A', biroGsitEmail: 'gsit_sis_a_00@intra.bca'},
      {biroGsitName: 'GSIT SIS B', biroGsitEmail: 'gsit_sis_b_00@intra.bca'},
      {biroGsitName: 'GSIT SIS C', biroGsitEmail: 'gsit_sis_c_00@intra.bca'},
      {biroGsitName: 'GSIT SIS D', biroGsitEmail: 'gsit_sis_d_00@intra.bca'}
    ],
    
    closeOnContentClick: true,
  }),
  
  computed: {
    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
  },

  methods: {
    onSubmit() {
      console.log(this.planningFor, this.status, this.date, this.sendNotif)
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
