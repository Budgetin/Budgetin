<template>
    <v-container class="mt-5">
        <v-row>COA: {{data.serialized_data.coa}}</v-row>
        <v-row>Expense Type: {{data.serialized_data.expense_type}}</v-row>
        <v-row>Allocate: {{data.serialized_data.allocate}}</v-row>
        <v-row>Top Up: {{data.serialized_data.top_up}}</v-row>
        <v-row>Return: {{data.serialized_data.return}}</v-row>
        <v-row>Switching In: {{data.serialized_data.switching_in}}</v-row>
        <v-row>Switching Out: {{data.serialized_data.switching_out}}</v-row>
        <v-row>Realization January: {{data.serialized_data.realization_jan}}</v-row>
        <v-row>Realization February: {{data.serialized_data.realization_feb}}</v-row>
        <v-row>Realization March: {{data.serialized_data.realization_mar}}</v-row>
        <v-row>Realization April: {{data.serialized_data.realization_apr}}</v-row>
        <v-row>Realization May: {{data.serialized_data.realization_may}}</v-row>
        <v-row>Realization June: {{data.serialized_data.realization_jun}}</v-row>
        <v-row>Realization July: {{data.serialized_data.realization_jul}}</v-row>
        <v-row>Realization August: {{data.serialized_data.realization_aug}}</v-row>
        <v-row>Realization September: {{data.serialized_data.realization_sep}}</v-row>
        <v-row>Realization October: {{data.serialized_data.realization_oct}}</v-row>
        <v-row>Realization November: {{data.serialized_data.realization_nov}}</v-row>
        <v-row>Realization December: {{data.serialized_data.realization_dec}}</v-row>
    </v-container>
</template>

<script>
export default {
  name: "ItemLogBudgetRealization",
  props: ["data"],
  computed:{

  }
}

</script>