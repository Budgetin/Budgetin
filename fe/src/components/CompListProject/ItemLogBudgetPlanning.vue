<template>
    <v-container class="mt-5">
        <v-row>COA: {{data.serialized_data.coa}}</v-row>
        <v-row>Expense Type: {{data.serialized_data.expense_type}}</v-row>
        <!-- <v-row>Budget This Year: {{data.serialized_data.planning_nominal}}</v-row> -->
        <v-row>Planning Q1: {{data.serialized_data.planning_q1}}</v-row>
        <v-row>Planning Q2: {{data.serialized_data.planning_q2}}</v-row>
        <v-row>Planning Q3: {{data.serialized_data.planning_q3}}</v-row>
        <v-row>Planning Q4: {{data.serialized_data.planning_q4}}</v-row>
        <v-row>Status: {{getActive}}</v-row>
    </v-container>
</template>

<script>
export default {
  name: "ItemLogBudgetPlanning",
  props: ["data"],
  computed:{
    getActive(){
      return this.data.serialized_data.is_active == 1 ? "Active" : "Inactive";
    },
  }
}

</script>