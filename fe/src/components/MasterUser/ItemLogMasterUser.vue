<template>
    <v-container class="mt-5">
        <v-row>Username: {{data.serialized_data.name}}</v-row>
    </v-container>
</template>
<script>
export default {
  name: "ItemLogMasterUser",
  props: ["data"],
}

</script>