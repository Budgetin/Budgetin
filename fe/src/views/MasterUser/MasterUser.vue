<template>
  <v-app id="master-user">
    <v-container class="master-user__container outer-container">
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-subheader class="master-user__header">Master User</v-subheader>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-icon>mdi-trash</v-icon>
          <v-data-table
            :items="dataMasterUser"
            :loading="loadingGetMasterUser"
            :headers="dataTable.headers"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
                    <v-text-field
                      class="master-user__input"
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
                    class="master-user__btn"
                  >
                    <v-btn rounded color="primary" @click="logout">
                      logOut
                    </v-btn>
                  </v-col>
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'EditMasterUser',
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
              <binary-status-chip :boolean="item.is_active"> </binary-status-chip>
            </template>

          </v-data-table>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="dialog" persistent width="37.5rem">
          <form-User
          :form="form"
          :isView="false"
          :isNew="true"
          :dataMasterUser="dataMasterUser"
          @editClicked="onEdit"
          @cancelClicked="onCancel"
          @submitClicked="onSubmit"
          ></form-User>
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
import FormUser from "@/components/MasterUser/FormUser";
import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";
import BinaryStatusChip from "@/components/chips/BinaryStatusChip";
export default {
  name: "MasterUser",
  components: {FormUser,BinaryStatusChip,SuccessErrorAlert},
  watch: {},
  data: () => ({
    dialog: false,
    isEdit: false,
    search: "",
    dataTable: {
      headers: [
        { text: "Username", value: "username"},
        { text: "Role", value: "role"},
        { text: "Status", value: "is_active", align: "center"},
        { text: "Update By", value: "update_by"},
        { text: "Update Date", value: "updated_at"},
        { text: "Actions", value: "actions", align: "center", sortable: false },
      ]
    },
    form: {
      id: "",
      username: "",
      role: "",
      is_active: "",
    },
    alert: {
      show: false,
      success: null,
      title: null,
      subtitle: null,
    },
  }),
  created() {
    this.getMasterUser();
    // this.getMasterStrategy();
    // this.setBreadcrumbs();
  },
  computed: {
    ...mapState("masterUser", ["loadingGetMasterUser", "dataMasterUser"]),
    
    // ...mapState("masterStrategy", ["loadingGetMasterStrategy", "dataMasterStrategy"]),
  },
  methods: {
    ...mapActions("masterUser", ["getMasterUser", "postMasterUser"]),
    ...mapActions("login", ["logOut"]),

    // ...mapActions("masterStrategy", ["getMasterStrategy", "postMasterStrategy"]),
    logout(){
      // console.log("logout");
      this.logOut();
    },
    onAdd() {
      this.dialog = !this.dialog;
    },
    onEdit(item) {
      this.$store.commit("masterUser/SET_EDITTED_ITEM", item);
    },    
    onCancel() {
      this.dialog = false;
    },
    onSubmit(e) {
      this.postMasterUser(e)
        .then(() => {
          // this.onSaveSuccess();
        })
        .catch((error) => {
          // this.onSaveError(error);
        });
    },
    onSaveSuccess() {
      this.dialog = false;
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Save Success";
      this.alert.subtitle = "Master Source has been saved successfully";
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
  }
}
</script>

<style>
button {
  min-width: 2rem;
}
</style>

<style lang="scss" scoped>
#master-user {
  .master-user__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .master-user__input {
    padding: 10px 32px;
  }

  .master-user__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .master-User__container {
    padding: 24px 0px;
    // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #master-User {
    .master-User__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .master-User__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
