<template>
  <v-chip :color="chipColor" small dark class="lighten-4" :class="textColor">
    {{ label }}
  </v-chip>
</template>

<script>
export default {
  name: "BinaryIsBudgetChip",
  props: ["boolean"],
  computed: {
    chipColor() {
      return this.boolean ? "cyan" : "red";
    },
    textColor() {
      return `${this.chipColor}--text`;
    },
    label() {
      return this.boolean ? "Yes" : "No";
    },
  },
};
</script>