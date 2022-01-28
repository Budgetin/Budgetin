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
            <template v-if="item.table == 'coa'">
              <item-log-master-coa
                :data="item"
              >
              </item-log-master-coa>
            </template>
            <template v-if="item.table == 'product'">
              <item-log-master-product
                :data="item"
              >
              </item-log-master-product>
            </template>
            <template v-if="item.table == 'strategy'">
              <item-log-master-strategy
                :data="item"
              >
              </item-log-master-strategy>
            </template>
            <template v-if="item.table == 'user'">
              <item-log-master-user
                :data="item"
              >
              </item-log-master-user>
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
import ItemLogMasterCoa from "@/components/MasterCOA/ItemLogMasterCoa"
import ItemLogMasterProduct from "@/components/MasterProduct/ItemLogMasterProduct"
import ItemLogMasterStrategy from "@/components/MasterStrategy/ItemLogMasterStrategy"
import ItemLogMasterUser from "@/components/MasterUser/ItemLogMasterUser"

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
  components: { ItemLogMasterCoa,ItemLogMasterProduct,ItemLogMasterStrategy,ItemLogMasterUser },
  created() {
    // console.log(items)
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
