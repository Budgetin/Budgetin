<template>
  <v-container class="mt-5">
    <!-- {{getName}} -->
    <v-row>COA Name: {{ data.serialized_data.name }}</v-row>
    <v-row>Definition: {{ data.serialized_data.definition }}</v-row>
    <v-row>Hyperion Text: {{ data.serialized_data.hyperion_name }}</v-row>
    <v-row>Capex: {{ getCapex }}</v-row>
    <v-row v-if="data.serialized_data.is_capex == 1"
      >Minimum tobe CAPEX: {{numberWithDots(this.data.serialized_data.minimum_item_origin) }}</v-row
    >
  </v-container>
</template>
<script>
import formatting from "@/mixins/formatting";
export default {
  name: "ItemLogMasterCoa",
  props: ["data"],
  mixins: [formatting],
  computed: {
    getCapex() {
      return this.data.serialized_data.is_capex == 1 ? "Yes" : "No";
    },

  },
};
</script>
