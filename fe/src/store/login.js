import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/login/";

const login = {
  namespaced: true,
  state: {
    loadingPostPatchMasterlogin: false, // for loading post/patch
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    postMasterlogin({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
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

export default login;
