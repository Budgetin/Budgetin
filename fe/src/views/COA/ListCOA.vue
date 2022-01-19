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
          <v-data-table :items="desserts" :headers="headers" :search="search">
            
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
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" color="primary" @click="onEdit(item)">
                      mdi-eye
                    </v-icon>
                  </template>
                  <span>View/Edit</span>
                </v-tooltip>
            </template>

          </v-data-table>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-dialog v-model="dialog" persistent width="37.5rem">
          <form-coa
          @cancelClicked="onCancel"
          ></form-coa>
        </v-dialog>
      </v-row>

    </v-container>
  </v-app>
</template>

<script>
import FormCoa from "@/components/MasterCOA/FormCoa";
export default {
  components: {FormCoa},
  data() {
    return {
      dialog: false,
      search: "",
      headers: [
        { text: "COA", value: "coa",width: "20%"},
        { text: "Hyperion Name", value: "hyperion" ,width: "20%"},
        { text: "Update By", value: "update_by" },
        { text: "Update Date", value: "update_date" },
        { text: "Status", value: "status" },
        { text: "Actions", value: "actions", align: "center", sortable: false },
      ],
      desserts: [
        {
          id: 1,
          coa: "Consultant",
          hyperion: "XVI I.3.b HONORARIUM CONSULTANT",
          update_by: "Phang Willy",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 2,
          coa: "Hardware",
          hyperion: "l. Computer and Machinery I",
          update_by: "Jeffry Setiawan",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 3,
          coa: "Software",
          hyperion: "p. Software Khusus",
          update_by: "Phang Willy",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 4,
          coa: "Maintenance Hardware",
          hyperion: "XVI A.6.5 KOMPUTER",
          update_by: "Jeffry Setiawan",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 5,
          coa: "Maintenance Software",
          hyperion: "XVI F.7 SOFTWARE",
          update_by: "Phang Willy",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 6,
          coa: "Gedung",
          hyperion: "h. Gedung Dalam Pembangunan",
          update_by: "Jeffry Setiawan",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 7,
          coa: "Tanah",
          hyperion: "Tanah",
          update_by: "Phang Willy",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 8,
          coa: "Sewa Gedung",
          hyperion: "Sewa Gedung",
          update_by: "Jeffry Setiawan",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 9,
          coa: "Pemeliharaan Gedung & Perabotan",
          hyperion:
            "XVI A.6.2 GEDUNG, GUDANG",
          update_by: "Phang Willy",
          update_date: "30 November 2021",
          status: "active",
        },
        {
          id: 10,
          coa: "Keperluan Kantor Lainnya",
          hyperion: "XVI A.2.1 n. LAINNYA",
          update_by: "Jeffry Setiawan",
          update_date: "30 November 2021",
          status: "active",
        },
      ],
    };
  },
  methods: {
    onAdd() {
      this.dialog = !this.dialog;
    },
    onCancel() {
      this.dialog = false;
    }
  }
};
</script>
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

  .master-coa__card {
    button {
      width: 8rem;
    }
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
