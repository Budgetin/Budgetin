<template>
  <v-app id="master-coa">
    <v-container class="master-coa__container outer-container">
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-subheader class="master-coa__header">Master COA</v-subheader>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-data-table
            :items="dataMasterCoa"
            :loading="loadingGetMasterCoa"
            :headers="dataTable.headers"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
                    <v-text-field
                      class="master-coa__input"
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
                    class="master-coa__btn"
                  >
                    <v-btn rounded color="primary" @click="onAdd">
                      Add COA
                    </v-btn>
                  </v-col>
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'EditMasterCoa',
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
        <v-dialog v-model="dialog" persistent width="37.5rem">
          <form-coa
          :form="form"
          :isView="false"
          :isNew="true"
          :dataMasterCoa="dataMasterCoa"
          @editClicked="onEdit"
          @cancelClicked="onCancel"
          @submitClicked="onSubmit"
          ></form-coa>
        </v-dialog>
      </v-row>

    </v-container>
  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import FormCoa from "@/components/MasterCOA/FormCoa";
export default {
  name: "MasterCoa",
  components: {FormCoa},
  watch: {},
  data: () => ({
    dialog: false,
    isEdit: false,
    search: "",
    dataTable: {
      headers: [
        { text: "COA", value: "name"},
        { text: "Hyperion Name", value: "hyperion_name"},
        { text: "Update By", value: "update_by"},
        { text: "Update Date", value: "update_date"},
        { text: "Actions", value: "actions", align: "center", sortable: false },
      ]
    },
    form: {
      id: "",
      name: "",
      definition: "",
      hyperion_name: "",
      is_capex: "",
      minimum_item_origin: "",
    },
  }),
  created() {
    this.getMasterCoa();
    // this.setBreadcrumbs();
  },
  computed: {
    ...mapState("masterCoa", ["loadingGetMasterCoa", "dataMasterCoa"]),
  },
  methods: {
    ...mapActions("masterCoa", ["getMasterCoa", "postMasterCoa"]),
    onAdd() {
      this.dialog = !this.dialog;
    },
    onEdit(item) {
      this.$store.commit("masterCoa/SET_EDITTED_ITEM", item);
    },    
    onCancel() {
      this.dialog = false;
    },
    onSubmit(e) {
      this.postMasterCoa(e)
        .then(() => {
          this.onSaveSuccess();
        })
        .catch((error) => {
          this.onSaveError(error);
        });
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
#master-coa {
  .master-coa__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .master-coa__input {
    padding: 10px 32px;
  }

  .master-coa__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .master-coa__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #master-coa {
    .master-coa__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .master-coa__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
