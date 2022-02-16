<template>
  <v-chip :color="chipColor" small dark class="lighten-4" :class="textColor">
    {{ label }}
  </v-chip>
</template>

<script>
export default {
  name: "BinaryYesNoChip",
  props: ["boolean"],
  computed: {
    chipColor() {
      return this.boolean ? "rgba(97, 164, 232, 0.2)" : "red";
    },
    textColor() {
      return this.boolean ? "blue--text" : "red";
      // return `${this.chipColor}--text`;
    },
    label() {
      return this.boolean ? "Yes" : "No";
    },
  },
};
</script>