import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/logout/";

const login = {
  namespaced: true,
  state: {
    loadingGetLogin: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchLogin: false, // for loading post/patch
    dataLogin: [], // for v-data-table
    dataActiveLogin: [], //for dropdown
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
    edittedItem: null,
    edittedItemHistories: [],
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
      console.log("logout")
      commit("GET_INIT");
      getAPI
        .get("/api/logout")
        .then((response) => {
          console.log(response);
          commit("GET_SUCCESS", sorted);
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
            console.log(response)
            resolve(response);
          })
          .catch((error) => {
            console.log(error)
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  // if (error.response.data.hasOwnProperty("login_name")) {
                  //   errorMsg += error.response.data.login_name;
                  // }
                  break;

                default:
                  errorMsg += `Please recheck your input or try again later`;
                  break;
              }
            }
            commit("POST_PATCH_ERROR", errorMsg);
            reject(errorMsg);
          });
      });
    },
  },
  mutations: {
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetLogin = true;
    },
    GET_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingGetLogin = false;
    },
    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchMasterlogin = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchMasterlogin = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchMasterlogin = false;
      state.errorMsg = error;
    },
  },
};

export default logout;
