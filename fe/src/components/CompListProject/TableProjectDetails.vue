<template>
    <v-container>
        <v-row no-gutters style="margin-top: 16px">
            <v-subheader>Project Details</v-subheader>
        </v-row>

        <v-row no-gutters>
            <v-col >
                <v-data-table
                :headers="dataTable.projectDetailsHeaders"
                :loading="loadingGetListProject"
                :items="data">
                </v-data-table>
                <!-- :items="projectDetail" -->
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
export default {
    name: "TableProjectDetails",
    props: ["data"],
    data: () => ({
        isView: true,
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

        projectDetail: [],

        dataTable: {
            projectDetailsHeaders: [
                { text: "Year", value: "data.planning.year", width: "10%" },
                { text: "Project ID", value: "project_detail.dcsp_id", width: "15%" },
                { text: "Status", value: "project_detail.planning.is_active", width: "20%" },
                { text: "Due Date", value: "project_detail.planning.due_date", width: "20%" },
                { text: "Project Type", value: "project_detail.project_type", width: "25%" }
            ],
            // projectDetailsHeaders: [
            //     { text: "Year", value: "year", width: "10%" },
            //     { text: "Project ID", value: "dcsp_id", width: "15%" },
            //     { text: "Status", value: "is_active", width: "20%" },
            //     { text: "Due Date", value: "due_date", width: "20%" },
            //     { text: "Project Type", value: "name", width: "25%" }
            // ],
            // desserts: [
            //     {
            //         year: "2023",
            //         dcsp_id: "00001",
            //         is_active: "true",
            //         due_date: "2022-08-12",
            //         name: "New"
            //     }
            // ]
        },
    }),

    created() {
        this.getEdittedItem();
        this.getListProjectById(this.$route.params.id);
        // console.log("TABLE PROJECT DETAILS MASUK CREATED PARAM ID");
        // console.log(this.$route.params.id);
        console.log(this.data);
    },

    computed: {
        ...mapState("listProject", ["loadingGetListProject", "dataListPlanning"]),
    },

    methods: {
        ...mapActions("listProject", ["getListProjectById"]),

        getEdittedItem() {
            console.log("TABLE PROJECT DETAILS MASUK EDITTED ITEM1");
            this.getListProjectById(this.$route.params.id).then(() => {
                console.log("TABLE PROJECT DETAILS MASUK EDITTED ITEM2");
                console.log(this.$route.params.id);
                
                this.projectDetail = JSON.parse(
                    JSON.stringify(this.$store.state.listProject.edittedItem)
                );
                console.log(this.projectDetail);
            });
        },
        onOK() {
            return this.$router.go(-1);
        }
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
        font-size: 1.25rem;
        font-weight: 600;
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