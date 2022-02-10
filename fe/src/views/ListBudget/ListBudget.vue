<template>
  <v-app id="list-budget">
    <v-container class="list-budget__container outer-container">
      <v-row no-gutters>
          <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
              <v-subheader class="list-budget__header">List of Budgets</v-subheader>
          </v-col>
        <v-tabs 
          v-model="tab" 
          color="blue" 
          centered
          grow
          @change="onTabChange"
          >
            <v-tab
                v-for="item in items"
                :key="item"
                align="center">
                {{ item }}
            </v-tab>
        </v-tabs>
      </v-row>
      <v-row no-gutters>
        
      </v-row>
            <v-divider></v-divider>
      <br>
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>

          <!---------------------------- ACTIVE ---------------------------->

          <v-data-table
            :items="dataListBudget"
            :loading="loadingGetListBudget"
            :headers="listColumn"
            :search="search"
            v-if="tab==0"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="3" lg="3" no-gutters>
                    <v-text-field
                      class="list-budget__input"
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Search"
                      hide-details
                    >
                    </v-text-field>
                  </v-col>

                  <v-col
                    cols="6"
                    xs="6"
                    sm="2"
                    md="1"
                    lg="1"
                    no-gutters
                    class="column__btn"
                  >
                    <v-btn class="mt-2" color="primary" @click="chooseColumn">
                      <v-icon>mdi-table-column-plus-before</v-icon>
                    </v-btn>
                  </v-col>

                  <v-col
                    cols="12"
                    xs="12"
                    sm="6"
                    md="8"
                    lg="8"
                    no-gutters
                    class="list-budget__btn"
                  >
                    <v-btn rounded color="primary" @click="onUpdateRealization">Update Realization </v-btn>
                    <v-btn rounded color="primary" @click="onInputOption"> Add Budget </v-btn>
                    <v-btn rounded color="primary" @click="onExport">
                          Download
                      </v-btn>
                  </v-col>
                  
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'EditListPlanning',
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
            <template v-slot:[`item.is_budget`]="{ item }">
                <binary-yes-no-chip :boolean="item.is_budget"> </binary-yes-no-chip>
            </template>
            <template v-slot:[`item.project_detail.project.is_tech`]="{ item }">
                <binary-yes-no-chip :boolean="item.project_detail.project.is_tech"> </binary-yes-no-chip>
            </template>
          </v-data-table>

          <!---------------------------- INACTIVE ---------------------------->

          <v-data-table
            :items="dataListInactiveBudget"
            :loading="loadingGetListInactiveBudget"
            :headers="listColumn"
            :search="search"
            v-if="tab==1"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="3" lg="3" no-gutters>
                    <v-text-field
                      class="list-budget__input"
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Search"
                      hide-details
                    >
                    </v-text-field>
                  </v-col>

                  <v-col
                    cols="6"
                    xs="6"
                    sm="2"
                    md="1"
                    lg="1"
                    no-gutters
                    class="column__btn"
                  >
                    <v-btn class="mt-2" color="primary" @click="chooseColumn">
                      <v-icon>mdi-table-column-plus-before</v-icon>
                    </v-btn>
                  </v-col>

                  <v-col
                    cols="12"
                    xs="12"
                    sm="6"
                    md="8"
                    lg="8"
                    no-gutters
                    class="list-budget__btn"
                  >
                    <v-btn rounded color="primary" @click="onUpdateRealization" v-if="tab==0">Update Realization </v-btn>
                    <v-btn rounded color="primary" @click="onInputOption" v-if="tab==0"> Add Budget </v-btn>
                    <v-btn rounded color="primary" @click="onExport" v-if="tab==0">
                          <v-icon left> mdi-export-variant </v-icon>
                          Download
                      </v-btn>
                  </v-col>
                  
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'EditListPlanning',
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
            <template v-slot:[`item.is_budget`]="{ item }">
                <binary-yes-no-chip :boolean="item.is_budget"> </binary-yes-no-chip>
            </template>
            <template v-slot:[`item.project_detail.project.is_tech`]="{ item }">
                <binary-yes-no-chip :boolean="item.project_detail.project.is_tech"> </binary-yes-no-chip>
            </template>
          </v-data-table>
        </v-col>
      </v-row>

      <v-row no-gutters>
          <v-dialog v-model="dialogChoose" persistent width="25rem">
              <form-choose-project-type
              @newClicked="onNewClick"
              @existingClicked="onExistingClick"
              @cancelClicked="onCancel">
              </form-choose-project-type>
          </v-dialog>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="dialogUpload" persistent width="25rem">
          <upload-file-budget
            @cancelClicked="onCancel"
            @uploadClicked="uploadBudget">
          </upload-file-budget>
        </v-dialog>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="dialogUpdateRealization" persistent width="25rem">
          <upload-file-realization
            @cancelClicked="onCancel"
            @uploadClicked="uploadRealization">
          </upload-file-realization>
        </v-dialog>
      </v-row>

            <v-row no-gutters>
          <v-dialog v-model="isLoading" persistent width="25rem">
            <v-card >
              <v-card-title class="d-flex justify-center">
                Loading
              </v-card-title>

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
          <v-dialog v-model="inputOption" persistent width="25rem">
            <v-card>
              <v-card-title>
                How to Input
                <v-spacer></v-spacer>
                <v-btn icon small @click="onCancel">
                  <v-icon color="primary"> mdi-close </v-icon>
                </v-btn>
              </v-card-title>

              <v-card-text>
                <v-row no-gutters align="center">
                  <v-col cols="6" class="mt-2">
                    <v-btn rounded color="primary" @click="onUpload"> Upload Excel </v-btn>
                  </v-col>
                  <v-col cols="6" class="mt-2">
                    <v-btn rounded color="primary" @click="onAdd"> Input Form </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-dialog>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="dialog" scrollable persistent width="37.5rem">
          <column-option
            :data="dataTable.Listheader"
            :selectedColumn="listColumn"
            @closeClicked="onClose"
          />
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
import ColumnOption from "@/components/ListBudget/ColumnOption";
import FormChooseProjectType from "@/components/ListBudget/FormChooseProjectType"
import UploadFileBudget from "@/components/ListBudget/UploadFileBudget"
import UploadFileRealization from "@/components/ListBudget/UploadFileRealization"
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert";
import BinaryYesNoChip from "@/components/chips/BinaryYesNoChip";
export default {
  name: "ListBudget",
  components: {SuccessErrorAlert,ColumnOption,FormChooseProjectType,BinaryYesNoChip,UploadFileBudget,UploadFileRealization},
  watch: {},
  data: () => ({
    dialog: false,
    dialogUpdateRealization :false,
    dialogChoose: false,
    dialogUpload: false,
    inputOption : false,
    isEdit: false,
    search: "",
    tab: null,
    items: ['Active', 'Inactive'],
    dataTable: {
      selectedHeader: [],
      Listheader: [
        { text: "Project ID", value: "project_detail.dcsp_id", width: "7rem" },
        { text: "Project Name", value: "project_detail.project.project_name", width: "8rem" },
        { text: "Biro", value: "project_detail.project.biro.code", width: "5rem" },
        { text: "ID ITFAM", value: "project_detail.project.itfam_id", width: "7rem" },
        {
          text: "Project Description",
          value: "project_detail.project.project_description",
          width: "10rem",
        },
        { text: "Tech / Non Tech", value: "project_detail.project.is_tech", width: "9rem" },
        {
          text: "Product ID",
          value: "project_detail.project.product.product_code",
          width: "7rem",
        },
        { text: "RCC", value: "project_detail.project.biro.rcc", width: "5rem" },
        { text: "Project Type", value: "project_detail.project_type", width: "9rem" },
        { text: "Is Budget", value: "is_budget", width: "7rem" },
        { text: "COA", value: "coa", width: "5rem" },
        {
          text: "Capex/Opex",
          value: "expense_type",
          width: "8rem",
        },
        { text: "Start Year", value: "project_detail.project.start_year", width: "7rem" },
        { text: "End Year", value: "project_detail.project.end_year", width: "7rem" },
        {
          text: "Total Investment",
          value: "project_detail.project.total_investment_value",
          width: "9rem",
        },
        {
          text: "Budget This Year",
          value: "budget_nominal",
          width: "9rem",
        },
        { text: "Planning Q1", value: "planning_q1", width: "5rem" },
        { text: "Planning Q2", value: "planning_q2", width: "5rem" },
        { text: "Planning Q3", value: "planning_q3", width: "5rem" },
        { text: "Planning Q4", value: "planning_q4", width: "5rem" },
        { text: "Realization Jan", value: "realization_jan", width: "5rem" },
        { text: "Realization Feb", value: "realization_feb", width: "5rem" },
        { text: "Realization Mar", value: "realization_mar", width: "5rem" },
        { text: "Realization Apr", value: "realization_apr", width: "5rem" },
        { text: "Realization May", value: "realization_may", width: "5rem" },
        { text: "Realization Jun", value: "realization_jun", width: "5rem" },
        { text: "Realization Jul", value: "realization_jul", width: "5rem" },
        { text: "Realization Aug", value: "realization_aug", width: "5rem" },
        { text: "Realization Sep", value: "realization_sep", width: "5rem" },
        { text: "Realization Oct", value: "realization_oct", width: "5rem" },
        { text: "Realization Nov", value: "realization_nov", width: "5rem" },
        { text: "Realization Dec", value: "realization_dec", width: "5rem" },
        {
          text: "Strategy",
          value: "project_detail.project.product.strategy",
          width: "6rem",
        },
        { text: "Created By", value: "created_by", width: "7rem" },
        { text: "Updated At", value: "updated_at", width: "8rem" },
      ],
    },
    form: {
    id: "",
    is_budget: "",
    expense_type: "",
    planning_nominal: "",
    planning_q1: "",
    planning_q2: "",
    planning_q3: "",
    planning_q4: "",
    realization_jan: "",
    realization_feb: "",
    realization_mar: "",
    realization_apr: "",
    realization_may: "",
    realization_jun: "",
    realization_jul: "",
    realization_aug: "",
    realization_sep: "",
    realization_oct: "",
    realization_nov: "",
    realization_dec: "",
    switching_in: "",
    switching_out: "",
    top_up: "",
    returns: "",
    allocate: "",
    coa: "",
    project_detail: {
        id: "",
        dcsp_id: "",
        planning: {
            id: "",
            year: "",
            due_date: "",
            is_active: ""
        },
        project: {
            id: "",
            project_name: "",
            project_description: "",
            itfam_id: "",
            is_tech: "",
            start_year: "",
            end_year: "",
            total_investment_value: "",
            product: {
                id: "",
                product_code: "",
                strategy: ""
            },
            biro: {
                id: "",
                code: "",
                name: "",
                rcc: ""
            }
        },
        project_type: ""
    },
    created_by: "",
    updated_by: "",
    created_at: "",
    updated_at: ""
},
    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
  }),
  created() {
    this.getListBudget();
    this.getListInactiveBudget();
    this.getSelectedHeader();
    this.setBreadcrumbs();
  },
  computed: {
    ...mapState("listBudget", ["loadingGetListBudget", "loadingGetListInactiveBudget", "dataListBudget", "dataListInactiveBudget", "isLoading"]),
    ...mapState("choosedColumn", ["listColumn"]),
  },
  methods: {
    ...mapActions("listBudget", ["getListBudget", "getListInactiveBudget", "postListBudget","importBudget","importRealization"]),
    getSelectedHeader() {
      if (this.listColumn.length == 1) {
        this.dataTable.selectedHeader = [].concat(this.dataTable.Listheader);
        this.dataTable.selectedHeader.splice(0, 0, {
          text: "For",
          value: "project_detail.planning.year",
          width: "5rem",
        });
        this.setColumn(this.dataTable.selectedHeader);
      }
    },
    setBreadcrumbs() {
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "List Budget",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "ListBudget",
          },
        }
      ]);
    },
    setColumn(list) {
      this.$store.commit("choosedColumn/SET_LIST", list);
    },
    chooseColumn() {
      //this.dataTable.selectedHeader.splice(0, 2);
      this.dialog = !this.dialog;
    },
    onEdit(item) {
      this.$store.commit("listBudget/SET_EDITTED_ITEM", item);
    },
    onCancel() {
      this.dialogChoose = false;
      this.inputOption = false;
      this.dialogUpload = false;
      this.dialogUpdateRealization = false;
      
    },
    onClose(e) {
      this.dataTable.selectedHeader.splice(0, 1);
      this.dialog = false;
      if (e.length > 0) {
        this.dataTable.selectedHeader = [];
        for (let i = 0; i < e.length; i++) {
          this.dataTable.selectedHeader.push(e[i]);
        }
        this.dataTable.selectedHeader.splice(0, 1, {
          text: "For",
          value: "project_detail.planning.year",
          width: "5rem",
        });
        this.setColumn(this.dataTable.selectedHeader);
      }
    },
    onSaveSuccess() {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Save Success";
      this.alert.subtitle = "Budget has been saved successfully";
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
    uploadBudget(data){
      this.importBudget(data)
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.dialog = false;
          this.alert.show = true;
          this.alert.success = false;
          this.alert.title = "Upload Failed";
          this.alert.subtitle = error.message;
        });
    },
    uploadRealization(data){
      this.importRealization(data)
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.dialog = false;
          this.alert.show = true;
          this.alert.success = false;
          this.alert.title = "Upload Failed";
          this.alert.subtitle = error.message;
        });
    },
    onExport() {
      this.downloadBudget()
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.dialog = false;
          this.alert.show = true;
          this.alert.success = false;
          this.alert.title = "Download Failed";
          this.alert.subtitle = error.message;
        });
    },
    onUpload(){
      this.dialogUpload = true;
      this.inputOption = false;
    },

    onInputOption(){
      this.inputOption = true;
    },

    onUpdateRealization(){
      this.dialogUpdateRealization = true;
    },

    onAdd() {
      this.dialogChoose = !this.dialogChoose;
      this.inputOption = false;
      this.dialogUpload = false;
    },
    onNewClick(){
      return this.$router.push("/listBudget/new");
    },
    onExistingClick(){
      return this.$router.push("/listBudget/existing");
    },
    onTabChange(){
      console.log(this.tab);
    }
  },
};
</script>

