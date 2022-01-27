<template>
    <v-container class="mt-5">
        <v-row>Product Code: {{data.serialized_data.product_code}}</v-row>
        <v-row>Product Name: {{data.serialized_data.product_name}}</v-row>
        <v-row>Strategy: {{data.serialized_data.strategy.name}}</v-row>
    </v-container>
</template>
<script>
export default {
  name: "ItemLogMasterProduct",
  props: ["data"],
}

</script>