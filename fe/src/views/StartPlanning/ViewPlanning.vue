<template>
    <v-app id="view-planning">
        <v-container>
            <v-row no-gutters>
                <v-card class="view-planning__detail">
                    <v-row no-gutters>
                        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                            <v-row no-gutters>
                                <v-subheader class="view-planning__header">View Planning</v-subheader>
                                <v-col no-gutters class="view-planning__btn">
                                    <v-btn
                                        icon
                                        color="primary"
                                        class="mt-3">
                                        <v-icon>mdi-pencil-outline</v-icon>
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-col>
                    </v-row>

                    <v-card-text>
                        <v-form class="px-3">
                            <v-row no-gutters>
                                <!-- PLANNING FOR -->
                                <v-col cols="6"> Planning For <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="planningFor">
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
                                        <div class="status">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="Active">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>
                            </v-row>

                            <v-row no-gutters>
                                <!-- DUE DATE -->
                                <v-col cols="6"> Due Date <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="dueDate">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="2022-11-30">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>

                                <!-- SEND NOTIFICATION -->
                                <v-col cols="6"> Send Notification <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="status">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="Yes">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>
                            </v-row>
                        </v-form>

                        <v-col no-gutters class="view-planning__btn">
                            <v-btn rounded color="primary" @click="onBack" style="width: 8rem; margin-top: 96px">
                                OK
                            </v-btn>
                        </v-col>
                    </v-card-text>
                </v-card>

                <v-card class="view-planning__logHistory">
                    <v-row no-gutters>
                        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                            <v-subheader class="view-planning__header">Log History</v-subheader>
                        </v-col>
                        <v-card-text class="view-planning__cardText">
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
            
        };
    },

    methods: {
        onAdd() {
            this.dialog = !this.dialog;
        },
        onCancel() {
            this.dialog = false;
        },
    }
};
</script>

<style scoped>
.planningFor {
    min-width: 150px;
}
.status {
    min-width: 150px;
}
.dueDate {
    min-width: 150px;
}
.sendNotif {
    min-width: 150px;
}
.sendTo {
    width: 500px;
}
.emailBody {
    width: 500px;
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

#view-planning {
    .view-planning__header {
        padding-top: 32px;
        padding-bottom: 32px;
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
        min-width: 80%;
    }
    .view-planning__detail {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 50%;
    }
    .view-planning__input {
        padding: 10px 32px;
    }
    .view-planning__btn {
        text-align: end;
        button {
            margin: 10px 32px;
        }
    }
    .view-planning__container {
        padding: 24px 0px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        border-radius: 8px;
    }
    .view-planning__cardText {
        flex-grow: 4;
        max-height: 470px;
        overflow-y: scroll;
    }
    .view-planning__logHistory {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 40%;
    }
}

@media only screen and (max-width: 600px) {
/* For mobile phones */
#view-planning {
    .view-planning__btn {
        text-align: center;
        padding: 0px 32px;

        button {
        width: 100%;
        margin: 0px 0px 32px 0px;
        }
    }
    .view-planning__card {
        flex-direction: column;
        button {
        width: 16rem !important;
        margin-left: unset !important;
        }
    }
  }
}
</style>