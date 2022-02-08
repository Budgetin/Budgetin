import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js";

const ENDPOINT = "/api/login/";
const SECONDENDPOINT = "/api/logout/";

const login = {
  namespaced: true,
  state: {
    userInitial: "",
    loadingGetLogout: false, // for loading table
    loadingPostPatchLogin: false, // for loading post/patch
    dataLogin: [], // for v-data-table
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
    loadingGetInitial: false,
  },
  getters: {
    isAuthenticated: state => state.userInitial,
  },
  actions: {
    logOut({ commit }) {
      commit("GET_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .get(SECONDENDPOINT)
          .then((response) => {
            commit("GET_SUCCESS");
            resolve(response);
          })
          .catch((error) => {
            commit("GET_ERROR", error);
            reject(error);
          });
      });
    },

    setInitial({ commit }) {
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + "user/")
          .then((response) => {
            commit("GET_INITIAL_SUCCESS", response.data.initial);
            resolve(response);
          })
          .catch((error) => {
            commit("GET_INITIAL_ERROR", error);
            reject(error);
          });
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
            console.log(error);
            let errorMsg = `Please recheck your input or try again later`;
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
      router.push({ name: "Login" });
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetLogout = false;
      state.errorMsg = error;
    },

    GET_INITIAL_SUCCESS(state, initial) {
      state.requestStatus = "SUCCESS";
      state.loadingGetInitial = false;
      state.userInitial = initial;
    },
    GET_INITIAL_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetInitial = false;
      state.errorMsg = error;
      state.userInitial = "";
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
      state.userInitial = "";
      state.errorMsg = error;
    },
  },
};

export default login;
