<template>
    <v-app id="list-project">
        <v-container class="list-project__container outer-container">
            <!-- <v-row no-gutters>
                <v-tabs v-model="tab" color="primary" align-with-title>
                    <v-tabs-slider color="grey"></v-tabs-slider>
                    <v-tab
                        v-for="item in items"
                        :key="item">
                        {{ item }}
                    </v-tab>
                </v-tabs>
            </v-row>
            <v-divider></v-divider> -->
            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <v-subheader class="list-project__header">Project List</v-subheader>
                </v-col>
            </v-row>

            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <!-- height = "80vh"
                    fixed-header -->
                    <v-data-table
                    :headers="dataTable.headers"
                    :loading="loadingGetListProject"
                    :items="dataListProject"
                    :search="search">
                        <template v-slot:top>
                            <v-toolbar-title>
                                <v-row class="mb-5" no-gutters>
                                    <v-col cols="12" xs="12" sm="6" md="4" lg="4" no-gutters>
                                        <v-row no-gutters>
                                            <v-text-field
                                            class="list-project__input"
                                            v-model="search"
                                            append-icon="mdi-magnify"
                                            label="Search"
                                            single-line
                                            hide-details>
                                            </v-text-field>
                                        </v-row>
                                    </v-col>

                                    <!-- <v-col no-gutters>
                                        <v-btn color="primary" @click="onFilter" class="mt-4">
                                            <v-icon> mdi-filter-outline </v-icon>
                                        </v-btn>
                                    </v-col> -->
                                </v-row>
                            </v-toolbar-title>
                        </template>
                                    
                        <template v-slot:[`item.actions`]="{ item }">
                            <!-- VIEW PROJECT -->
                            <router-link
                                style="text-decoration: none"
                                :to="{
                                    name: 'ViewListProject',
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
                    </v-data-table>
                </v-col>
            </v-row>
        </v-container>
    </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import FormListProject from '@/components/CompListProject/FormListProject';
export default {
    name: "ListProject",
    components: {
        FormListProject
    },
    watch: {},
    data: () => ({
        tab: null,
        items: ['Active', 'Inactive'],
        
        isEdit: false,
        search: "",
        dataTable: {
            headers: [
                { text: "Action", value: "actions", align: "center", sortable: false, width: "3rem"},
                // { text: "ID", value: "id", width: "4rem"},
                { text: "ID ITFAM", value: "itfam_id", width: "8rem"},
                { text: "Project Name", value: "project_name", width: "14rem"},
                // { text: "Project Description", value: "project_description", width: "10rem"},
                { text: "RCC", value: "biro.rcc", width: "5rem"},
                { text: "Biro", value: "biro.code", width: "5rem"},
                { text: "Product Code", value: "product.product_code", width: "8rem"},
                { text: "Product Name", value: "product.product_name", width: "16rem"},
                { text: "Start Year", value: "start_year", width: "6rem"},
                { text: "End Year", value: "end_year", width: "6rem"},
            ],
        },

        form: {
            id: "",
            project_name: "",
            project_description: "",
            product: {
                id: "",
                product_code: "",
                product_name: "",
            },
            // product: [],
            itfam_id: "",
            biro: {
                id: "",
                rcc: "",
                code: "",
            },
            // biro: [],
            is_tech: "",
            start_year: "",
            end_year: "",
            total_investment_value: ""
        },
    }),

    created() {
        this.getListProject();
        this.setBreadcrumbs();
    },
    computed: {
        ...mapState("listProject", ["loadingGetListProject", "dataListProject"]),
    },
    methods: {
        ...mapActions("listProject", ["getListProject"]),

        setBreadcrumbs() {
            let param = this.isView ? "View Project Detail" : "Edit Project";
            this.$store.commit("breadcrumbs/SET_LINKS", [
                {
                    text: "Project List",
                    link: true,
                    exact: true,
                    disabled: false,
                    to: {
                        name: "ListProject",
                    },
                },
            ]);
        },
        onCancel() {
            this.dialog = false;
        },
        onFilter() {

        },
        onEdit(item) {
            this.$store.commit("listProject/SET_EDITTED_ITEM", item);
        },
        onOK() {
            return this.$router.go(-1);
        },
    }
};
</script>

<style scoped>
.v-data-table /deep/ .sticky-header {
    position: sticky;
    top: 0;
}
</style>

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

    .list-project__switch {
        margin-left: 600px;
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