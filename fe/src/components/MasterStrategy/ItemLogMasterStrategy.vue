<template>
    <v-container class="mt-5">
        <v-row>Strategy Name: {{data.serialized_data.name}}</v-row>
    </v-container>
</template>
<script>
export default {
  name: "ItemLogMasterStrategy",
  props: ["data"],
}

</script>