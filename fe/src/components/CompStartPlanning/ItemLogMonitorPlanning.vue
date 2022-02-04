<template>
    <v-container class="mt-5">
        <!-- <v-row>Group: {{data.serialized_data.biro.group_code}}</v-row>
        <v-row>Sub-Group: {{data.serialized_data.biro.sub_group_code}}</v-row>
        <v-row>Biro: {{data.serialized_data.biro.code}}</v-row>
        <v-row>PIC: {{data.serialized_data.pic_initial}}</v-row> -->
        <v-row>Status: {{data.serialized_data.monitoring_status}}</v-row>
    </v-container>
</template>

<script>
export default {
  name: "ItemLogMonitorPlanning",
  props: ["data"],
}

</script>