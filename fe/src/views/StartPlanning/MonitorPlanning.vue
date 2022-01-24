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
                        :headers="headers"
                        :items="desserts"
                        :search="search"
                        class="data-table">
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
                                    
                        <template v-slot:[`item.actions`]="{ item }">
                            <!-- VIEW/EDIT PLANNING -->
                            <router-link
                                style="text-decoration: none"
                                :to="{
                                name: 'ViewStatusMonitoring',
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
        </v-container>
    </v-app>
</template>

<script>
export default {
    watch: {},
    data() {
        return {
            dialog: false,
            search: "",
            headers: [
                { text: "No", value: "no", width: "5%" },
                { text: "Group", value: "group", width: "15%" },
                { text: "Sub-Group", value: "subGroup", width: "15%" },
                { text: "Biro", value: "biro", width: "15%" },
                { text: "PIC", value: "pic", width: "15%" },
                { text: "Updated Date", value: "updatedDate", width: "20%" },
                { text: "Status", value: "status", width: "17%" },
                { text: "Action", value: "actions", align: "center", sortable: false, width: "10%"},
            ],
            desserts: [
                {
                    no: 1,
                    group: "GAQ",
                    subGroup: "ARC",
                    biro: "ARC A",
                    pic: "JRE",
                    updatedDate: "5 January 2022",
                    status: "Submitted",
                },
                {
                    no: 2,
                    group: "APT",
                    subGroup: "CTS",
                    biro: "CTS A",
                    pic: "PLN",
                    updatedDate: "2 January 2022",
                    status: "Draft",
                },
                {
                    no: 3,
                    group: "DIS",
                    subGroup: "DIS *",
                    biro: "DIS A",
                    pic: "YOH",
                    updatedDate: "15 January 2022",
                    status: "Submitted",
                },
                {
                    no: 4,
                    group: "GAQ",
                    subGroup: "SAQ",
                    biro: "SAQ B",
                    pic: "WAN",
                    updatedDate: "",
                    status: "To-Do",
                },
                {
                    no: 5,
                    group: "APT",
                    subGroup: "CTS",
                    biro: "CTS B",
                    pic: "LCD",
                    updatedDate: "5 January 2022",
                    status: "Draft",
                },
                {
                    no: 6,
                    group: "APT",
                    subGroup: "CTS",
                    biro: "CTS C",
                    pic: "DVD",
                    updatedDate: "3 January 2022",
                    status: "Submitted",
                },
                {
                    no: 7,
                    group: "GAQ",
                    subGroup: "SAQ",
                    biro: "SAQ A",
                    pic: "WAN",
                    updatedDate: "4 January 2022",
                    status: "Submitted",
                },
                {
                    no: 8,
                    group: "DIS",
                    subGroup: "DIS B",
                    biro: "DIS B *",
                    pic: "APE",
                    updatedDate: "",
                    status: "To-Do",
                },
                {
                    no: 9,
                    group: "APT",
                    subGroup: "ITX",
                    biro: "ITX A",
                    pic: "IWA",
                    updatedDate: "8 January 2022",
                    status: "Draft",
                },
                {
                    no: 10,
                    group: "IIO",
                    subGroup: "SIS",
                    biro: "SIS B",
                    pic: "WIB",
                    updatedDate: "",
                    status: "To-Do",
                },
                {
                    no: 11,
                    group: "DMO",
                    subGroup: "IMO",
                    biro: "IMO A",
                    pic: "HND",
                    updatedDate: "5 January 2022",
                    status: "Submitted",
                },
                {
                    no: 12,
                    group: "IIO",
                    subGroup: "SIS",
                    biro: "SIS C",
                    pic: "ANT",
                    updatedDate: "5 January 2022",
                    status: "Draft",
                },
            ],
        };
    },

    methods: {
        onCancel() {
            this.dialog = false;
        },
        onView() {
            
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