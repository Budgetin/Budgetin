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
      <v-timeline dense>
        <v-timeline-item
          v-for="item in items"
          :key="item.id"
          :color="getActionColor(item.action)"
          small
          fill-dot
          class="mr-3"
        >
          <!-- <v-container>
            <v-row justify="space-between">
              <div>
                <strong>
                  {{ getActionString(item.action) }} {{ topic }}
                </strong>
              </div>
              <div class="mr-3">
                {{ formatDateTime(item.action_time) }}
              </div>
            </v-row>

            <template v-if="item.hasOwnProperty('changes')">
              <v-row v-for="k in Object.keys(item.changes)" :key="k">
                {{ k }}: {{ item.changes[k] }}
              </v-row>
            </template>
            <template v-else>
              <template v-if="item.action.toLowerCase() === 'create'">
                <v-row>MPP For: {Tahun}</v-row>
                <v-row>Type: {Type}</v-row>
                <v-row>Biro: {{ item.data.header }}</v-row>
                <v-row>Status: {Status}</v-row>
              </template>
              <template v-else>
                <v-row>Aspect: {{ item.data.aspect }}</v-row>
                <v-row>period: {{ item.data.periode }}</v-row>
                <v-row>Category: {{ item.data.category }}</v-row>
                <v-row>Value Request: {{ item.data.value_request }}</v-row>
                <v-row>Value Adjust: {{ item.data.value_adjsust }}</v-row>
                <v-row>Requirement: {{ item.data.requirement }}</v-row>
                <v-row>Job Description: {{ item.data.job_description }}</v-row>
                <v-row>Note: {{ item.data.note }}</v-row>
              </template>
            </template>
            <v-row
              ><strong>{{ item.user }}</strong></v-row
            >
          </v-container> -->
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
    <!-- <pre v-for="item in items" :key="item">{{ item.changes }}</pre> -->
  </v-card>
</template>

<script>
// import formatting from "@/mixins/formatting";
export default {
  name: "TimelineLog",
  // props: ["items", "topic"],
  props: {
    items: {
      type: Array,
      default: () => [],
    },
    topic: {
      type: String,
      default: () => "Source",
    },
    isGoBack: {
      type: Boolean,
      default: false,
    },
  },
  // mixins: [formatting],
  computed: {},
  methods: {
    getActionString(action) {
      switch (action) {
        case 0:
          return "Create";
        case 1:
          return "Update";
        case 2:
          return "Delete";
        case "Create":
          return "Generate Access Input";
        case "Update":
          return "Update Detail Request";
        case "Insert":
          return "Insert Detail Request";
        default:
          return "Unknown";
      }
    },
    getActionColor(action) {
      switch (action) {
        case 0:
          return "#29B1C1";
        case 1:
          return "#16B1FF";
        case 2:
          return "red";
        case "Create":
          return "#29B1C1";
        case "Update":
          return "#16B1FF";
        case "Insert":
          return "Red";
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