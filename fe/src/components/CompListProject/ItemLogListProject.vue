<template>
    <v-container class="mt-5">
        <v-row>Project Name: {{data.serialized_data.project_name}}</v-row>
        <v-row>Project Description: {{data.serialized_data.project_description}}</v-row>
        <v-row>Product Name: {{data.serialized_data.product}}</v-row>
        <v-row>Biro: {{data.serialized_data.biro}}</v-row>
        <v-row>Tech/Non-Tech: {{getTech}}</v-row>
        <v-row>Start Year: {{data.serialized_data.start_year}}</v-row>
        <v-row>End Year: {{data.serialized_data.end_year}}</v-row>
        <v-row>Total Investment: {{numberWithDots(this.data.serialized_data.total_investment_value) }}</v-row>
    </v-container>
</template>

<script>
import formatting from "@/mixins/formatting";
export default {
  name: "ItemLogListProject",
  props: ["data"],
  mixins: [formatting],
  computed:{
    getTech() {
        return this.data.serialized_data.is_tech == true ? "Tech" : "Non-Tech";
    },
  }
}

</script>