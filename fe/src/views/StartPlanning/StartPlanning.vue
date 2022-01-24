<template>
    <v-app id="start-planning">
        <v-container class="start-planning__container outer-container">
            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                <v-subheader class="start-planning__header">List of Created Planning</v-subheader>
                </v-col>
            </v-row>

            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <v-data-table
                        :headers="headers"
                        :items="desserts"
                        :search="search"
                        class="data-table">
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
                                            hide-details>
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="12" xs="12" sm="6" md="8" lg="8" no-gutters class="start-planning__btn">
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
                                }">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on }">
                                        <v-icon  class="ma-3" v-on="on" color="primary" @click="onMonitor(item)">
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
                                }">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on }">
                                        <v-icon v-on="on" color="primary" @click="onView()">
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
                <v-dialog v-model="dialog" persistent width="40rem">
                    <form-start-planning
                        @cancelClicked="onCancel">
                    </form-start-planning>
                </v-dialog>
            </v-row>
        </v-container>
    </v-app>

    <!-- <template>
        <div id="page-id">
            {{item.id}}
        </div>
    </template> -->
</template>

<script>
import FormStartPlanning from '@/components/CompStartPlanning/FormStartPlanning';
export default {
    name: "CompStartPlanning",
    components: {
        FormStartPlanning
    },
    
    props: ['item.id'],
    
    watch: {},
    data() {
        return {
            // planningFor: this.$route.params.planningFor,
            // monitor: {},

            dialog: false,
            search: "",
            headers: [
                { text: "ID", value: "id", width: "5%" },
                { text: "Planning For", value: "planningFor", width: "10%" },
                { text: "Status", value: "status", width: "8%" },
                { text: "Notification", value: "notification", width: "8%" },
                { text: "Updated By", value: "updatedBy", width: "20%" },
                { text: "Updated Date", value: "updatedDate", width: "15%" },
                { text: "Action", value: "actions", align: "center", sortable: false, width: "10%"},
            ],
            desserts: [
                {
                    id: 1,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 2,
                    planningFor: "2022",
                    status: "Inactive",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2021",
                },
                {
                    id: 3,
                    planningFor: "2021",
                    status: "Inactive",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2020",
                },
                {
                    id: 4,
                    planningFor: "2020",
                    status: "Inactive",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2019",
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
        },
        // onMonitor(item) {
        //     console.log(item+"monitor");
        // },
        // onView(item) {
        //     console.log(item);
        // }
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

// style {
//     button {
//         min-width: 3rem !important;
//     }
// }

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