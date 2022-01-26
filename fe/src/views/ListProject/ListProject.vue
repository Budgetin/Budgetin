<template>
    <v-app id="list-project">
        <v-container class="list-project__container outer-container">
            <v-row no-gutters>
                <v-tabs v-model="tab" color="primary" align-with-title>
                    <v-tabs-slider color="grey"></v-tabs-slider>
                    <v-tab
                        v-for="item in items"
                        :key="item">
                        {{ item }}
                    </v-tab>
                </v-tabs>
            </v-row>
            <v-divider></v-divider>
            <v-row no-gutters style="margin-top: 16px">
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                <v-subheader class="list-project__header">List of Projects</v-subheader>
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
                                        <v-row>
                                        <v-text-field
                                            class="list-project__input"
                                            v-model="search"
                                            append-icon="mdi-magnify"
                                            label="Search"
                                            single-line
                                            hide-details>
                                        </v-text-field>

                                        <v-btn color="primary" @click="onFilter" class="mt-4">
                                            <v-icon>
                                                mdi-filter-outline
                                            </v-icon>
                                        </v-btn>
                                        </v-row>
                                    </v-col>
                                    
                                    <v-col cols="12" xs="12" sm="6" md="8" lg="8" no-gutters class="list-project__btn">
                                        <v-btn rounded color="primary" @click="onExport">
                                            <v-icon left>
                                                mdi-export-variant
                                            </v-icon>
                                            Export Data
                                        </v-btn>
                                    </v-col>
                                </v-row>
                            </v-toolbar-title>
                        </template>
                                    
                        <template v-slot:[`item.actions`]="{ item }">
                            <!-- VIEW/EDIT PLANNING -->
                            <router-link
                                style="text-decoration: none"
                                :to="{
                                name: 'ViewPlanning',
                                params: { id: item.id },
                                }">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on }">
                                        <v-icon v-on="on" color="primary" @click="onView">
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

            <!-- <v-row no-gutters>
                <v-dialog v-model="dialog" persistent width="40rem">
                    <form-list-project
                        @cancelClicked="onCancel">
                    </form-list-project>
                </v-dialog>
            </v-row> -->
        </v-container>
    </v-app>
</template>

<script>
import FormStartPlanning from '@/components/CompStartPlanning/FormStartPlanning';
export default {
    name: "CompStartPlanning",
    components: {
        FormStartPlanning
    },
    
    watch: {},
    data() {
        return {
            tab: null,
            items: ['Active', 'Inactive'],

            search: "",
            headers: [
                { text: "Action", value: "actions", align: "center", sortable: false, width: "7%"},
                { text: "ID ITFAM", value: "id", width: "10%" },
                { text: "Project Name", value: "project_name", width: "15%" },
                { text: "Project Description", value: "project_desc", width: "20%" },
                { text: "RCC", value: "rcc", width: "10%" },
                { text: "Biro", value: "code", width: "10%" },
            ],
            desserts: [
                {
                    id: "202300010",
                    project_name: "Prototype Re-design LAN ATM Pertokoan",
                    project_desc: "Merapikan LAN ATM EBC",
                    rcc: "093",
                    code: "NIS B",
                },
                {
                    id: "202300011",
                    project_name: "Wi-fi Cabang",
                    project_desc: "Access point untuk Future Branch",
                    rcc: "093",
                    code: "NIS B",
                },
                {
                    id: "202300012",
                    project_name: "Tool Fiber Optic",
                    project_desc: "Fiber Optic Tester",
                    rcc: "093",
                    code: "NIS A",
                },
                {
                    id: "202300013",
                    project_name: "Subduck BNDC Cibitung",
                    project_desc: "Zone fiber optic MM2100",
                    rcc: "093",
                    code: "NIS C",
                },
            ],
        };
    },

    methods: {
        onExport() {
        },
        onCancel() {
            this.dialog = false;
        },
        onMonitor() {
            console.log(item+"monitor");
        },
        onView() {
            console.log(item);
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

#list-project {
    .list-project__header {
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
    }

    .list-project__tab {
        margin-bottom: 32px;
    }

    .list-project__input {
        padding: 10px 32px;
    }

    .list-project__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }

    .list-project__container {
        padding: 24px 0px;
        // box-shadow: rgb(0 0 0 / 35%) 0px 5px 15px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
    }

    .list-project__card {
        button {
            width: 8rem;
        }
    }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#list-project {
    .list-project__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .list-project__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>