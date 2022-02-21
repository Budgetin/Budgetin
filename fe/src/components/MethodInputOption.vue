<template>
  <v-card>
    <v-card-title>
      How to Input
      <v-spacer></v-spacer>
      <v-btn icon small @click="$emit('cancelClicked')">
        <v-icon color="primary"> mdi-close </v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="6" class="mt-2" align="center" justify="center">
          <div
            class="choose-project-type_box"
            align="center"
            justify="center"
            @click="$emit('uploadClicked')"
          >
            <img
              :src="require('../assets/upload_2.gif')"
              height="80rem"
            /><br />
            Upload Excel
            <!-- <v-btn rounded color="primary" @click="onUpload"> Upload Excel </v-btn> -->
          </div>
        </v-col>
        <v-col cols="6" class="mt-2" align="center" justify="center">
          <div
            class="choose-project-type_box"
            align="center"
            justify="center"
            @click="$emit('formClicked')"
          >
            <img
              :src="require('../assets/new_project.gif')"
              height="80rem"
              style="padding: 0.2rem"
            /><br />
            Input Form
            <!-- <v-btn rounded color="primary" @click="onAdd"> Input Form </v-btn> -->
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "MethodInputOption",
  props: [],
  data: () => ({}),
  computed: {},
  methods: {},
};
</script>

<style scoped>
::v-deep .choose-project-type_box{
  border:3px rgb(228, 228, 228) solid;
  border-radius:20px;
  padding:0.5rem;
  width: 10rem;
  font-weight: 600;
  cursor:pointer;
}

::v-deep .choose-project-type_box:hover{
  border:3px rgb(93, 158, 243) solid;
  border-radius:20px;
  padding:0.5rem;
  width: 10rem;
  cursor:pointer;
}
</style>
