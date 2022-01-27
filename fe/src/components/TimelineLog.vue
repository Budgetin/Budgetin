<template>
  <v-card>
    <v-card-title v-if="!isGoBack">Log History </v-card-title>
    <v-card-title v-else>
      <v-btn icon small color="primary" @click="$emit('onGoBack')">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      Log History
    </v-card-title>
    <v-card-text class="separate-scrollable-y">
    <v-timeline align-top dense>
      <v-timeline-item
          v-for="item in items "
          :key="item.id"
          small
          fill-dot
          class="mr-3"
        >
        {{item.name}}
      </v-timeline-item>
    </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script>
// import formatting from "@/mixins/formatting";
export default {
  name: "TimelineLog",
  props: {
    items: {
      type: Array,
      default: () => [],
    },
    isGoBack: {
      type: Boolean,
      default: false,
    },
  },
  created(){
    // console.log(items)
  }
}
</script>

<style lang="scss" scoped>
.separate-scrollable-y {
  overflow-y: auto !important;
  max-height: 75vh !important;
}
</style>