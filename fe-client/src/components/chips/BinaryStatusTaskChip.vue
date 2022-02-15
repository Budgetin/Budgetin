<template>
  <v-chip :color="chipColor" small dark :class="textColor" class="font-weight-bold">
    {{ data }}
  </v-chip>
</template>

<script>
export default {
  name: "BinaryStatusTaskChip",
  props: ["data"],
  computed: {
    chipColor() {
      if (this.data=="To Do") {
        return "rgba(245, 149, 12, 0.2)";
      }
      if (this.data=="Draft") {
        return "rgba(97, 164, 232, 0.2)";
      }
      if (this.data=="Submitted") {
        return "rgba(145, 85, 253, 0.2)";
      }
    },
    textColor() {
      if (this.data=="To Do") {
        return "orange--text";
      }
      if (this.data=="Draft") {
        return "blue--text";
      }
      if (this.data=="Submitted") {
        return "purple--text";
      }
    },
  },
};
</script>