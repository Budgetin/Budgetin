<template>
    <v-row>COA Name: {item.serialized_data.name}</v-row>
    <v-row>Definition: {item.serialized_data.definition}</v-row>
    <v-row>Hyperion Text: {item.serialized_data.hyperion_name}</v-row>
    <v-row>Capex: {item.serialized_data.is_capex}</v-row>
    <v-row v-if="item.serialized_data.is_capex == 1">Minimum tobe CAPEX: {item.serialized_data.minimum_item_origin}</v-row>
</template>