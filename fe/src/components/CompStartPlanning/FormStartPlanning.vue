<template>
  <v-card>
    <v-card-title class="text-h5">
      Start a New Planning
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form class="StartPlanning__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- PLANNING FOR -->
          <v-col cols="6"> Planning For <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="planningFor">
                <v-select
                  v-model="year"
                  :items="yearOptions"
                  item-text="yearValue"
                  label="Pick a Year"
                  outlined
                  return-object>
                </v-select>
              </div>
            </v-col>
          </v-col>

          <!-- STATUS -->
          <v-col cols="6"> Status <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="status">
                <v-select
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

        <!-- DUE DATE -->  
        <v-row no-gutters>
          <v-col cols="6"> Due Date <strong class="red--text">*</strong>
            <v-col cols="12" sm="6" md="4">
              <v-menu
                v-model="menu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto">
                <template v-slot:activator="{ on, attrs }">
                  <div class="dueDate">
                    <v-text-field
                      v-model="date"
                      outlined
                      readonly
                      v-bind="attrs"
                      v-on="on">
                    </v-text-field>
                  </div>
                </template>
                <v-date-picker
                  v-model="date"
                  @input="menu = false">
                </v-date-picker>
              </v-menu>
            </v-col>
          </v-col>

          <!-- SEND NOTIFICATION -->
          <v-col cols="6"> Send Notification <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="sendNotif">
                <v-select
                  v-model="notif"
                  :items="notifOptions"
                  item-text="option"
                  label="Yes/No"
                  outlined
                  return-object
                  @click="notifValue(returnValue)">
                </v-select>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <!-- SEND TO -->
        <v-row no-gutters v-if="notifValue(returnValue)=='Yes'">
          <v-col> Send to <strong class="red--text">*</strong>
            <v-col no-gutters>
              <v-select
                class="StartPlanning__select"
                v-model="sendToEmail"
                :items="biroGsit"
                item-text="biroGsitName"
                item-value="biroGsitEmail"
                label="Select Biro"
                multiple
                chips
                outlined>
              </v-select>
            </v-col>
            
            <!-- <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="sendTo">
                <v-select
                  v-model="sendToEmail"
                  :items="biroGsit"
                  item-text="biroGsitName"
                  item-value="biroGsitEmail"
                  label="Send to"
                  outlined
                  multiple
                  chips
                  return-object>
                </v-select>
              </div>
            </v-col> -->
          </v-col>
        </v-row>

        <!-- E-MAIL BODY -->
        <v-row no-gutters v-if="notifValue(returnValue)=='Yes'">
          <v-col> E-mail Body
            <v-col>
              <div class="emailBody">
                <v-textarea
                  outlined
                  dense
                  :disabled="isView">
                </v-textarea>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <!-- BUTTONS -->
        <v-row no-gutters>
          <v-col cols="11" align="right">
            <!-- <div class="cancelBtn"> -->
              <v-btn
                rounded
                outlined
                class="primary--text"
                @click="$emit('cancelClicked')"
                v-if="!isView">
                Cancel
              </v-btn>
              <v-btn rounded class="primary ml-3" type="submit" v-if="!isView">
                Submit
              </v-btn>
            <!-- </div> -->
          </v-col>
        </v-row>
      </v-form>      
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "FormStartPlanning",
  props: ["isView"],

  data() {
    return {
      // dialog: false,
      planningFor: '',
      status: '',
      sendNotif: '',
      date: null,
      sendToEmail: [],
    }
  },
  data: () => ({
    date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    menu: false,

    checkbox: false,
    validation: {
      required: (v) => !!v || "This field is required",
      // counterInitial: (v) => v.length <= 50 || "Max. 50 characters",
      // counterName: (v) => v.length <= 50 || "Max. 50 characters",
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
    year: '2023',

    statusOptions: [
      {activeInactive: 'Active'},
      {activeInactive: 'Inactive'}
    ],
    status: null,

    notifOptions: [
      {option: 'Yes'},
      {option: 'No'}
    ],
    notif: 'No',

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

  methods: {
    submit() {
      console.log(this.planningFor, this.status, this.date, this.sendNotif)
    },
    notifValue(returnValue) {
      return this.notif.option
    },
  },
}
</script>

<style scoped>
  .planningFor {
    min-width: 165px;
  }
  .status {
    min-width: 165px;
  }
  .dueDate {
    min-width: 165px;
  }
  .sendNotif {
    min-width: 165px;
  }
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
  .StartPlanning__checkbox{
    align-content:flex-start
  }
  .StartPlanning__form{
    width: auto;
    margin-left: 2% !important;
  }
  .StartPlanning__select{
    min-width: 500px;
  }
</style>
    
