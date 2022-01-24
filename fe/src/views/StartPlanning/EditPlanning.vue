<template>
    <v-app id="edit-planning">
        <v-container>
            <v-row no-gutters>
                <v-card class="edit-planning__detail">
                    <v-row no-gutters>
                        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                            <v-row no-gutters>
                                <v-subheader class="edit-planning__header">Edit Planning</v-subheader>
                            </v-row>
                        </v-col>
                    </v-row>

                    <v-card-text>
                        <v-form class="px-3">
                            <v-row no-gutters>
                                <!-- PLANNING FOR -->
                                <v-col cols="6"> Planning For <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-planning__field">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="2023">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>

                                <!-- STATUS -->
                                <v-col cols="6"> Status <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-planning__field">
                                            <v-select
                                            v-model="status"
                                            :items="statusOptions"
                                            item-text="activeInactive"
                                            label="Active/Inactive"
                                            outlined
                                            return-object>
                                            </v-select>
                                        </div>
                                    </v-col>
                                </v-col>
                            </v-row>

                            <v-row no-gutters>
                                <!-- DUE DATE -->
                                <v-col cols="6"> Due Date <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <v-menu
                                        v-model="menu"
                                        :close-on-content-click="false"
                                        :nudge-right="40"
                                        transition="scale-transition"
                                        offset-y
                                        min-width="auto">
                                            <template v-slot:activator="{ on, attrs }">
                                                <div class="edit-planning__field">
                                                    <v-text-field
                                                    v-model="date"
                                                    outlined
                                                    readonly
                                                    v-bind="attrs"
                                                    v-on="on">
                                                    </v-text-field>
                                                </div>
                                            </template>
                                            <v-date-picker
                                            v-model="date"
                                            @input="menu = false">
                                            </v-date-picker>
                                        </v-menu>
                                    </v-col>
                                </v-col>

                                <!-- SEND NOTIFICATION -->
                                <v-col cols="6"> Send Notification <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-planning__field">
                                            <v-select
                                            v-model="notif"
                                            :items="notifOptions"
                                            item-text="option"
                                            label="Yes/No"
                                            outlined
                                            return-object
                                            @click="notifValue(returnValue)">
                                            </v-select>
                                        </div>
                                    </v-col>
                                </v-col>
                            </v-row>

                            <!-- SEND TO -->
                            <v-row no-gutters v-if="notifValue(returnValue)=='Yes'">
                                <v-col> Send to <strong class="red--text">*</strong>
                                    <v-col no-gutters>
                                        <v-select
                                            class="StartPlanning__select"
                                            v-model="sendToEmail"
                                            :items="biroGsit"
                                            item-text="biroGsitName"
                                            item-value="biroGsitEmail"
                                            label="Select Biro"
                                            multiple
                                            chips
                                            outlined>
                                        </v-select>
                                    </v-col>
                                </v-col>
                            </v-row>

                            <!-- E-MAIL BODY -->
                            <v-row no-gutters v-if="notifValue(returnValue)=='Yes'">
                                <v-col> E-mail Body
                                    <v-col>
                                        <div class="emailBody">
                                            <v-textarea
                                            outlined
                                            dense
                                            :disabled="isView">
                                            </v-textarea>
                                        </div>
                                    </v-col>
                                </v-col>
                            </v-row>

                            <!-- BUTTONS -->
                            <v-row no-gutters>
                                <v-col cols="11" align="right">
                                    <!-- <div class="cancelBtn"> -->
                                    <v-btn
                                        rounded
                                        outlined
                                        class="primary--text"
                                        @click="onCancel"
                                        v-if="!isView"
                                        style="width: 8rem; margin-top: 96px">
                                        Cancel
                                    </v-btn>
                                    <v-btn
                                        rounded
                                        class="primary ml-3"
                                        type="save"
                                        v-if="!isView"
                                        style="width: 8rem; margin-top: 96px">
                                        Save
                                    </v-btn>
                                    <!-- </div> -->
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-card-text>
                </v-card>

                <v-card class="edit-planning__logHistory">
                    <v-row no-gutters>
                        <v-col no-gutters>
                            <v-subheader class="edit-planning__header">Log History</v-subheader>
                        </v-col>
                        <v-card-text class="edit-planning__cardText">
                            <v-timeline
                                align-top
                                dense>
                                <v-timeline-item
                                color="primary"
                                small>
                                    <v-row class="pt-1">
                                        <v-col cols="4">
                                            <v-row no-gutters>
                                                <strong>Phang Willy</strong>
                                            </v-row>

                                            <v-row no-gutters>
                                                <strong>5 Jan 2022</strong>
                                            </v-row>
                                        </v-col>
                                        <v-col>
                                            <strong>Update Planning</strong>
                                            <div class="text-caption">
                                                Due Date: 2022-11-30
                                                </div>
                                            <div class="text-caption">
                                                Send Notification: Yes
                                            </div>
                                        </v-col>
                                    </v-row>
                                </v-timeline-item>

                                <v-timeline-item
                                color="primary"
                                small>
                                    <v-row class="pt-1">
                                        <v-col cols="4">
                                            <v-row no-gutters>
                                                <strong>Jeffry Setiawan</strong>
                                            </v-row>

                                            <v-row no-gutters>
                                                <strong>5 Jan 2022</strong>
                                            </v-row>
                                        </v-col>
                                        <v-col>
                                            <strong>Update ARC</strong>
                                            <div class="text-caption">
                                                Due Date: 2022-11-25
                                            </div>
                                            <div class="text-caption">
                                                Send Notification: Yes
                                            </div>
                                        </v-col>
                                    </v-row>
                                </v-timeline-item>

                                <v-timeline-item
                                color="primary"
                                small>
                                    <v-row class="pt-1">
                                        <v-col cols="4">
                                            <v-row no-gutters>
                                                <strong>Phang Willy</strong>
                                            </v-row>

                                            <v-row no-gutters>
                                                <strong>5 Jan 2022</strong>
                                            </v-row>
                                        </v-col>
                                        <v-col>
                                            <strong>Create Planning</strong>
                                            <div class="text-caption">
                                                Planning For: 2023
                                            </div>
                                            <div class="text-caption">
                                                Status: Active
                                            </div>
                                            <div class="text-caption">
                                                Due Date: 2022-10-20
                                            </div>
                                            <div class="text-caption">
                                                Send Notification: Yes
                                            </div>
                                            <div class="text-caption">
                                                Send to: GSIT ARC A, GSIT CTS A, GSIT CTS B, ...
                                            </div>
                                            <div class="text-caption">
                                                Content: Dear All, Terkait adanya kebutuhan planning budget tahun 2023, kami mengajak Bapak/Ibu sekalian untuk mengisi perencanaan budget pada aplikasi budget (www.budgetgsitbca.co.id). Pengisian planning budget ini akan berakhir pada 31 Desember 2022. Atas perhatiannya saya ucapkan terima kasih. Best Regards, ITFAM
                                            </div>
                                        </v-col>
                                    </v-row>
                                </v-timeline-item>
                            </v-timeline>
                        </v-card-text>
                    </v-row>
                </v-card>
            </v-row>
        </v-container>
    </v-app>
