<template>
  <v-app id="start-planning">
    <v-container class="start-planning__container outer-container">
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-subheader class="start-planning__header"
            >List of Created Plannings</v-subheader
          >
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <!-- :sort-by.sync="sortBy"
                    :sort-desc.sync="sortDesc" -->
          <v-data-table
            :headers="dataTable.headers"
            :loading="loadingGetStartPlanning"
            :items="dataStartPlanning"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
                    <v-text-field
                      class="start-planning__input"
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Search"
                      single-line
                      hide-details
                    >
                    </v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    xs="12"
                    sm="6"
                    md="8"
                    lg="8"
                    no-gutters
                    class="start-planning__btn"
                  >
                    <v-btn rounded color="primary" @click="onAdd">
                      + Start New Planning
                    </v-btn>
                  </v-col>
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <!-- MONITOR PLANNING -->
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'MonitorPlanning',
                  params: { id: item.id },
                }"
              >
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon
                      class="ma-3"
                      v-on="on"
                      color="primary"
                      @click="onMonitor(item)"
                    >
                      mdi-monitor
                    </v-icon>
                  </template>
                  <span>Monitor</span>
                </v-tooltip>
              </router-link>

              <!-- VIEW/EDIT PLANNING -->
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'ViewPlanning',
                  params: { id: item.id },
                }"
              >
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" color="primary" @click="onEdit(item)">
                      mdi-eye
                    </v-icon>
                  </template>
                  <span>View/Edit</span>
                </v-tooltip>
              </router-link>
            </template>

            <template v-slot:[`item.is_active`]="{ item }">
              <binary-status-chip
                :boolean="item.is_active"
              ></binary-status-chip>
            </template>

            <template v-slot:[`item.notification`]="{ item }">
              <binary-yes-no-chip
                :boolean="item.notification"
              ></binary-yes-no-chip>
            </template>
          </v-data-table>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="loadingPostPatchStartPlanning" persistent width="25rem">
          <v-card>
            <v-card-title class="d-flex justify-center"> Loading </v-card-title>

            <v-card-text>
              <v-row no-gutters class="d-flex justify-center">
                <v-progress-circular
                  :size="70"
                  :width="7"
                  color="purple"
                  indeterminate
                ></v-progress-circular>
              </v-row>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="dialog" persistent width="40rem">
          <form-start-planning
            :form="form"
            :isNew="true"
            :isView="false"
            :dataAllBiroItHc="dataAllBiroItHc"
            :dataStartPlanning="dataStartPlanning"
            @editClicked="onEdit"
            @cancelClicked="onCancel"
            @submitClicked="onSubmit"
            @okClicked="onOK"
          >
          </form-start-planning>
        </v-dialog>
      </v-row>
    </v-container>

    <success-error-alert
      :success="alert.success"
      :show="alert.show"
      :title="alert.title"
      :subtitle="alert.subtitle"
      @okClicked="onAlertOk"
    />
  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import FormStartPlanning from "@/components/CompStartPlanning/FormStartPlanning";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
import BinaryStatusChip from "@/components/chips/BinaryStatusChip";
import BinaryYesNoChip from "@/components/chips/BinaryYesNoChip";
export default {
  name: "StartPlanning",
  components: {
    FormStartPlanning,
    SuccessErrorAlert,
    BinaryStatusChip,
    BinaryYesNoChip,
  },
  watch: {},
  data: () => ({
    dialog: false,
    isEdit: false,
    search: "",
    dataTable: {
      headers: [
        // { text: "ID", value: "id" },
        { text: "Planning For", value: "year", width: "8rem" },
        { text: "Status", value: "is_active", width: "6rem" },
        { text: "Due Date", value: "due_date", width: "8rem" },
        { text: "Notification", value: "notification", width: "8rem" },
        { text: "Updated By", value: "updated_by", width: "8rem" },
        { text: "Updated Date", value: "updated_at", width: "8rem" },
        {
          text: "Action",
          value: "actions",
          align: "center",
          sortable: false,
          width: "8rem",
        },
      ],
    },
    sortBy: "id",
    sortDesc: false,
    form: {
      id: "",
      year: "",
      is_active: {
        id: null,
        label: "",
      },
      // is_active: "",
      created_by: "",
      updated_by: "",
      updated_at: "",
      //due_date: "",
      due_date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      // send_notification: "",
      notification: {
        id: null,
        label: "",
      },
      biros: [],
      body: "",
    },
    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
  }),

  created() {
    this.getStartPlanning();
    this.getMonitorPlanning();
    this.getAllBiroItHc();
    this.setBreadcrumbs();
  },

  computed: {
    ...mapState("startPlanning", [
      "loadingGetStartPlanning",
      "dataStartPlanning",
      "loadingPostPatchStartPlanning",
    ]),
    ...mapState("monitorPlanning", [
      "loadingGetMonitorPlanning",
      "dataMonitorPlanning",
    ]),
    ...mapState("allBiroItHc", ["dataAllBiroItHc"]),
  },

  methods: {
    ...mapActions("startPlanning", ["getStartPlanning", "postStartPlanning"]),
    ...mapActions("monitorPlanning", [
      "getMonitorPlanning",
      "postMonitorPlanning",
    ]),
    ...mapActions("allBiroItHc", ["getAllBiroItHc"]),

    setBreadcrumbs() {
      let param = this.isView ? "View Planning" : "Edit Planning";
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Start Planning",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "StartPlanning",
          },
        },
      ]);
    },

    onAdd() {
      this.dialog = !this.dialog;
    },
    onCancel() {
      this.dialog = false;
    },
    onSubmit(e) {
      this.postStartPlanning(e)
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.onSaveError(error);
        });
    },
    onSaveSuccess() {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Save Success";
      this.alert.subtitle = "Planning Data has been saved successfully";
    },
    onSaveError(error) {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = false;
      this.alert.title = "Save Failed";
      this.alert.subtitle = error;
    },
    onAlertOk() {
      this.alert.show = false;
    },
    onMonitor(item) {
      this.$store.commit("monitorPlanning/SET_EDITTED_ITEM", item);
    },
    onEdit(item) {
      this.$store.commit("startPlanning/SET_EDITTED_ITEM", item);
    },
    onOK() {
      return this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped>
.searchBar {
  width: 400px;
}
.data-table {
  margin: 40px;
}

#start-planning {
  .start-planning__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .start-planning__input {
    padding: 10px 32px;
  }

  .start-planning__btn {
    text-align: end;
    button {
      margin: 10px 32px;
    }
  }

  .start-planning__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

  .start-planning__card {
    button {
      width: 8rem;
    }
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #start-planning {
    .start-planning__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .start-planning__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
