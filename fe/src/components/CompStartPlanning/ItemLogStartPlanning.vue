<template>
    <v-container class="mt-5">
        <v-row>Planning For: {{data.serialized_data.year}}</v-row>
        <v-row>Status: {{getActive}}</v-row>
        <v-row>Due Date: {{data.serialized_data.due_date}}</v-row>
        <v-row>Send Notification: {{getNotif}}</v-row>
        <v-row v-if="data.serialized_data.notification == 1">Send to: {{data.serialized_data.biros}}</v-row>
        <v-row v-if="data.serialized_data.notification == 1">E-mail Body: {{data.serialized_data.email_body}}</v-row>
    </v-container>
</template>

<script>
export default {
  name: "ItemLogStartPlanning",
  props: ["data"],
  computed:{
    getActive(){
      return this.data.serialized_data.is_active == 1 ? "Active" : "Inactive";
    },
    getNotif(){
      return this.data.serialized_data.notification == 1 ? "Yes" : "No";
    }
  }
}

</script>