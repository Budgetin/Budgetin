<template>
  <v-app id="inspire">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Login Form</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    prepend-icon="mdi-account"
                    type="text"
                    v-model="username"
                    :rules="validation.required"
                    label="Username"
                  >
                  </v-text-field>
                  <v-text-field
                    prepend-icon="mdi-account"
                    type="password"
                    v-model="password"
                    :rules="validation.required"
                    label="Password"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="submit">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
    name: "Login",
    props: {
        source: String,
    },
    data: () => ({
        username: "",
        password: "",
        validation: {
            required: [
                (v) => !!v || "This field is required"
            ],
        },
    }),
    methods: {
        ...mapActions("login", ["postLogin"]),
        submit() {
            if (this.username &&this.password) {
                const payload = {
                    username:this.username,
                    password:this.password,
                };
                console.log(payload)
                this.postLogin(JSON.parse(JSON.stringify(payload)))
                    .then(() => {
                        console.log("berhasil")
                    })
                    .catch((error) => {
                        console.log(error)
                    });
            }
        }
    }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Nunito&display=swap");
.v-toolbar__title {
    font-family: "Nunito", sans-serif !important;
}
.v-text-field input {
    font-family: "Nunito", sans-serif !important;
}
</style>
