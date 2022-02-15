<template>
  <v-chip :color="chipColor" small dark class="lighten-4" :class="textColor">
    {{ label }}
  </v-chip>
</template>

<script>
export default {
  name: "BinaryStatusChip",
  props: ["boolean"],
  computed: {
    chipColor() {
      return this.boolean ? "green" : "red";
    },
    textColor() {
      return `${this.chipColor}--text`;
    },
    label() {
      return this.boolean ? "Active" : "Inactive";
    },
  },
};
</script>