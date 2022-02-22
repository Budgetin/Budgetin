import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const ENDPOINT = "/api/project/";

const myProject = {
  namespaced: true,
  state: {
    //getMyProject
    requestMyProjectStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMyProject: false, // for loading table
    dataMyProject: [], // for v-data-table

    //getMyProjectById
    requestMyProjectByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMyProjectById: false, // for loading table
    dataMyProjectById: null,

    //postMyProject & patchMyProject
    requestPostPatchMyProjectStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchMyProject: false, // for loading post/patch

    //getHistoryMyProject
    requestGetHistoryMyProjectStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetHistoryMyProject: false, // for loading post/patch
    dataHistoryMyProject: [],
  },
  getters: {
  },
  actions: {
    getMyProject({ commit }) {
      commit("GET_INIT_MY_PROJECT");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_MY_PROJECT", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_MY_PROJECT", error);
        });
    },

    getMyProjectById({ commit }, id) {
      commit("GET_INIT_MY_PROJECT_BY_ID", true);
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("GET_SUCCESS_MY_PROJECT_BY_ID", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR_MY_PROJECT_BY_ID", error);
            reject(error);
          });
      });
    },

    postMyProject({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("myProject/getMyProject");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },

    patchMyProject({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("myProject/getMyProject");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },
    
    getHistoryMyProject({ commit }, id) {
      commit("GET_INIT_MY_PROJECT_HISTORY"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=myproject&entity=" + `${id}`)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("GET_SUCCESS_MY_PROJECT_HISTORY", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_MY_PROJECT_HISTORY", error);
          reject(error);
        });
      });
    },
  },

  mutations: {
    // getMyProject related
    GET_INIT_MY_PROJECT(state) {
      state.requestMyProjectStatus = "PENDING";
      state.loadingGetMyProject = true;
    },
    GET_SUCCESS_MY_PROJECT(state, dataMyProject) {
      state.requestMyProjectStatus = "SUCCESS";
      state.loadingGetMyProject = false;
      state.dataMyProject = dataMyProject;
    },
    GET_ERROR_MY_PROJECT(state, error) {
      state.requestMyProjectStatus = "ERROR";
      state.loadingGetMyProject = false;
      state.dataMyProject = [];
      state.dataActiveMyProject = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // getMyProjectById related
    GET_INIT_MY_PROJECT_BY_ID(state) {
      // state.loadingGetEdittedItem = payload;
      state.requestMyProjectByIdStatus = "PENDING";
      state.loadingGetMyProjectById = true;
    },
    GET_SUCCESS_MY_PROJECT_BY_ID(state, payload) {
      // state.edittedItem = payload;
      state.requestMyProjectByIdStatus = "SUCCESS";
      state.loadingGetMyProjectById = false;
      state.dataMyProjectById = payload;
    },
    GET_ERROR_MY_PROJECT_BY_ID(state, error) {
      state.requestMyProjectByIdStatus = "ERROR";
      state.loadingGetMyProjectById = false;
      state.dataMyProjectById = [];
      state.dataActiveMyProject = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post/patch related
    POST_PATCH_INIT(state) {
      state.requestPostPatchMyProjectStatus = "PENDING";
      state.loadingPostPatchMyProject = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestPostPatchMyProjectStatus = "SUCCESS";
      state.loadingPostPatchMyProject = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestPostPatchMyProjectStatus = "ERROR";
      state.loadingPostPatchMyProject = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // history relate
    GET_INIT_MY_PROJECT_HISTORY(state) {
      state.requestGetHistoryMyProjectStatus = "PENDING";
      state.loadingGetHistoryMyProject = true;
      state.dataHistoryMyProject = [];
    },
    GET_SUCCESS_MY_PROJECT_HISTORY(state, dataHistoryMyProject) {
      // state.edittedItem = payload;
      state.requestGetHistoryMyProjectStatus = "SUCCESS";
      state.loadingGetHistoryMyProject = false;
      state.dataHistoryMyProject = dataHistoryMyProject;
    },
    GET_ERROR_MY_PROJECT_HISTORY(state, error) {
      state.requestGetHistoryMyProjectStatus = "ERROR";
      state.loadingGetHistoryMyProject = false;
      state.dataHistoryMyProject = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default myProject
