<template>
    <v-container class="mt-5">
        <v-row>Project Type: {{getProjectType}}</v-row>
    </v-container>
</template>

<script>
export default {
  name: "ItemLogMyProjectDetail",
  props: ["data"],
  computed:{
    getProjectType() {
        if(this.data.serialized_data.project_type == 1) {
            return "Carry Forward"
        } else if(this.data.serialized_data.project_type == 2) {
            return "New"
        } else if(this.data.serialized_data.project_type == 3) {
            return "Regular"
        }
    }
  }
}

</script>