import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const ENDPOINT = "/api/planning/";

const startPlanning = {
  namespaced: true,
  state: {
    //getStartPlanning
    requestGetStartPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetStartPlanning: false, // for loading table
    dataStartPlanning: [], // for v-data-table

    //getStartPlanningById
    requestGetStartPlanningByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetStartPlanningById: false, // for loading table
    dataStartPlanningById: null,

    //postStartPlanning & patchStartPlanning
    requestPostPatchStartPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchStartPlanning: false, // for loading table

    //getHistoryStartPlanning
    requestGetHistoryStartPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetHistoryStartPlanning: false, // for loading table
    dataHistoryStartPlanning: [],
  },
  getters: {
  },
  actions: {
    getStartPlanning({ commit }) {
      commit("GET_INIT_START_PLANNING");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_START_PLANNING", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_START_PLANNING", error);
        });
    },

    getStartPlanningById({ commit }, id) {
      commit("GET_INIT_START_PLANNING_BY_ID", true);
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("GET_SUCCESS_START_PLANNING_BY_ID", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR_START_PLANNING_BY_ID", error);
            reject(error);
          });
      });
    },

    postStartPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("startPlanning/getStartPlanning");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error);
            reject(error.response.data.year);
          });
      });
    },

    patchStartPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("startPlanning/getStartPlanning");
          })
          .catch((error) => {
            reject(errorMsg);
            commit("POST_PATCH_ERROR", error.response.data);
          });
      });
    },

    getHistoryStartPlanning({ commit }, id) {
      commit("GET_INIT_START_PLANNING_HISTORY"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=planning&entity=" + `${id}`)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("GET_SUCCESS_START_PLANNING_HISTORY", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_START_PLANNING_HISTORY", error);
          reject(error);
        });
      });
    },
  },

  mutations: {
    // getStartPlanning related
    GET_INIT_START_PLANNING(state) {
      state.requestGetStartPlanningStatus = "PENDING";
      state.loadingGetStartPlanning = true;
    },
    GET_SUCCESS_START_PLANNING(state, dataStartPlanning) {
      state.requestGetStartPlanningStatus = "SUCCESS";
      state.loadingGetStartPlanning = false;
      state.dataStartPlanning = dataStartPlanning;
    },
    GET_ERROR_START_PLANNING(state, error) {
      state.requestGetStartPlanningStatus = "ERROR";
      state.loadingGetStartPlanning = false;
      state.dataStartPlanning = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // getStartPlanningById related
    GET_INIT_START_PLANNING_BY_ID(state) {
      state.requestGetStartPlanningByIdStatus = "PENDING";
      state.loadingGetStartPlanningById = true;
    },
    GET_SUCCESS_START_PLANNING_BY_ID(state, payload) {
      state.requestGetStartPlanningByIdStatus = "SUCCESS";
      state.loadingGetStartPlanningById = false;
      state.dataStartPlanningById = payload;
    },
    GET_ERROR_START_PLANNING_BY_ID(state, error) {
      state.requestGetStartPlanningByIdStatus = "ERROR";
      state.loadingGetStartPlanningById = false;
      state.dataStartPlanningById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post/patch related
    POST_PATCH_INIT(state) {
      state.requestPostPatchStartPlanningStatus = "PENDING";
      state.loadingPostPatchStartPlanning = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestPostPatchStartPlanningStatus = "SUCCESS";
      state.loadingPostPatchStartPlanning = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestPostPatchStartPlanningStatus = "ERROR";
      state.loadingPostPatchStartPlanning = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // history relate
    GET_INIT_START_PLANNING_HISTORY(state) {
      state.requestGetHistoryStartPlanningStatus = "PENDING";
      state.loadingGetHistoryStartPlanning = true;
      state.dataHistoryStartPlanning = [];
    },
    GET_SUCCESS_START_PLANNING_HISTORY(state, dataHistoryStartPlanning) {
      // state.edittedItem = payload;
      state.requestGetHistoryStartPlanningStatus = "SUCCESS";
      state.loadingGetHistoryStartPlanning = false;
      state.dataHistoryStartPlanning = dataHistoryStartPlanning;
    },
    GET_ERROR_START_PLANNING_HISTORY(state, error) {
      state.requestGetHistoryStartPlanningStatus = "ERROR";
      state.loadingGetHistoryStartPlanning = false;
      state.dataHistoryStartPlanning = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default startPlanning
