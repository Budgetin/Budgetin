<template>
  <v-card>
    <v-card-title class="mb-5">
      {{ cardTitle }} a Planning
      <v-spacer></v-spacer>
      <v-btn v-if="isView" icon small @click="$emit('editClicked')">
        <v-icon color="primary"> mdi-square-edit-outline </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" class="StartPlanning__form" lazy-validation @submit.prevent="onSubmit">
        <v-row no-gutters>
          <!-- PLANNING FOR -->
          <v-col cols="6"> Planning For <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="StartPlanning__field">
                <v-select
                v-model="form.year"
                :items="planningFor"
                placeholder="Choose Year"
                outlined
                return-object
                dense
                :disabled="isView"
                :rules="validation.required">
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
              <div class="StartPlanning__field">
                <v-select
                v-model="form.is_active"
                :items="statusInfoPlanning"
                item-text="label"
                item-value="id"
                placeholder="Choose Active/Inactive"
                outlined
                return-object
                dense
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
                  <div class="StartPlanning__field">
                    <v-text-field
                    ref="form"
                    v-model="form.due_date"
                    outlined
                    v-bind="attrs"
                    v-on="on"
                    dense
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

          <!-- SEND NOTIFICATION View/Edit -->
          <v-col cols="6"> Send Notification <strong class="red--text">*</strong>
            <v-col
              class="d-flex"
              cols="12"
              sm="6">
              <div class="StartPlanning__field">
                <v-select
                v-model="form.notification"
                :items="statusNotification"
                item-text="label"
                item-value="id"
                placeholder="Choose Yes/No"
                outlined
                return-object
                dense
                :disabled="isView"
                :rules="validation.required">
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
                :items="dataAllBiroItHc"
                v-model="selected"
                item-text="code"
                item-value="id"
                placeholder="Choose Biro"
                multiple
                chips
                outlined
                :rules="validation.selectRequired">
                  <template v-slot:prepend-item>
                    <v-list-item
                      ripple
                      @mousedown.prevent
                      @click="toggle"
                      :rules="validation.required">
                      <v-list-item-action>
                        <v-icon :color="selected.length > 0 ? 'indigo darken-4' : ''">
                          {{ icon }}
                        </v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>
                          Select All
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <v-divider class="mt-2"></v-divider>
                  </template>
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
  name: "FormStartPlanning",
  props: ["form", "isNew", "isView"],

  data: () => ({
    year: new Date().getFullYear(),
    selected: [],
    selectAll: [],
    menu: null,
    validation: {
      required: [
        (v) => !!v || "This field is required"
      ],
      targetRule: [
        v => /^[0-9.,]+$/.test(v) || "This field is numbers only",
      ],
      yearRule: [
        v => { if (!isNaN(parseFloat(v)) && v >= 1000 && v <= 9999) return true;
        return 'Year has to be integer and contains 4 digits'; }
      ],
      selectRequired: [
        (v) =>  v.length > 0 || "This field is required",
      ]
    },
  }),

  computed: {
    ...mapState("statusInfo", ["statusInfoPlanning"]),
    ...mapState("statusInfo", ["statusNotification"]),
    ...mapState("allBiroItHc", ["getAllBiroItHc", "dataAllBiroItHc"]),

    cardTitle() {
      return this.isNew ? "Add" : this.isView ? "View" : "Edit";
    },
    errorMsg() {
      return this.$store.state.source.errorMsg;
    },
    icon () {
      if (this.selected.length === this.dataAllBiroItHc.length ) return "mdi-close-box";
      if (this.selected.length != this.dataAllBiroItHc.length ) return "mdi-minus-box";
      return 'mdi-checkbox-blank-outline'
    },
    planningFor() {
      return Array.from({length: 10}, (value, index) => this.year + index)
    }
  },

  methods: {
    onSubmit() {
      let validate = this.$refs.form.validate();
      if (validate) {
        if (this.selectAll.length != 0) {
          const payload = {
            id: this.form.id,
            year: this.form.year,
            is_active: this.form.is_active.id,
            due_date: this.form.due_date + "T23:59",
            // notification: this.form.notification.id ? 1 : 0,
            notification: this.form.notification.id,
            // biros: this.selected ? this.selected : 0,
            biros: this.selectAll,
            // body: this.form.body ? this.form.body : 0,
            body: this.form.body,
          };
          this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
          console.log(this.selectAll);
        } else {
          const payload = {
            id: this.form.id,
            year: this.form.year,
            is_active: this.form.is_active.id,
            due_date: this.form.due_date + "T23:59",
            // notification: this.form.notification.id ? 1 : 0,
            notification: this.form.notification.id,
            // biros: this.selected ? this.selected : 0,
            biros: this.selected,
            // body: this.form.body ? this.form.body : 0,
            body: this.form.body,
          };
          this.$emit("submitClicked", JSON.parse(JSON.stringify(payload)));
          // console.log(this.selected);
        };
        this.$refs.form.reset();
      }
    },
    onCancel() {
      this.dialog = false;
    },
    onOK() {
      return this.$router.go(-1);
    },
    toggle () {
      this.$nextTick(() => {
        if (this.selected.length === this.dataAllBiroItHc.length) {
          this.selected = [];
        } else {
          this.selected = this.dataAllBiroItHc.slice();
          this.selectAll = [];
          for(let i=0; i < this.selected.length; i++) {
            this.selectAll.push(this.selected[i].id);
          };
        }
      })
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
  .StartPlanning__field {
    min-width: 165px;
  }
  .StartPlanning__btn {
    text-align: end;
    button {
      margin: 10px 32px;
      min-width: 8rem;
    }
  }
</style>
    
