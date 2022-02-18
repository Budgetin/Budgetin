<template>
    <v-container class="mt-5">
        <v-row>COA: {{data.serialized_data.coa}}</v-row>
        <v-row>Expense Type: {{data.serialized_data.expense_type}}</v-row>
        <v-row>Allocate: {{numberWithDots(this.data.serialized_data.allocate)}}</v-row>
        <v-row>Top Up: {{numberWithDots(this.data.serialized_data.top_up)}}</v-row>
        <v-row>Return: {{numberWithDots(this.data.serialized_data.return)}}</v-row>
        <v-row>Switching In: {{numberWithDots(this.data.serialized_data.switching_in)}}</v-row>
        <v-row>Switching Out: {{numberWithDots(this.data.serialized_data.switching_out)}}</v-row>
        <v-row>Realization January: {{numberWithDots(this.data.serialized_data.realization_jan)}}</v-row>
        <v-row>Realization February: {{numberWithDots(this.data.serialized_data.realization_feb)}}</v-row>
        <v-row>Realization March: {{numberWithDots(this.data.serialized_data.realization_mar)}}</v-row>
        <v-row>Realization April: {{numberWithDots(this.data.serialized_data.realization_apr)}}</v-row>
        <v-row>Realization May: {{numberWithDots(this.data.serialized_data.realization_may)}}</v-row>
        <v-row>Realization June: {{numberWithDots(this.data.serialized_data.realization_jun)}}</v-row>
        <v-row>Realization July: {{numberWithDots(this.data.serialized_data.realization_jul)}}</v-row>
        <v-row>Realization August: {{numberWithDots(this.data.serialized_data.realization_aug)}}</v-row>
        <v-row>Realization September: {{numberWithDots(this.data.serialized_data.realization_sep)}}</v-row>
        <v-row>Realization October: {{numberWithDots(this.data.serialized_data.realization_oct)}}</v-row>
        <v-row>Realization November: {{numberWithDots(this.data.serialized_data.realization_nov)}}</v-row>
        <v-row>Realization December: {{numberWithDots(this.data.serialized_data.realization_dec)}}</v-row>
    </v-container>
</template>

<script>
import formatting from "@/mixins/formatting";
export default {
  name: "ItemLogBudgetRealization",
  props: ["data"],
  mixins: [formatting],
  computed:{

  }
}

</script>