import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/login/";
const SECONDENDPOINT = "/api/logout/"

const login = {
  namespaced: true,
  state: {
    userInitial :"Admin",
    loadingGetLogout: false, // for loading table
    loadingPostPatchLogin: false, // for loading post/patch
    dataLogin: [], // for v-data-table
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    logOut() {
      if (store.state.login.requestStatus !== "SUCCESS")
        store.dispatch("login/setLogout");
    },
    setLogout({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(SECONDENDPOINT)
        .then(() => {
          commit("GET_SUCCESS");
        })
        .catch((error) => {
          commit("GET_ERROR", error);
        });
    },

    postLogin({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            commit("POST_PATCH_SUCCESS", response.data.initial);
            resolve(response);
          })
          .catch((error) => {
            console.log(error)
            let errorMsg =
            `Please recheck your input or try again later`;
            commit("POST_PATCH_ERROR", errorMsg);
            reject(errorMsg);
          });
      });
    },
  },
  mutations: {
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetLogout = true;
    },
    GET_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingGetLogout = false;
      router.push({ name: 'Login'});
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetLogout = false;
      state.errorMsg = error;
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchLogin = true;
    },
    POST_PATCH_SUCCESS(state, initial) {
      state.postPatchStatus = "SUCCESS";
      state.loadingPostPatchLogin = false;
      state.userInitial = initial;
    },
    POST_PATCH_ERROR(state, error) {
      state.postPatchStatus = "ERROR";
      state.loadingPostPatchLogin = false;
      state.errorMsg = error;
    },
  },
};

export default login;
