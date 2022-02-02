<template>
    <v-app id="view-list-project">
        <v-container>
            <v-row no-gutters>
                <!-- VIEW LIST PROJECT -->
                <form-list-project
                :form="form"
                :isView="isView"
                :dataListProject="dataListProject"
                @okClicked="onOK"
                class="view-list-project__detail">
                </form-list-project>
            </v-row>
        </v-container>

        <v-container class="view-list-project__outer-container">
            <!-- <v-card>
                <v-card-text> -->
            <v-row no-gutters style="margin-top: 16px">
                <v-subheader class="view-list-project__header">Project Details</v-subheader>
            </v-row>

            <v-row no-gutters>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                    <v-data-table
                    :headers="dataTable.headers"
                    :loading="loadingGetListPlanning"
                    :items="dataListPlanning"
                    class="data-table">
                    </v-data-table>
                </v-col>
            </v-row>
                <!-- </v-card-text>
            </v-card> -->
        </v-container>
    </v-app>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import FormListProject from '@/components/CompListProject/FormListProject';
export default {
    name: "ViewListProject",
    components: {
        FormListProject
    },
    data: () => ({
        isView: true,
        form: {
            id: "",
            project_name: "",
            project_description: "",
            product: {
                product_code: "",
                product_name: "",
            },
            itfam_id: "",
            biro: {
                rcc: "",
                code: "",
            },
            is_tech: "",
            start_year: "",
            end_year: "",
            total_investment_value: "",
            planning: {
                year: "",
                is_active: "",
                due_date: ""
            },
            dcsp_id: "",
            project_type: "",
        },

        dataTable: {
            headers: [
                { text: "Year", value: "planning.year", width: "10%" },
                { text: "Project ID", value: "dcsp_id", width: "15%", align: "start" },
                { text: "Status", value: "planning.is_active", width: "20%" },
                { text: "Due Date", value: "planning.due_date", width: "20%" },
                { text: "Project Type", value: "project_type", width: "25%" }
            ],
        },
    }),

    created() {
        this.getEdittedItem();
        this.setBreadcrumbs();
        this.getListPlanningById(this.$route.params.id);
    },

    computed: {
        ...mapState("listProject", ["loadingGetListProject", "dataListProject"]),
    },

    methods: {
        ...mapActions("listProject", ["getListProjectById"]),

        setBreadcrumbs() {
            let param = this.isView ? "View Detail Project" : "Edit Project";
            this.$store.commit("breadcrumbs/SET_LINKS", [
                {
                    text: "List of Projects",
                    link: true,
                    exact: true,
                    disabled: false,
                    to: {
                        name: "ListProject",
                    },
                },
                {
                    text: param,
                    disabled: true,
                },
            ]);
        },

        getEdittedItem() {
            console.log("Masuk Editted Item");
            this.getListProjectById(this.$route.params.id).then(() => {
                console.log("ParamID: "+this.$route.params.id);
                this.setForm();
            });
        },
        setForm() {
            // console.log("Masuk Set Form");
            this.form = JSON.parse(
                JSON.stringify(this.$store.state.listProject.edittedItem)
            );
            // console.log(this.form);
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

#view-list-project {
    .view-list-project__header {
        // padding-top: 32px;
        // padding-bottom: 32px;
        // padding-left: 32px;
        // font-size: 1.25rem;
        // font-weight: 600;
        // min-width: 80%;
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
    }
    .view-list-project__detail {
        border-radius: 8px;
        margin: 1% auto !important;
        padding-right: 3% !important;
        width: 92%;
        height: 90%;
    }
    .view-list-project__input {
        padding: 10px 32px;
    }
    .view-list-project__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
    .view-list-project__container {
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
        max-height: 90%;
    }
    .view-list-project__outer-container {
        width: 90% !important;
        margin: 1% auto !important;
        background-color: white;
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
        max-height: 90%;
    }
    // .view-list-project__form{
    //     width: 100%;
    //     margin-left: 2% !important;
    // }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#view-list-project {
    .view-list-project__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .view-list-project__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>
