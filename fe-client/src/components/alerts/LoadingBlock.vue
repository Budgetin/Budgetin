<template>
    <v-overlay :value="loadingStatus">
        <v-progress-circular
            indeterminate
            size="64"
        ></v-progress-circular>
    </v-overlay>
</template>

<script>
export default {
    name: "LoadingBlock",
    props:{
        loadingStatus: {
            type: Boolean,
            default: () => false,
        },
    }
}
</script>

<style lang="scss" scoped>

</style>