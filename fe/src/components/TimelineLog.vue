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
          v-for="item in items"
          :key="item.id"
          :color="getActionColor(item.action_id)"
          small
          fill-dot
          class="mr-3"
        >
          <v-container>
            <v-row justify="space-between">
              <div>
                <strong>
                  {{item.action_id}}
                </strong>
              </div>
              <div class="mr-3">
                {{ item.timestamp }}
              </div>
            </v-row>
          </v-container>
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
  created() {
    // console.log(items)
  },
  methods: {
    getActionColor(action) {
      console.log(action);
      switch (action) {
        case 1:
          return "blue";
        case 2:
          return "yellow";
        case 3:
          return "#40a9ff";
        case "create":
          return "#blue";
        case "read":
          return "#yellow";
        case "update":
          return "#40a9ff";
        default:
          return "grey";
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.separate-scrollable-y {
  overflow-y: auto !important;
  max-height: 75vh !important;
}
</style>
