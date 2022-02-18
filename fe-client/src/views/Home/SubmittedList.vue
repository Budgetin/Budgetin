<template>
  <v-app id="submitted-planning">
    <v-container class="submitted-planning__container outer-container">
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-subheader class="submitted-planning__header"
            >My Planning</v-subheader
          >
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-data-table
            :items="dataTable.value"
            :loading="dataTable.loadingTable"
            :headers="dataTable.Listheader"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
                    <v-text-field
                      class="submitted-planning__input"
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Search"
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
                    class="submitted-planning__btn"
                    justify="end"
                    v-if="taskInfo"
                  >
                    <v-btn
                      color="#16B1FF"
                      v-if="
                        taskInfo.planning.is_active &&
                        taskInfo.monitoring_status != 'Submitted'
                      "
                      class="white--text"
                      @click="onSubmit"
                      >Submit</v-btn
                    >
                    <v-btn
                      color="#7E73FF"
                      v-if="
                        taskInfo.planning.is_active &&
                        taskInfo.monitoring_status != 'Submitted'
                      "
                      @click="onAddOption"
                      class="white--text"
                      >Add Planning</v-btn
                    >
                    <v-btn outlined @click="ondownload">Download </v-btn>
                  </v-col>
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'ViewMyPlanning',
                  params: { id_project: item.project_detail.project.id },
                }"
              >
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" color="#16B1FF"> mdi-eye </v-icon>
                  </template>
                  <span>View/Edit</span>
                </v-tooltip>
              </router-link>
            </template>

            <template v-slot:[`item.is_budget`]="{ item }">
              <binary-yes-no-chip :boolean="item.is_budget">
              </binary-yes-no-chip>
            </template>
            <template v-slot:[`item.project_detail.project.is_tech`]="{ item }">
              <binary-yes-no-chip
                :boolean="item.project_detail.project.is_tech"
              >
              </binary-yes-no-chip>
            </template>


            <!-- start data bentuk nominal -->
            <template v-slot:[`item.project_detail.project.total_investment_value`]="{ item }">
              <span>{{ numberWithDots(item.project_detail.project.total_investment_value) }}</span>
            </template>
            <template v-slot:[`item.planning_nominal`]="{ item }">
              <span>{{ numberWithDots(item.planning_nominal) }}</span>
            </template>
            <template v-slot:[`item.planning_q1`]="{ item }">
              <span>{{ numberWithDots(item.planning_q1) }}</span>
            </template>
            <template v-slot:[`item.planning_q2`]="{ item }">
              <span>{{ numberWithDots(item.planning_q2) }}</span>
            </template>
            <template v-slot:[`item.planning_q3`]="{ item }">
              <span>{{ numberWithDots(item.planning_q3) }}</span>
            </template>
            <template v-slot:[`item.planning_q4`]="{ item }">
              <span>{{ numberWithDots(item.planning_q4) }}</span>
            </template>
          <!-- end data bentuk nominal -->

          </v-data-table>
        </v-col>
      </v-row>

      <!-- Input Option -->
      <v-row no-gutters>
        <v-dialog v-model="dialogChoose" persistent width="25rem">
          <form-choose-project-type
            @newClicked="onAddNew"
            @existingClicked="onAddExisting"
            @cancelClicked="onCancel"
          >
          </form-choose-project-type>
        </v-dialog>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="loadingGetDownloadPlanning" persistent width="25rem">
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
import FormChooseProjectType from "@/components/Home/FormChooseProjectType";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert";
import BinaryYesNoChip from "@/components/chips/BinaryYesNoChip";
import formatting from "@/mixins/formatting";
export default {
  name: "SubmittedList",
  components: { SuccessErrorAlert, BinaryYesNoChip, FormChooseProjectType },
  mixins: [formatting],
  watch: {},
  data: () => ({
    dialogChoose: false,
    search: "",
    taskInfo: null,
    dataTable: {
      loadingTable: true,
      value: [],
      Listheader: [
        {
          text: "Actions",
          value: "actions",
          align: "center",
          sortable: false,
          width: "5rem",
        },
        { text: "For", value: "project_detail.planning.year", width: "5rem" },
        { text: "Project ID", value: "project_detail.dcsp_id", width: "7rem" },
        {
          text: "Project Name",
          value: "project_detail.project.project_name",
          width: "8rem",
        },
        {
          text: "Biro",
          value: "project_detail.project.biro.code",
          width: "5rem",
        },
        {
          text: "ID ITFAM",
          value: "project_detail.project.itfam_id",
          width: "7rem",
        },
        {
          text: "Project Description",
          value: "project_detail.project.project_description",
          width: "10rem",
        },
        {
          text: "Tech / Non Tech",
          value: "project_detail.project.is_tech",
          width: "9rem",
        },
        {
          text: "Product ID",
          value: "project_detail.project.product.product_code",
          width: "7rem",
        },
        {
          text: "RCC",
          value: "project_detail.project.biro.rcc",
          width: "5rem",
        },
        {
          text: "Project Type",
          value: "project_detail.project_type",
          width: "9rem",
        },
        { text: "Is Budget", value: "is_budget", width: "7rem" },
        { text: "COA", value: "coa", width: "5rem" },
        {
          text: "Capex/Opex",
          value: "expense_type",
          width: "8rem",
        },
        {
          text: "Start Year",
          value: "project_detail.project.start_year",
          width: "7rem",
        },
        {
          text: "End Year",
          value: "project_detail.project.end_year",
          width: "7rem",
        },
        {
          text: "Total Investment",
          value: "project_detail.project.total_investment_value",
          width: "9rem",
        },
        {
          text: "Budget This Year",
          value: "planning_nominal",
          width: "9rem",
        },
        { text: "Planning Q1", value: "planning_q1", width: "5rem" },
        { text: "Planning Q2", value: "planning_q2", width: "5rem" },
        { text: "Planning Q3", value: "planning_q3", width: "5rem" },
        { text: "Planning Q4", value: "planning_q4", width: "5rem" },
        {
          text: "Strategy",
          value: "project_detail.project.product.strategy",
          width: "6rem",
        },
        { text: "Created By", value: "created_by", width: "7rem" },
        { text: "Updated At", value: "updated_at", width: "8rem" },
      ],
    },
    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
  }),
  created() {
    this.setBreadcrumbs();
    this.getTaskInformationById();
    this.getSubmittedItem();
  },
  computed: {
    ...mapState("home", ["loadingGetDownloadPlanning"]),
  },
  methods: {
    ...mapActions("home", [
      "getTaskById",
      "getSubmittedTaskById",
      "submitPlanning",
      "downloadPlanning",
    ]),
    setBreadcrumbs() {
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Home",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "Home",
          },
        },
        {
          text: "Submitted List",
          disabled: true,
        },
      ]);
    },
    getTaskInformationById() {
      this.getTaskById(this.$route.params.id).then(() => {
        this.taskInfo = JSON.parse(
          JSON.stringify(this.$store.state.home.dataTaskById)
        );
      });
    },
    getSubmittedItem() {
      this.getSubmittedTaskById(this.$route.params.id).then(() => {
        this.dataTable.value = JSON.parse(
          JSON.stringify(this.$store.state.home.dataSubmittedTask)
        );
        this.dataTable.loadingTable =
          this.$store.state.home.loadingGetSubmittedTaskItem;
      });
    },
    onSubmit() {
      if (this.taskInfo) {
        this.submitPlanning(this.taskInfo)
          .then(() => {
            this.getTaskInformationById();
            this.onSaveSuccess("Planning Submitted");
          })
          .catch((error) => {
            this.onSaveError(error);
          });
      }
    },
    onAddOption() {
      this.dialogChoose = !this.dialogChoose;
    },
    onCancel() {
      this.dialogChoose = false;
    },
    onAddNew() {
      let param = this.$route.params.id;
      return this.$router.push("/home/" + param + "/submitted/new");
    },
    onAddExisting() {
      let param = this.$route.params.id;
      return this.$router.push("/home/" + param + "/submitted/new");
    },
    ondownload() {
      if (this.taskInfo) {
        this.downloadPlanning(this.taskInfo)
          .then(() => {
            this.onSaveSuccess("Check Your Download Folder");
          })
          .catch((error) => {
            this.onSaveError(error);
          });
      }
    },
    onSaveSuccess(message) {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Success";
      this.alert.subtitle = message;
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
  },
};
</script>

