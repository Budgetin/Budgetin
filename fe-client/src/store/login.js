import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js";

const ENDPOINT = "/api/login/";
const SECONDENDPOINT = "/api/logout/";

const login = {
  namespaced: true,
  state: {
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchLogin: false, // for loading post/patch
    userInitial: "", // for data Initial
    userRole: "", // for data Role
    getInitialStatus: "IDLE",// possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetInitial: false, // for loading intial
    loadingGetLogout: false, // for loading table
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
  },
  getters: {
    isAuthenticated: state => state.userInitial,
    isUser: state => state.userRole == "User" ? true : false,
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
          .get(ENDPOINT + "user/?role=user")
          .then((response) => {
            commit("GET_INITIAL_SUCCESS", response.data);
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
            if(!response.data.message){
              commit("POST_PATCH_SUCCESS", response.data);
              resolve(response);
            }
            else{
              throw new Error("403");
            }
            
          })
          .catch((error) => {
            let errorMsg = error.message == '403' ? 
                          `You have insufficient permission`:
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
      router.push({ name: "Login" });
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetLogout = false;
      state.errorMsg = error;
    },

    GET_INITIAL_SUCCESS(state, data) {
      state.getInitialStatus = "SUCCESS";
      state.loadingGetInitial = false;
      state.userInitial = data.initial;
      state.userRole = data.role;
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
    POST_PATCH_SUCCESS(state, data) {
      state.postPatchStatus = "SUCCESS";
      state.loadingPostPatchLogin = false;
      state.userInitial = data.initial;
      state.userRole = data.role;
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
