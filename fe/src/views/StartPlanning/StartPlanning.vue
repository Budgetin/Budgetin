<template>
    <v-app id="start-planning">
        <v-container class="start-planning__container outer-container">
            <v-card>
                <v-card-title>
                    <v-row no-gutters>
                        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                        <v-subheader class="start-planning__header">Start Planning</v-subheader>
                        </v-col>
                    </v-row>
                </v-card-title>

                <v-row no-gutters>
                    <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                        <v-data-table
                            :headers="headers"
                            :items="desserts"
                            :search="search">
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
                            @cancelClicked="onCancel">
                        </form-coa>
                    </v-dialog>
                </v-row>
            </v-card>
        </v-container>
    </v-app>
</template>

<script>
import FormStartPlanning from '@/components/StartPlanning/FormStartPlanning';
export default {
    components: {
        FormStartPlanning
    },
    data() {
        return {
            search: "",
            headers: [
                { text: "ID", value: "id",width: "20%"},
                { text: "Planning For", value: "planningFor" ,width: "20%"},
                { text: "Status", value: "status" },
                { text: "Notification", value: "notification" },
                { text: "Updated By", value: "updatedBy" },
                { text: "Updated Date", value: "updatedDate" },
                { text: "Actions", value: "actions", align: "center", sortable: false },
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
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 3,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 4,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 5,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 6,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 7,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 8,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 9,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
                },
                {
                    id: 10,
                    planningFor: "2023",
                    status: "Active",
                    notification: "Yes",
                    updatedBy: "Phang Willy",
                    updatedDate: "30 November 2022",
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
    },
};
</script>

<style lang="scss" scoped>
.searchBar {
    width: 400px;
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