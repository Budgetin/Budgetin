<template>
    <v-app id="monitor-planning">
        <v-container class="monitor-planning__container outer-container">
            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <v-subheader class="monitor-planning__header">Monitoring Status</v-subheader>
                </v-col>
            </v-row>

            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <v-data-table
                    :headers="dataTable.headers"
                    :loading="loadingGetMonitorPlanning"
                    :items="monitorData"
                    :search="search">
                        <template v-slot:top>
                            <v-toolbar-title>
                                <v-row class="mb-5" no-gutters>
                                    <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
                                        <v-text-field
                                            class="monitor-planning__input"
                                            v-model="search"
                                            append-icon="mdi-magnify"
                                            label="Search"
                                            single-line
                                            hide-details>
                                        </v-text-field>
                                    </v-col>
                                </v-row>
                            </v-toolbar-title>
                        </template>

                        <!-- VIEW/EDIT PLANNING -->  
                        <template v-slot:[`item.actions`]="{ item }">
                            <router-link
                                style="text-decoration: none"
                                :to="{
                                name: 'ViewStatusMonitoring',
                                params: { id: item.id },
                                }">
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

                        <!-- <template v-slot:[`item.status`]="{ item }">
                            <binary-status-chip :boolean="item.status"> </binary-status-chip>
                        </template> -->
                    </v-data-table>
                </v-col>
            </v-row>
        </v-container>
    </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import BinaryStatusChip from "@/components/chips/BinaryStatusChip";
export default {
    name: "MonitorPlanning",
    components: {
        BinaryStatusChip
    },
    watch: {},
    data: () => ({
        dialog: false,
        search: "",
        dataTable: {
            headers: [
                { text: "Group", value: "biro.group_code"},
                { text: "Sub-Group", value: "biro.sub_group_code"},
                { text: "Biro", value: "biro.code"},
                { text: "PIC", value: "pic_initial"},
                { text: "Updated Date", value: "updated_at"},
                { text: "Status", value: "monitoring_status"},
                { text: "Action", value: "actions", align: "center", sortable: false},
            ],
        },

        monitorData: [],
        
        form: {
            id: "",
            biro: {
                id: "",
                ithc_biro: "",
                code: "",
                sub_group_code: "",
                group_code: "",
                name: "",
            },
            monitoring_status: "",
            is_deleted: "",
            planning_id: "",
            pic_employee_id: "",
            pic_initial: "",
            pic_display_name: "",
            updated_by: "",
            updated_at: "",
        },
        alert: {
            show: false,
            success: null,
            title: null,
            subtitle: null,
        },
    }),

    created() {
        this.getEdittedItem();
        this.getMonitorPlanningById(this.$route.params.id);
        this.setBreadcrumbs();
    },
    
    computed: {
        cardTitle() {
            return this.isNew ? "Add" : this.isView ? "View" : "Edit";
        },
        ...mapState("monitorPlanning", ["loadingGetMonitorPlanning"]),
    },

    methods: {
        ...mapActions("monitorPlanning", ["getMonitorPlanningById", "postMonitorPlanning"]),

        setBreadcrumbs() {
            let param = this.isView ? "View Monitor Planning Status" : "Edit Monitor Planning Status";
            this.$store.commit("breadcrumbs/SET_LINKS", [
                {
                    text: "Monitor Planning Status",
                    link: true,
                    exact: true,
                    disabled: false,
                    to: {
                        name: "MonitorPlanning",
                    },
                },
            ]);
        },
        
        getEdittedItem() {
            this.getMonitorPlanningById(this.$route.params.id).then(() => {
            
            this.monitorData = JSON.parse(
                JSON.stringify(this.$store.state.monitorPlanning.edittedItem))
            });
        },

        onAdd() {
            this.dialog = !this.dialog;
        },
        onCancel() {
            this.dialog = false;
        },
        onSubmit(e) {
            this.postMonitorPlanning(e)
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
            this.alert.subtitle = "Monitoring Status has been saved successfully";
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
        
        onEdit(item) {
            this.$store.commit("monitorPlanning/SET_EDITTED_ITEM", item);
        },
        onOK() {
            return this.$router.go(-1);
        }
    }
};
</script>

<style lang="scss" scoped>
.searchBar {
    width: 400px;
}
.data-table {
    margin: 40px;
}

#monitor-planning {
    .monitor-planning__header {
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
    }

    .monitor-planning__input {
        padding: 10px 32px;
    }

    .monitor-planning__btn {
        text-align: end;

        button {
            margin: 10px 32px;
        }
    }

    .monitor-planning__container {
        padding: 24px 0px;
        // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
    }

    .monitor-planning__card {
        button {
            width: 8rem;
        }
    }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#monitor-planning {
    .monitor-planning__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .monitor-planning__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>