import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const ENDPOINT = "/api/project/";

const listProject = {
  namespaced: true,
  state: {
    //getListProject
    requestListProjectStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListProject: false, // for loading table
    dataListProject: [], // for v-data-table

    //getListProjectById
    requestListProjectByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListProjectById: false, // for loading table
    dataListProjectById: null,

    //postListProject & patchListProject
    requestPostPatchListProjectStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchListProject: false, // for loading post/patch

    //getHistoryListProject
    requestGetHistoryListProjectStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetHistoryListProject: false, // for loading post/patch
    dataHistoryListProject: [],
  },
  getters: {
  },
  actions: {
    getListProject({ commit }) {
      commit("GET_INIT_LIST_PROJECT");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_LIST_PROJECT", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_LIST_PROJECT", error);
        });
    },

    getListProjectById({ commit }, id) {
      commit("GET_INIT_LIST_PROJECT_BY_ID", true);
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("GET_SUCCESS_LIST_PROJECT_BY_ID", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR_LIST_PROJECT_BY_ID", error);
            reject(error);
          });
      });
    },

    postListProject({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("listProject/getListProject");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },

    patchListProject({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("listProject/getListProject");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },
    
    getHistoryListProject({ commit }, id) {
      commit("GET_INIT_LIST_PROJECT_HISTORY"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=project&entity=" + `${id}`)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("GET_SUCCESS_LIST_PROJECT_HISTORY", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_LIST_PROJECT_HISTORY", error);
          reject(error);
        });
      });
    },
  },

  mutations: {
    // getListProject related
    GET_INIT_LIST_PROJECT(state) {
      state.requestListProjectStatus = "PENDING";
      state.loadingGetListProject = true;
    },
    GET_SUCCESS_LIST_PROJECT(state, dataListProject) {
      state.requestListProjectStatus = "SUCCESS";
      state.loadingGetListProject = false;
      state.dataListProject = dataListProject;
    },
    GET_ERROR_LIST_PROJECT(state, error) {
      state.requestListProjectStatus = "ERROR";
      state.loadingGetListProject = false;
      state.dataListProject = [];
      state.dataActiveListProject = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // getListProjectById related
    GET_INIT_LIST_PROJECT_BY_ID(state) {
      // state.loadingGetEdittedItem = payload;
      state.requestListProjectByIdStatus = "PENDING";
      state.loadingGetListProjectById = true;
    },
    GET_SUCCESS_LIST_PROJECT_BY_ID(state, payload) {
      // state.edittedItem = payload;
      state.requestListProjectByIdStatus = "SUCCESS";
      state.loadingGetListProjectById = false;
      state.dataListProjectById = payload;
    },
    GET_ERROR_LIST_PROJECT_BY_ID(state, error) {
      state.requestListProjectByIdStatus = "ERROR";
      state.loadingGetListProjectById = false;
      state.dataListProjectById = null;
      state.dataActiveListProject = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post/patch related
    POST_PATCH_INIT(state) {
      state.requestPostPatchListProjectStatus = "PENDING";
      state.loadingPostPatchListProject = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestPostPatchListProjectStatus = "SUCCESS";
      state.loadingPostPatchListProject = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestPostPatchListProjectStatus = "ERROR";
      state.loadingPostPatchListProject = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // history relate
    GET_INIT_LIST_PROJECT_HISTORY(state) {
      state.requestGetHistoryListProjectStatus = "PENDING";
      state.loadingGetHistoryListProject = true;
      state.dataHistoryListProject = [];
    },
    GET_SUCCESS_LIST_PROJECT_HISTORY(state, dataHistoryListProject) {
      // state.edittedItem = payload;
      state.requestGetHistoryListProjectStatus = "SUCCESS";
      state.loadingGetHistoryListProject = false;
      state.dataHistoryListProject = dataHistoryListProject;
    },
    GET_ERROR_LIST_PROJECT_HISTORY(state, error) {
      state.requestGetHistoryListProjectStatus = "ERROR";
      state.loadingGetHistoryListProject = false;
      state.dataHistoryListProject = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default listProject
