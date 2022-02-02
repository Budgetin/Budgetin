<template>
  <v-card>
    <v-card-title class="text-h5" style="margin-bottom: 32px">
      <!-- {{ cardTitle }} a Planning -->
      Filter
      <v-spacer></v-spacer>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="FilterBox__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- ID ITFAM -->
          <v-col cols="6"> Planning For
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="FilterBox__field">
                <v-text-field
                  v-model="form.year"
                  placeholder="Input a Year"
                  outlined
                  return-object
                  :disabled="isView"
                  :rules="validation.required">
                </v-text-field>
              </div>
            </v-col>
          </v-col>

          <!-- PROJECT NAME -->
          <v-col cols="6"> Status <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="FilterBox__field">
                <v-select
                  v-model="form.is_active"
                  :items="statusInfoPlanning"
                  item-text="label"
                  item-value="id"
                  placeholder="Choose Active/Inactive"
                  outlined
                  return-object
                  :disabled="isView"
                  :rules="validation.statusRule">
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
                  <div class="FilterBox__field">
                    <v-text-field
                    ref="form"
                    v-model="form.due_date"
                    outlined
                    v-bind="attrs"
                    v-on="on"
                    placeholder="Pick a Date"
                    :disabled="isView"
                    :rules="validation.required">
                    </v-text-field>
                  </div>
                </template>
                <v-date-picker
                v-model="form.due_date"
                @input="menu = false"
                :min="new Date().toISOString().substr(0, 10)">
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
              <div class="FilterBox__field">
                <v-select
                  v-model="form.notification"
                  :items="statusNotification"
                  item-text="label"
                  item-value="id"
                  placeholder="Choose Yes/No"
                  outlined
                  return-object
                  :disabled="isView"
                  :rules="validation.notifRule">
                </v-select>
              </div>
            </v-col>
          </v-col>
        </v-row>

        <!-- SEND TO -->
        <v-container v-if="form.notification">
          <v-row no-gutters v-if="form.notification.id==1">
            <v-col> Send to <strong class="red--text">*</strong>
              <v-col no-gutters>
                <div class="sendTo">
                <v-select
                  :items="dataAllBiro"
                  v-model="form.biros"
                  item-text="code"
                  item-value="id, code"
                  placeholder="Choose Biro"
                  multiple
                  chips
                  outlined>
                </v-select>
                </div>
              </v-col>            
            </v-col>
          </v-row>

          <!-- E-MAIL BODY -->
          <v-row no-gutters v-if="form.notification.id==1">
            <v-col> E-mail Body
              <v-col>
                <div class="emailBody">
                  <v-textarea
                  v-model="form.body"
                  outlined
                  dense
                  :disabled="isView">
                  </v-textarea>
                </div>
              </v-col>
            </v-col>
          </v-row>
        </v-container>

        <!-- BUTTONS -->
        <v-row no-gutters>
          <v-col cols="12" align="right">
            <v-btn
              rounded
              outlined
              class="primary--text"
              @click="$emit('okClicked')"
              v-if="isView"
            >
              OK
            </v-btn>
            <v-btn
              rounded
              outlined
              class="primary--text"
              @click="$emit('cancelClicked')"
              v-if="!isView"
            >
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
  name: "FormFilterBox",
  props: ["form", "isNew", "isView"],

  data: () => ({
    //yearSubstring: new Date().getFullYear(),
    //due_date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    menu: null,
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
      // yearRule: v  => {
      //   //if (!v.trim()) return true;
      //   if (!isNaN(parseFloat(v)) && v >= 1000 && v <= 9999) return true;
      //   return 'Year has to be integer and contains 4 digits';
      // },
    },
  }),
  
  computed: {
    ...mapState("statusInfo", ["statusInfoPlanning"]),
    ...mapState("statusInfo", ["statusNotification"]),
    ...mapState("allBiro", ["getAllBiro", "dataAllBiro"]),

    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
  },

  methods: {
    onSubmit() {
      // console.log("Masuk Sini");
      let validate = this.$refs.form.validate();
      // console.log("Masuk Let Validate");
      if (validate) {
        const payload = {
          id: this.form.id,
          year: this.form.year,
          is_active: this.form.is_active.id,
          due_date: this.form.due_date + "T23:59",
          notification: this.form.notification.id ? 1 : 0,
          biros: this.form.biros ? this.form.biros : 0,
          body: this.form.body ? this.form.body : 0,
        };
        // console.log("ID"+this.form.id);
        // console.log("Year"+this.form.year);
        // console.log("DueDate"+this.form.due_date);
        // console.log("is_active"+this.form.is_active.id);
        // console.log("sendNotif"+this.form.notification.id);
        // console.log("Biro"+this.form.biros);
        // console.log("body"+this.form.body);
        this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
        this.$refs.form.reset()
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
  .FilterBox__checkbox{
    align-content:flex-start
  }
  .FilterBox__form{
    width: auto;
    margin-left: 2% !important;
  }
  .FilterBox__select{
    min-width: 500px;
  }
  .FilterBox__field {
    min-width: 165px;
  }
  .FilterBox__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
</style>
    
