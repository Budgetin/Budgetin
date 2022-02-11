<template>
  <v-app id="login-form">
    <v-main class="conic-gradient">
      <v-container fluid fill-height>
        <v-row justify="center">
          <v-card min-height="" min-width="550px">
            <div class="pa-8">
              <v-card-title class="justify-center title mb-15"
                >WELCOME BACK!</v-card-title
              >
              <v-card-text>
                <v-form
                  ref="form"
                  v-model="valid"
                  lazy-validation
                  @submit.prevent="handleLogin"
                >
                  <v-text-field
                    prepend-icon="mdi-account"
                    v-model="username"
                    :rules="[(v) => !!v || 'User Domain is required!']"
                    type="text"
                    color="secondary"
                    label="Username"
                    outlined
                    required
                  ></v-text-field>

                  <v-text-field
                    prepend-icon="mdi-lock"
                    v-model="password"
                    :rules="[(v) => !!v || 'Password is required!']"
                    color="secondary"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="showPassword = !showPassword"
                    :type="showPassword ? 'text' : 'password'"
                    outlined
                    required
                    label="Password"
                  ></v-text-field>

                  <div class="my-3"></div>

                  <v-btn
                    block
                    rounded
                    x-large
                    color="primary lighten-2"
                    class="white--text ml-5"
                    depressed
                    type="submit"
                    :disabled="!valid"
                    :loading="loading"
                  >
                    <!-- @click="handleLogin" -->
                    Sign In
                  </v-btn>
                </v-form>
              </v-card-text>
            </div>
          </v-card>
        </v-row>
        <!-- <success-error-alert
          :success="alert.success"
          :show="alert.show"
          :title="alert.title"
          :subtitle="alert.subtitle"
          @okClicked="onAlertOk"
        /> -->
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapActions, mapState } from "vuex";
// import SuccessErrorAlert from "@/components/alerts/SuccessErrorAlert.vue";

export default {
  name: "Login",
  // components: { SuccessErrorAlert },
  data() {
    return {
      valid: true,
      username: "",
      password: "",
      errorMsg: "",
      showPassword: false,
      loading: false,
      initial:"",
      alert: {
        show: false,
        success: null,
        title: null,
        subtitle: null,
      },
    };
  },
  created() {
  },
  methods: {
    ...mapActions("login", ["postLogin", "setInitial"]),
    handleLogin() {
      // //console. = "";
      this.$refs.form.validate();
      this.valid = false;
      if (this.username && this.password) {
        this.loading = true;
        const payload = {
          username: this.username,
          password: this.password,
        };
        this.postLogin(JSON.parse(JSON.stringify(payload)))
          .then(() => {
            this.onSubmitSuccess();
          })
          .catch((error) => {
            this.onSubmitError(error);
          });
      }
    },
    onSubmitSuccess() {
      this.alert.show = true;
      this.alert.success = true;
      this.alert.title = "Login Success";
      this.alert.subtitle = "Successfully Login";
    },
    onAlertOk() {
      this.alert.show = false;
      this.valid = true;
      this.loading = false;
      if (this.alert.success) {
        this.$router.push({ path: "/coa" });
      }
    },
    onSubmitError(error) {
      this.alert.show = true;
      this.alert.success = false;
      this.alert.title = "Submit Failed";
      this.alert.subtitle = error;
    },
  },
};
</script>

<style scoped>
.v-application .title {
  font-size: 1.7rem !important;
  font-weight: 700;
  color: #333333;
}

.v-text-field--outlined >>> fieldset {
  border-color: #8699da;
}

.input-label {
  font-size: 1.2rem;
}

.conic-gradient {
  background: #3a1c71;
  background: -webkit-conic-gradient(
    from -10deg,
    #004da9,
    #a1cff3,
    #cea9ed,
    #004da9
  );
  background: conic-gradient(from -10deg, #004da9, #a1cff3, #cea9ed, #004da9);
}

.v-btn {
  width: 98% !important;
}
</style>
