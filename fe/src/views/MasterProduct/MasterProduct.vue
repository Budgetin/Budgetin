<template>
  <v-app id="master-product">
    <v-container class="master-product__container outer-container">
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-subheader class="master-product__header">Master Product</v-subheader>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-data-table
            :items="dataMasterProduct"
            :loading="loadingGetMasterProduct"
            :headers="dataTable.headers"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
                    <v-text-field
                      class="master-product__input"
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
                    class="master-product__btn"
                  >
                    <v-btn rounded color="primary" @click="onAdd">
                      Add Product
                    </v-btn>
                  </v-col>
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'EditMasterProduct',
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
          </v-data-table>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="inputOption" persistent width="37.5rem">
          <method-input-option
           @cancelClicked="onCancel"
           @formClicked="onForm"
           @uploadClicked="onUpload"
          >
          </method-input-option>
        </v-dialog>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="uploadDialog" persistent width="37.5rem">
          <upload-file-product
            @cancelClicked="onCancel"
            @uploadClicked="onSubmitUpload"
            @downloadClicked="onDownload"
          >
          </upload-file-product>
        </v-dialog>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="loadingImportProductTemplate" persistent width="25rem">
          <v-card>
            <v-card-title class="d-flex justify-center"> Loading </v-card-title>
            <v-card-text>
              <v-row no-gutters class="d-flex justify-center">
                <v-progress-circular
                  :size="70"
                  :width="7"
                  color="blue"
                  indeterminate
                ></v-progress-circular>
              </v-row>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="formDialog" persistent width="37.5rem">
          <form-Product
          :form="form"
          :isView="false"
          :isNew="true"
          :dataMasterProduct="dataMasterProduct"
          :dataMasterStrategy="dataMasterStrategy"
          @editClicked="onEdit"
          @cancelClicked="onCancel"
          @submitClicked="onSubmit"
          ></form-Product>
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
import MethodInputOption from "@/components/MethodInputOption"
import FormProduct from "@/components/MasterProduct/FormProduct";
import UploadFileProduct from "@/components/MasterProduct/UploadFileProduct";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
export default {
  name: "MasterProduct",
  components: {FormProduct,SuccessErrorAlert, MethodInputOption, UploadFileProduct},
  watch: {},
  data: () => ({
    inputOption:false,
    formDialog: false,
    uploadDialog:false,
    dialog: false,
    isEdit: false,
    search: "",
    dataTable: {
      headers: [
        { text: "Product Code", value: "product_code"},
        { text: "Product", value: "product_name"},
        { text: "IT Strategy", value: "strategy.name"},
        { text: "Update By", value: "updated_by"},
        { text: "Update Date", value: "updated_at"},
        { text: "Actions", value: "actions", align: "center", sortable: false,width: "4rem" },
      ]
    },
    form: {
      id: "",
      product_code: "",
      product_name: "",
      strategy:{
        id:"",
        name:""
      },
    },
    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
  }),
  created() {
    this.getMasterProduct();
    this.getMasterStrategy();
    this.setBreadcrumbs();
  },
  computed: {
    ...mapState("masterProduct", ["loadingGetMasterProduct", "dataMasterProduct", "loadingImportProductTemplate"]),
    ...mapState("masterStrategy", ["loadingGetMasterStrategy", "dataMasterStrategy"]),
  },
  methods: {
    ...mapActions("masterProduct", ["getMasterProduct", "postMasterProduct", "importProduct", "importTemplateProduct"]),
    ...mapActions("masterStrategy", ["getMasterStrategy", "postMasterStrategy"]),
    setBreadcrumbs() {
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Master Product",
          link: true,
          exact: true,
          disabled: false,
          to: {
            name: "MasterProduct",
          },
        },
      ]);
    },
    onDownload(){
      this.importTemplateProduct()
        .then(() => {
          // this.onDownloadSuccess();
        })
        .catch((error) => {
          this.onDownloadError(error);
        });
    },
    onAdd() {
      // this.dialog = !this.dialog;
      this.inputOption = true;
    },
    onUpload(){
      this.inputOption = false;
      this.formDialog = false;
      this.uploadDialog = true;
    },
    onSubmitUpload(file){
      this.importProduct(file)
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.onSaveError(error);
        });
    },
    onForm(){
      this.inputOption = false;
      this.formDialog = true;
      this.uploadDialog = false;
    },
    onEdit(item) {
      this.$store.commit("masterProduct/GET_MASTER_PRODUCT_BY_ID_SUCCESS", item);
    },    
    onCancel() {
      // this.dialog = false;
      this.inputOption = false;
      this.formDialog = false;
      this.uploadDialog = false;
    },
    onSubmit(e) {
      this.postMasterProduct(e)
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.onSaveError(error);
        });
    },
    onSaveSuccess() {
      this.formDialog = false;
      this.uploadDialog = false;
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Save Success";
      this.alert.subtitle = "Master Source has been saved successfully";
    },
    onSaveError(error) {
      this.formDialog = false;
      this.uploadDialog = false;
      this.alert.show = true;
      this.alert.success = false;
      this.alert.title = "Save Failed";
      this.alert.subtitle = error;
    },
    onDownloadSuccess() {
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Download Success";
      this.alert.subtitle = "Product Template has been downloaded successfully";
    },
    onDownloadError(error) {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = false;
      this.alert.title = "Download Failed";
      this.alert.subtitle = error;
    },
    onAlertOk() {
      this.alert.show = false;
    },
  }
}
</script>

<style>
button {
  min-width: 2rem;
}
</style>

<style lang="scss" scoped>
#master-product {
  .master-product__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .master-product__input {
    padding: 10px 32px;
  }

  .master-product__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .master-product__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #master-product {
    .master-product__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .master-product__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
