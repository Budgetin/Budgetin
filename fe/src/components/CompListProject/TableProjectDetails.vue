<template>
    <v-container>
        <v-row no-gutters style="margin-top: 16px">
            <v-subheader class="table-project-details__header" style="font-size: 1.25rem; font-weight: 600;">Project Details</v-subheader>
        </v-row>

        <v-row no-gutters>
            <v-col >
                <v-data-table
                :headers="dataTable.projectDetailsHeaders"
                :loading="status"
                :items="showItem">
                    <template v-slot:[`item.planning.is_active`]="{ item }">
                        <binary-status-chip :boolean="item.planning.is_active"></binary-status-chip>
                    </template>

                    <template v-slot:[`item.actions`]="{ item }">
                        <!-- EDIT PROJECT DETAIL -->
                        <router-link
                            style="text-decoration: none"
                            :to="{
                                name: 'ViewListProjectDetail',
                                params: { id_project_detail: item.id },
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
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import BinaryStatusChip from "@/components/chips/BinaryStatusChip";
export default {
    name: "TableProjectDetails",
    props: ["projectDetail"],
    components: {
        BinaryStatusChip
    },
    data: () => ({
        dialog: false,
        isEdit: false,
        isView: true,
        showItem: [],
        form: {
            id: "",
            created_by: "",
            updated_by: "",
            created_at: "",
            updated_at: "",
            itfam_id: "",
            project_name: "",
            project_description: "",
            start_year: "",
            end_year: "",
            is_tech: "",
            total_investment_value: "",
            biro: {
                id: "",
                rcc: "",
                code: "",
                name: ""
            },
            product: {
                id: "",
                product_name: "",
                product_code: "",
                strategy: ""
            },
            project_detail: [
                {
                    id: "",
                    dcsp_id: "",
                    project_type: "",
                    planning: {
                        id: "",
                        year: "",
                        is_active: "",
                        due_date: ""
                    },
                    budget: [
                        {
                            id: "",
                            expense_type: "",
                            planning_q1: "",
                            planning_q2: "",
                            planning_q3: "",
                            planning_q4: "",
                            realization_jan: "",
                            realization_feb: "",
                            realization_mar: "",
                            realization_apr: "",
                            realization_may: "",
                            realization_jun: "",
                            realization_jul: "",
                            realization_aug: "",
                            realization_sep: "",
                            realization_oct: "",
                            realization_nov: "",
                            realization_dec: "",
                            switching_in: "",
                            switching_out: "",
                            top_up: "",
                            returns: "",
                            allocate: "",
                            coa: ""
                        },
                    ]
                },
            ]
        },

        dataTable: {
            projectDetailsHeaders: [
                { text: "Action", value: "actions", align: "center", sortable: false},
                { text: "ID", value: "id"},
                { text: "Year", value: "planning.year"},
                { text: "Project ID", value: "dcsp_id"},
                { text: "Status", value: "planning.is_active"},
                { text: "Due Date", value: "planning.due_date"},
                { text: "Project Type", value: "project_type"},
            ],
        },
    }),

    mounted(){
        this.showItem = this.projectDetail.project_detail;
        // console.log("SHOW ITEM");
        // console.log(this.showItem);
    },
    computed: {
       status: function() {
           return this.projectDetail.project_detail ? false : true
       },
    },
    methods: {
        onOK() {
            return this.$router.go(-1);
        },
        onEdit(item) {
            this.$store.commit("listProject/GET_SUCCESS_LIST_PROJECT_BY_ID", item);
        },
    }
}
</script>

<style lang="scss" scoped>
.searchBar {
    width: 400px;
}
.data-table {
    margin: 40px;
}

#table-project-details {
    .table-project-details__header {
        padding-left: 32px;
        font-size: 3.25rem !important;
        font-weight: 600 !important;
    }
    .table-project-details__detail {
        border-radius: 8px;
        margin: 1% auto !important;
        padding-right: 3% !important;
        width: 97%;
        height: 90%;
    }
    .table-project-details__input {
        padding: 10px 32px;
    }
    .table-project-details__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
    .table-project-details__container {
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
        max-height: 90%;
    }
    .table-project-details__outer-container {
        width: 90% !important;
        margin: 1% auto !important;
        background-color: white;
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
        max-height: 90%;
    }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#table-project-details {
    .table-project-details__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .table-project-details__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>