<style>
button {
  min-width: 2rem;
}

table > tbody > tr:hover td:nth-child(1),
table > tbody > tr:hover td:nth-child(2),
table > tbody > tr:hover td:nth-child(3),
table > tbody > tr:hover td:nth-child(4){
  background: #EEEEEE;
}

table > tbody > tr > td:nth-child(1),
table > thead > tr > th:nth-child(1) {
  position: sticky !important;
  position: -webkit-sticky !important;
  /* max-width: 4.1rem; */
  left: 0;
  z-index: 9;
  background: white;
}
table > thead > tr > th:nth-child(1) {
  z-index: 10;
}
table > tbody > tr > td:nth-child(2),
table > thead > tr > th:nth-child(2) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 5rem;
  z-index: 9;
  background: white;
}
table > thead > tr > th:nth-child(2) {
  z-index: 10;
}
table > tbody > tr > td:nth-child(3),
table > thead > tr > th:nth-child(3) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left:12rem;
  z-index: 9;
  background: white;
}
table > thead > tr > th:nth-child(3) {
  z-index: 10;
}
table > tbody > tr > td:nth-child(4),
table > thead > tr > th:nth-child(4) {
  position: sticky !important;
  position: -webkit-sticky !important;
  left: 20rem;
  z-index: 9;
  background: white;
}
table > thead > tr > th:nth-child(4) {
  z-index: 10;
}
</style>

<style lang="scss" scoped>
#list-budget {
  .list-budget__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .list-budget__input {
    padding: 10px 32px;
  }

  .list-budget__btn {
    text-align: end;

    button {
      margin: 10px 10px;
    }
  }

  .list-budget__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }
}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #list-budget {
    .list-budget__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .list-budget__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
