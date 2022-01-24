<template>
    <v-app id="edit-planning">
        <v-container>
            <v-row no-gutters>
                <v-card class="edit-planning__detail">
                    <v-row no-gutters>
                        <v-col cols="12" xs="12" sm="12" md="12" lg="12" no-gutters>
                            <v-row no-gutters>
                                <v-subheader class="edit-planning__header">Edit Status Monitoring</v-subheader>
                            </v-row>
                        </v-col>
                    </v-row>

                    <v-card-text>
                        <v-form class="px-3">
                            <v-row no-gutters>
                                <!-- GROUP -->
                                <v-col cols="6"> Group <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-status-monitoring__field">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="GAQ">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>

                                <!-- SUBGROUP -->
                                <v-col cols="6"> Sub-Group <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-status-monitoring__field">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="ARC">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>
                            </v-row>

                            <v-row no-gutters>
                                <!-- BIRO -->
                                <v-col cols="6"> Biro <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-status-monitoring__field">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="ARC A">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>

                                <!-- PIC -->
                                <v-col cols="6"> PIC <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-status-monitoring__field">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="Jumas Ranope">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>
                            </v-row>

                            <v-row no-gutters>
                                <!-- UPDATE DATE -->
                                <v-col cols="6"> Update Date <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-status-monitoring__field">
                                            <v-text-field
                                            outlined
                                            dense
                                            disabled
                                            label="2022-11-30">
                                            </v-text-field>
                                        </div>
                                    </v-col>
                                </v-col>

                                <!-- STATUS -->
                                <v-col cols="6"> Status <strong class="red--text">*</strong>
                                    <v-col cols="6">
                                        <div class="edit-status-monitoring__field">
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

                            <!-- BUTTONS -->
                            <v-row no-gutters>
                                <v-col cols="11" align="right">
                                    <v-btn
                                        rounded
                                        outlined
                                        class="primary--text"
                                        @click="onCancel"
                                        v-if="!isView"
                                        style="width: 8rem; margin-top: 64px; margin-bottom: 32px">
                                        Cancel
                                    </v-btn>
                                    <v-btn
                                        rounded
                                        class="primary ml-3"
                                        type="save"
                                        v-if="!isView"
                                        style="width: 8rem; margin-top: 64px; margin-bottom: 32px">
                                        Save
                                    </v-btn>
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
                                            <strong>Update ARC</strong>
                                            <div class="text-caption">
                                                Status: Submitted
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
                                                <strong>2 Jan 2022</strong>
                                            </v-row>
                                        </v-col>
                                        <v-col>
                                            <strong>Update ARC</strong>
                                            <div class="text-caption">
                                                Status: Draft
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
            group: '',
            subgroup: '',
            biro: '',
            pic: '',
            updateDate: '',
        }
    },
    data: () => ({
        menu: false,

        statusOptions: [
            {activeInactive: 'Active'},
            {activeInactive: 'Inactive'}
        ],
        status: null,
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