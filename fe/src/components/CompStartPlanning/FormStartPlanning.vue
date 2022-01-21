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
      <v-form ref="form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- PLANNING FOR -->
          <v-col cols="6"> Planning For <strong class="red--text">*</strong>
            <v-col cols="6">
              <div class="planningFor">
                <v-text-field
                  outlined
                  dense
                  :disabled="isView"
                  :rules="[validation.required]">
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
            
            <!-- <v-col cols="6">
              <div class="status">
                <v-text-field
                  outlined
                  dense
                  :disabled="isView"
                  :rules="[validation.required]">
                </v-text-field>
              </div>
            </v-col> -->
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
                      prepend-icon="mdi-calendar"
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
          <v-col cols="6"> Send to
            <v-col cols="6">
              <div class="sendTo">
                <v-text-field
                  outlined
                  dense
                  :disabled="isView">
                </v-text-field>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <!-- E-MAIL BODY -->
        <v-row no-gutters v-if="notifValue(returnValue)=='Yes'">
          <v-col cols="6"> E-mail Body
            <v-col cols="6">
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
            <!-- </div> -->
            <!-- <div class="submitBtn">
              <v-btn
                rounded
                outlined
                class="primary ml-3"
                type="submit"
                @click="$emit('okClicked')"
                v-if="isView">
                Submit
              </v-btn>
            </div> -->
            <!-- <div class="submitBtn"> -->
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
    }
  },
  data: () => ({
      date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      menu: false,
      // dialog: false,

      checkbox: false,
      validation: {
        required: (v) => !!v || "This field is required",
        // counterInitial: (v) => v.length <= 50 || "Max. 50 characters",
        // counterName: (v) => v.length <= 50 || "Max. 50 characters",
      },

      statusOptions: [
        {activeInactive: 'Active'},
        {activeInactive: 'Inactive'}
      ],
      status: 'Active',

      notifOptions: [
        {option: 'Yes'},
        {option: 'No'}
      ],
      notif: 'No',
      closeOnContentClick: true,
    }),

  methods: {
    submit() {
      console.log(this.planningFor, this.status, this.date, this.sendNotif)
    },
    notifValue(returnValue) {
      return this.notif.option
    },
    isNotif() {
      
    },
  },
}
</script>

<style scoped>
    .planningFor {
      width: 165px;
    }
    .status {
      width: 165px;
    }
    .dueDate {
      width: 165px;
    }
    .sendNotif {
      width: 295px;
    }
    .sendTo {
      width: 500px;
    }
    .emailBody {
      width: 500px;
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
    .StartPlanning__checkbox{
      align-content:flex-start
    }
</style>

<style lang="scss">
  .v-card__text {
    color: unset !important;
  }
</style>
    
