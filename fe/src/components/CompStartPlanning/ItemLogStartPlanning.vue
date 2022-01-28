<template>
    <v-container class="mt-5">
        <v-row>Planning For: {{data.serialized_data.username}} - {{data.serialized_data.display_name}}</v-row>
        <v-row>Status: {{getActive}}</v-row>
        <v-row>Due Date: {{data.serialized_data.role}}</v-row>
        <v-row>Send Notification: {{data.serialized_data.role}}</v-row>
        <v-row>Send to: {{data.serialized_data.role}}</v-row>
        <v-row>E-mail Body: {{data.serialized_data.role}}</v-row>

    </v-container>
</template>
<script>
export default {
  name: "ItemLogStartPlanning",
  props: ["data"],
  computed:{
    getActive(){
      return this.data.serialized_data.is_active == 1 ? "Active" : "Inactive";
    }
  }
}

</script>