<style scoped>
::v-deep button {
  min-width: 2rem;
}

::v-deep table > tbody > tr:hover td:nth-child(1),
::v-deep table > tbody > tr:hover td:nth-child(2),
::v-deep table > tbody > tr:hover td:nth-child(3),
::v-deep table > tbody > tr:hover td:nth-child(4) {
  background: #eeeeee;
}

::v-deep table > tbody > tr > td:nth-child(1),
::v-deep table > thead > tr > th:nth-child(1) {
  position: sticky !important;
  position: -webkit-sticky !important;
  /* max-width: 4.1rem; */
  left: 0;
  z-index: 9;
  background: white;
}
::v-deep table > thead > tr > th:nth-child(1) {
  z-index: 10;
}
::v-deep table > tbody > tr > td:nth-child(2),
::v-deep table > thead > tr > th:nth-child(2) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 5rem;
  z-index: 9;
  background: white;
}
::v-deep table > thead > tr > th:nth-child(2) {
  z-index: 10;
}
::v-deep table > tbody > tr > td:nth-child(3),
::v-deep table > thead > tr > th:nth-child(3) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 10rem;
  z-index: 9;
  background: white;
}
::v-deep table > thead > tr > th:nth-child(3) {
  z-index: 10;
}
::v-deep table > tbody > tr > td:nth-child(4),
::v-deep table > thead > tr > th:nth-child(4) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 17rem;
  z-index: 9;
  background: white;
}
::v-deep table > thead > tr > th:nth-child(4) {
  z-index: 10;
}

::v-deep .choose-project-type_box {
  border: 3px rgb(228, 228, 228) solid;
  border-radius: 20px;
  padding: 0.5rem;
  width: 10rem;
  font-weight: 600;
  cursor: pointer;
}

::v-deep .choose-project-type_box:hover {
  border: 3px rgb(93, 158, 243) solid;
  border-radius: 20px;
  padding: 0.5rem;
  width: 10rem;
  cursor: pointer;
}
</style>

<style lang="scss" scoped>
#submitted-planning {
  .submitted-planning__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .submitted-planning__input {
    padding: 10px 32px;
  }

  .submitted-planning__btn {
    text-align: end;

    button {
      margin: 10px 10px;
    }
  }

  .submitted-planning__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #submitted-planning {
    .submitted-planning__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .submitted-planning__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
