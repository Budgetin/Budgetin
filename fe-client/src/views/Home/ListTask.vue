<template>
  <v-app id="list-task">
    <v-container class="list-task__container outer-container">
      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-subheader class="list-task__header">My Task</v-subheader>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
          <v-data-table
            :items="dataHome"
            :loading="loadingGetHome"
            :headers="dataTable.headers"
            :search="search"
          >
            <template v-slot:top>
              <v-toolbar-title>
                <v-row class="mb-5" no-gutters>
                  <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
                    <v-text-field
                      class="list-task__input"
                      v-model="search"
                      append-icon="mdi-magnify"
                      label="Search"
                      hide-details
                    >
                    </v-text-field>
                  </v-col>
                </v-row>
              </v-toolbar-title>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <router-link
                style="text-decoration: none"
                :to="{
                  name: 'EditSubmittedPlanning',
                  params: { id: item.id },
                }"
              >
                <v-tooltip bottom v-if="item.planning.is_active">
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" color="#16B1FF">
                      mdi-lead-pencil
                    </v-icon>
                  </template>
                  <span>Edit</span>
                </v-tooltip>

                <v-tooltip bottom v-if="!item.planning.is_active">
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" color="#16B1FF" @click="onView(item)">
                      mdi-eye
                    </v-icon>
                  </template>
                  <span>View</span>
                </v-tooltip>
              </router-link>
            </template>

            <template v-slot:[`item.monitoring_status`]="{ item }">
              <binary-status-task-chip :data="item.monitoring_status"> </binary-status-task-chip>
            </template>

          </v-data-table>
        </v-col>
      </v-row>

    </v-container>

  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import BinaryStatusTaskChip from "@/components/chips/BinaryStatusTaskChip.vue";

export default {
  name: "Home",
  components: {BinaryStatusTaskChip},
  watch: {},
  data: () => ({
    dialog: false,
    search: "",
    isEdit: false,
    dataTable: {
      headers: [
        { text: "Planning For", value: "planning.year"},
        { text: "Biro", value: "biro.code"},
        { text: "Status", value: "monitoring_status", align: "center"},
        { text: "Due Date", value: "due_date"},
        { text: "Update By", value: "updated_by"},
        { text: "Update Date", value: "updated_at"},
        { text: "Actions", value: "actions", align: "center", sortable: false ,width: "4rem"},
      ]
    },
  }),
  created() {
    this.getHome();
    this.setBreadcrumbs();
  },
  computed: {
    ...mapState("home", ["loadingGetHome", "dataHome"]),
  },
  methods: {
    ...mapActions("home", ["getHome"]),
    setBreadcrumbs() {
      this.$store.commit("breadcrumbs/SET_LINKS", [
        {
          text: "Home",
          link: false,
          exact: true,
          disabled: true,
        },
      ]);
    },
    onView(item){

    }    
  }
}
</script>

<style>
button {
  min-width: 2rem;
}
</style>

<style lang="scss" scoped>
#list-task {
  .list-task__header {
    padding-left: 32px;
    font-size: 1.25rem;
    font-weight: 600;
  }

  .list-task__input {
    padding: 10px 32px;
  }

  .list-task__btn {
    text-align: end;

    button {
      margin: 10px 32px;
    }
  }

  .list-task__container {
    padding: 24px 0px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 8px;
  }

}

@media only screen and (max-width: 600px) {
  /* For mobile phones */
  #list-task {
    .list-task__btn {
      text-align: center;
      padding: 0px 32px;

      button {
        width: 100%;
        margin: 0px 0px 32px 0px;
      }
    }
    .list-task__card {
      flex-direction: column;
      button {
        width: 16rem !important;
        margin-left: unset !important;
      }
    }
  }
}
</style>
