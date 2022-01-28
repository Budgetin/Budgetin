<template>
    <v-container class="mt-5">
        <v-row>Username: {{data.serialized_data.username}} - {{data.serialized_data.display_name}}</v-row>
        <v-row>Role: {{data.serialized_data.role}}</v-row>
        <v-row>Status: {{getActive}}</v-row>

    </v-container>
</template>
<script>
export default {
  name: "ItemLogMasterUser",
  props: ["data"],
  computed:{
    getActive(){
      return this.data.serialized_data.is_active == 1 ? "Active" : "Inactive";
    }
  }
}

</script>