</template>

<script>
export default {
    watch: {},
    data() {
        return {
            status: '',
            sendNotif: '',
            date: null,
            sendToEmail: [],
        }
    },
    data: () => ({
        date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        menu: false,

        checkbox: false,
        validation: {
            required: (v) => !!v || "This field is required",
        },
        
        statusOptions: [
            {activeInactive: 'Active'},
            {activeInactive: 'Inactive'}
        ],
        status: null,
        
        notifOptions: [
            {option: 'Yes'},
            {option: 'No'}
        ],
        notif: 'No',

        biroGsit: [
            {biroGsitName: 'GSIT ARC A', biroGsitEmail: 'gsit_arc_a_00@intra.bca'},
            {biroGsitName: 'GSIT CTS A', biroGsitEmail: 'gsit_cts_a_00@intra.bca'},
            {biroGsitName: 'GSIT CTS B', biroGsitEmail: 'gsit_cts_b_00@intra.bca'},
            {biroGsitName: 'GSIT CTS C', biroGsitEmail: 'gsit_cts_c_00@intra.bca'},
            {biroGsitName: 'GSIT CTS D', biroGsitEmail: 'gsit_cts_d_00@intra.bca'},
            {biroGsitName: 'GSIT CTS E', biroGsitEmail: 'gsit_cts_e_00@intra.bca'},
            {biroGsitName: 'GSIT DIS A', biroGsitEmail: 'gsit_dis_a_00@intra.bca'},
            {biroGsitName: 'GSIT DIS B', biroGsitEmail: 'gsit_dis_b_00@intra.bca'},
            {biroGsitName: 'GSIT DTM A', biroGsitEmail: 'gsit_dtm_a_00@intra.bca'},
            {biroGsitName: 'GSIT DTM B', biroGsitEmail: 'gsit_dtm_b_00@intra.bca'},
            {biroGsitName: 'GSIT DTM C', biroGsitEmail: 'gsit_dtm_c_00@intra.bca'},
            {biroGsitName: 'GSIT IBO A', biroGsitEmail: 'gsit_ibo_a_00@intra.bca'},
            {biroGsitName: 'GSIT IBO B', biroGsitEmail: 'gsit_ibo_b_00@intra.bca'},
            {biroGsitName: 'GSIT IBO C', biroGsitEmail: 'gsit_ibo_c_00@intra.bca'},
            {biroGsitName: 'GSIT IBO D', biroGsitEmail: 'gsit_ibo_d_00@intra.bca'},
            {biroGsitName: 'GSIT IBO E', biroGsitEmail: 'gsit_ibo_e_00@intra.bca'},
            {biroGsitName: 'GSIT IBO F', biroGsitEmail: 'gsit_ibo_f_00@intra.bca'},
            {biroGsitName: 'GSIT IBO G', biroGsitEmail: 'gsit_ibo_g_00@intra.bca'},
            {biroGsitName: 'GSIT IMO A', biroGsitEmail: 'gsit_imo_a_00@intra.bca'},
            {biroGsitName: 'GSIT IMO B', biroGsitEmail: 'gsit_imo_b_00@intra.bca'},
            {biroGsitName: 'GSIT IMO C', biroGsitEmail: 'gsit_imo_c_00@intra.bca'},
            {biroGsitName: 'GSIT IMO D', biroGsitEmail: 'gsit_imo_d_00@intra.bca'},
            {biroGsitName: 'GSIT ISO A', biroGsitEmail: 'gsit_iso_a_00@intra.bca'},
            {biroGsitName: 'GSIT ISO B', biroGsitEmail: 'gsit_iso_b_00@intra.bca'},
            {biroGsitName: 'GSIT ISO C', biroGsitEmail: 'gsit_iso_c_00@intra.bca'},
            {biroGsitName: 'GSIT ITX A', biroGsitEmail: 'gsit_itx_a_00@intra.bca'},
            {biroGsitName: 'GSIT ITX B', biroGsitEmail: 'gsit_itx_b_00@intra.bca'},
            {biroGsitName: 'GSIT ITX C', biroGsitEmail: 'gsit_itx_c_00@intra.bca'},
            {biroGsitName: 'GSIT ITX D', biroGsitEmail: 'gsit_itx_d_00@intra.bca'},
            {biroGsitName: 'GSIT ITX E', biroGsitEmail: 'gsit_itx_e_00@intra.bca'},
            {biroGsitName: 'GSIT ITX F', biroGsitEmail: 'gsit_itx_f_00@intra.bca'},
            {biroGsitName: 'GSIT ITX G', biroGsitEmail: 'gsit_itx_g_00@intra.bca'},
            {biroGsitName: 'GSIT NIS A', biroGsitEmail: 'gsit_nis_a_00@intra.bca'},
            {biroGsitName: 'GSIT NIS B', biroGsitEmail: 'gsit_nis_b_00@intra.bca'},
            {biroGsitName: 'GSIT NIS C', biroGsitEmail: 'gsit_nis_c_00@intra.bca'},
            {biroGsitName: 'GSIT NIS D', biroGsitEmail: 'gsit_nis_d_00@intra.bca'},
            {biroGsitName: 'GSIT NIS E', biroGsitEmail: 'gsit_nis_e_00@intra.bca'},
            {biroGsitName: 'GSIT SAQ A', biroGsitEmail: 'gsit_saq_a_00@intra.bca'},
            {biroGsitName: 'GSIT SAQ B', biroGsitEmail: 'gsit_saq_b_00@intra.bca'},
            {biroGsitName: 'GSIT SAQ C', biroGsitEmail: 'gsit_saq_c_00@intra.bca'},
            {biroGsitName: 'GSIT SIS A', biroGsitEmail: 'gsit_sis_a_00@intra.bca'},
            {biroGsitName: 'GSIT SIS B', biroGsitEmail: 'gsit_sis_b_00@intra.bca'},
            {biroGsitName: 'GSIT SIS C', biroGsitEmail: 'gsit_sis_c_00@intra.bca'},
            {biroGsitName: 'GSIT SIS D', biroGsitEmail: 'gsit_sis_d_00@intra.bca'}
        ],
            
        closeOnContentClick: true,
    }),

    methods: {
        onAdd() {
            this.dialog = !this.dialog;
        },
        onCancel() {
            return this.$router.go(-1);
        },
        onSave() {
            console.log(this.status, this.date, this.sendNotif);
        },
        notifValue(returnValue) {
            return this.notif.option;
        },
    }
};
</script>

<style scoped>
.sendTo {
    min-width: 90%;
}
.emailBody {
    min-width: 90%;
}

.cancelBtn {
    width: 200px;
}
.saveBtn {
    width: 200px;
}
.saveBtn--text /deep/ label {
    color: white;
}
</style>

<style lang="scss" scoped>
.searchBar {
    width: 400px;
}
.data-table {
    margin: 40px;
}

#edit-planning {
    .edit-planning__header {
        padding-top: 32px;
        padding-bottom: 32px;
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
        min-width: 80%;
    }
    .edit-planning__detail {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 50%;
    }
    .edit-planning__input {
        padding: 10px 32px;
    }
    .edit-planning__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
    .edit-planning__container {
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
    }
    .edit-planning__cardText {
        flex-grow: 4;
        max-height: 470px;
        overflow-y: scroll;
    }
    .edit-planning__logHistory {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 40%;
    }
    .edit-planning__field {
        min-width: 150px;
    }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#edit-planning {
    .edit-planning__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .edit-planning__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>