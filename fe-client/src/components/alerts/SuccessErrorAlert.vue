<template>
  <alert-base
    :status="status"
    :show="show"
    :title="title"
    :subtitle="subtitle"
    :persistent="true"
  >
    <template v-slot:content>
      <v-btn
        rounded
        :color="buttonColor"
        @click="$emit('okClicked')"
        :outlined="!success"
      >
        {{ buttonText }}
      </v-btn>
    </template>
  </alert-base>
</template>
<script>
import AlertBase from "./base/AlertBase";
export default {
  name: "AlertSuccess",
  props: ["show", "title", "subtitle", "success"],
  components: { AlertBase },
  computed: {
    status() {
      return this.success ? "success" : "error";
    },
    buttonText() {
      return this.success ? "Ok, Great!" : "Oh, Snap!";
    },
    buttonColor() {
      return this.success ? "primary" : "red";
    },
  },
};
</script>