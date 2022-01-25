<template>
    <v-card class="log-history__card">
        <v-row no-gutters>
            <v-col no-gutters>
                <v-card-title class="log-history__header text-h5">Log History</v-card-title>
            </v-col>
            <v-card-text class="log-history__cardText">
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
</template>

<style lang="scss" scoped>
#log-history {
    .log-hitory__card {
        border-radius: 8px;
        margin: 1% auto !important;
        width: 40%;
    }
    .log-history__cardText {
        flex-grow: 4;
        max-height: 470px;
        overflow-y: scroll;
    }
    .log-history__header {
        padding-top: 32px;
        padding-bottom: 32px;
        padding-left: 32px;
        font-size: 1.25rem;
        font-weight: 600;
        min-width: 80%;
    }
}