<template>
    <v-container class="mt-5">
        <!-- {{getName}} -->
        <v-row>Product Code: {{data.serialized_data.product_code}}</v-row>
        <v-row>Product Name: {{data.serialized_data.product_name}}</v-row>
        <v-row>Strategy: {{data.serialized_data.strategy.name}}</v-row>
    </v-container>
</template>
<script>
export default {
  name: "ItemLogMasterCoa",
  props: ["data"],
  computed: {
      getCapex(){
          return this.data.serialized_data.is_capex==1 ? "Yes" : "No";
      },
      getMinimum(){
          return this.data.serialized_data.minimum_item_origin.toString().split( /(?=(?:\d{3})+(?:\.|$))/g ).join( "," );
      }
  }
}

</script>