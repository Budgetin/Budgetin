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
          :color="getColor(item.action)"
          small
          fill-dot
          class="mr-3"
        >
          <v-container>
            <v-row justify="space-between">
              <div>
                <strong>
                  {{item.action}}
                </strong>
              </div>
              <div class="mr-3">
                {{ item.timestamp }}
              </div>
            </v-row>
            <template v-if="item.table == 'budgetPlanning'">
              <item-log-budget-planning
                :data="item"
              />
            </template>
            <template v-if="item.table == 'budgetRealization'">
              <item-log-budget-realization
                :data="item"
              />
            </template>
            <template v-if="item.table == 'project_detail'">
              <item-log-my-project-detail
                :data="item"
              />
            </template>
            <template v-if="item.table == 'myproject'">
              <item-log-my-project
                :data="item"
              />
            </template>
            <v-row class="mt-1">
              <div>
                <strong>
                  {{item.serialized_data.updated_by}}
                </strong>
              </div>
            </v-row>
          </v-container>
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script>
import ItemLogMyProjectDetail from "@/components/MyProject/ItemLogMyProjectDetail"
import ItemLogBudgetPlanning from "@/components/MyProject/ItemLogBudgetPlanning"
import ItemLogBudgetRealization from '@/components/MyProject/ItemLogBudgetRealization'
import ItemLogMyProject from '@/components/MyProject/ItemLogMyProject'

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
  components: { ItemLogBudgetPlanning,ItemLogBudgetRealization,ItemLogMyProjectDetail,ItemLogMyProject },
  created() {
    
  },
  methods: {
    getColor(action) {
      switch (action) {
        case 1:
          return "#18ffb4de";
        case 2:
          return "yellow";
        case 3:
          return "#40a9ff";
        case "Create":
          return "#18ffb4de";
        case "Read":
          return "yellow";
        case "Update":
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
