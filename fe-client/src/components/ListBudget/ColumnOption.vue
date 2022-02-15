<template>
  <v-card>
    <v-card-title class="mb-5">
      Choose Column
      <v-spacer></v-spacer>
      <v-btn icon small @click="onClose">
        <v-icon color="primary"> mdi-close </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-list>
        <v-list-item ripple @mousedown.prevent @click="toggle" class="indigo--text text--accent-4">
          <v-list-item-content>
            <v-list-item-title> Select All </v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-icon :color="selected.length > 0 ? 'indigo darken-4' : ''">
              {{ icon }}
            </v-icon>
          </v-list-item-action>
        </v-list-item>
        <v-list-item-group v-model="selected" multiple>
          <v-list-item
            v-for="(item, i) in data"
            :key="i"
            :value="item"
            active-class="indigo--text text--accent-4"
          >
            <template v-slot:default="{ active }">
              <v-list-item-content>
                <v-list-item-title v-text="item.text"></v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                <v-checkbox
                  :input-value="active"
                  color="indigo darken-4"
                ></v-checkbox>
              </v-list-item-action>
            </template>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "FormStrategy",
  props: ["data", "selectedColumn"],
  data: () => ({
    selected: [],
  }),
  mounted() {
    this.selected = this.selectedColumn;
  },
  computed: {
    icon() {
      if (this.selected.length === this.data.length ) return "mdi-close-box";
      if (this.selected.length != this.data.length ) return "mdi-minus-box";
      return "mdi-checkbox-blank-outline";
    },
  },
  methods: {
    onClose() {
      this.$emit("closeClicked", this.selected);
    },
    toggle() {
      this.$nextTick(() => {
        if (this.selected.length === this.data.length) {
          this.selected = [];
        } else {
          this.selected = this.data.slice();
        }
      });
    },
  },
};
</script>

<style lang="scss" scopped>
.v-card__text {
  color: unset !important;
}

button {
  min-width: 8rem;
}

.v-btn--rounded {
  min-width: 8rem !important;
}
</style>

<style scoped>
v-card-title {
  position: sticky !important;
  position: -webkit-sticky !important;
  top: 4.55rem;
  z-index: 9;
  background: white;
}
</style>
