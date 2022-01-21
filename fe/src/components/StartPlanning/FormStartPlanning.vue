<template>
  <v-row justify="center">
    <v-col align="right" class="mr-7">
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
              <!-- PLANNING FOR -->
              <v-row no-gutters>
                <v-col cols="6"> Planning For <strong class="red--text">*</strong> </v-col>
                <v-col cols="6">
                  <v-text-field
                    outlined
                    dense
                    :disabled="isAdd"
                    :rules="[validation.required]">
                  </v-text-field>
                </v-col>
              </v-row>

              <!-- STATUS -->
              <v-row no-gutters>
                <v-col cols="6"> Status <strong class="red--text">*</strong> </v-col>
                <v-col cols="6">
                  <v-text-field
                    outlined
                    dense
                    :disabled="isAdd"
                    :rules="[validation.required]">
                  </v-text-field>
                </v-col>
              </v-row>

              <!-- DUE DATE -->  
              <v-row>
                <v-col cols="6"> Due Date <strong class="red--text">*</strong> </v-col>
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
              </v-row>

              <!-- SEND NOTIFICATION -->
              <v-row no-gutters>
                <v-col cols="6" class="mb-5">
                  <v-checkbox
                    v-model="checkbox"
                    :label="`Send Notification`"
                  ></v-checkbox>
                </v-col>
              </v-row>

              <!-- SEND TO -->
              <v-row no-gutters v-if="checkbox">
                <v-col cols="6"> Send to </v-col>
                <v-col cols="6">
                  <v-text-field
                    outlined
                    dense
                    :disabled="isAdd">
                  </v-text-field>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-col md="2" offset-md="7">
              <div class="cancelBtn">
                <v-btn
                  rounded
                  outlined
                  color="blue-grey darken-2"
                  @click="dialog = false"
                  style="width:100px;">
                  Cancel
                </v-btn>
              </div>
            </v-col>
            <v-col>
              <div class="saveBtn">
                <v-btn
                  rounded
                  color="cyan"
                  dark
                  @click="submit"
                  style="width:100px;"
                  class="saveBtn--text">
                  Save
                </v-btn>
              </div>
            </v-col>
          </v-card-actions>
        </v-card>
    </v-col>  
  </v-row>
</template>

<script>
export default {
  name: "FormStartPlanning",
  props: ["isView"],

  data() {
    return {
      dialog: false,
      planningFor: '',
      status: '',
      sendNotif: '',
      date: null,
    }
  },
  data: () => ({
      date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      menu: false,
      dialog: false,

      checkbox: false,
      validation: {
        required: (v) => !!v || "This field is required",
        // counterInitial: (v) => v.length <= 50 || "Max. 50 characters",
        // counterName: (v) => v.length <= 50 || "Max. 50 characters",
      },

      links: [
        { title: 'Yes', route: '/' },
        { title: 'No', route: '/' },
      ],
      closeOnContentClick: true,
    }),

  methods: {
    submit() {
      console.log(this.planningFor, this.status, this.date, this.sendNotif)
    },
  },
}
</script>

<style scoped>
    .planningFor {
        width: 295px;
    }
    .status {
        width: 295px;
    }
    .dueDate {
        width: 295px;
    }
    .sendNotif {
        width: 295px;
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
    .FormCOA__checkbox{
      align-content:flex-start
    }
</style>

<style lang="scss">
  .v-card-title {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
  }
  button {
    min-width: 8rem;
  }
</style>
    
