import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const ENDPOINT = "/api/monitoring/";

const monitorPlanning = {
  namespaced: true,
  state: {
    //getMonitorPlanning
    requestGetMonitorPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMonitorPlanning: false, // for loading table
    dataMonitorPlanning: [], // for v-data-table

    //getMonitorPlanningById
    requestGetMonitorPlanningByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMonitorPlanningById: false, // for loading table
    dataMonitorPlanningById: null,

    //getMonitorPlanningDetailById
    requestGetMonitorPlanningDetailByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMonitorPlanningDetailById: false, // for loading table
    dataMonitorPlanningDetailById: null,

    //postMonitorPlanning & patchMonitorPlanning
    requestPostPatchMonitorPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchMonitorPlanning: false, // for loading table

    //getHistoryMonitorPlanning
    requestGetHistoryMonitorPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetHistoryMonitorPlanning: false, // for loading table
    dataHistoryMonitorPlanning: [],
  },
  getters: {
  },
  actions: {
    getMonitorPlanning({ commit }) {
      commit("GET_INIT_MONITOR_PLANNING");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_MONITOR_PLANNING", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_MONITOR_PLANNING", error);
        });
    },

    getMonitorPlanningById({ commit }, id) {
      commit("GET_INIT_MONITOR_PLANNING_BY_ID", true);
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + "?planning=" + `${id}`)
          .then((response) => {
            const data = response.data;
            commit("GET_SUCCESS_MONITOR_PLANNING_BY_ID", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR_MONITOR_PLANNING_BY_ID", error);
            reject(error.message);
          });
      });
    },

    getMonitorPlanningDetailById({ commit }, id) {
      commit("GET_INIT_MONITOR_PLANNING_DETAIL_BY_ID", true);
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}`)
          .then((response) => {
            const data = response.data;
            commit("GET_SUCCESS_MONITOR_PLANNING_DETAIL_BY_ID", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR_MONITOR_PLANNING_DETAIL_BY_ID", error);
            reject(error);
          });
      });
    },

    postMonitorPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("monitorPlanning/getMonitorPlanning");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },

    patchMonitorPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("monitorPlanning/getMonitorPlanning");
          })
          .catch((error) => {
            reject(error.message);
            commit("POST_PATCH_ERROR", error.response.data);
          });
      });
    },

    getHistoryMonitorPlanning({ commit }, id) {
      commit("GET_INIT_MONITOR_PLANNING_HISTORY"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=monitoring&entity=" + `${id}`)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("GET_SUCCESS_MONITOR_PLANNING_HISTORY", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_MONITOR_PLANNING_HISTORY", error);
          reject(error);
        });
      });
    },
  },

  mutations: {
    // getMonitorPlanning related
    GET_INIT_MONITOR_PLANNING(state) {
      state.requestGetMonitorPlanningStatus = "PENDING";
      state.loadingGetMonitorPlanning = true;
    },
    GET_SUCCESS_MONITOR_PLANNING(state, dataMonitorPlanning) {
      state.requestGetMonitorPlanningStatus = "SUCCESS";
      state.loadingGetMonitorPlanning = false;
      state.dataMonitorPlanning = dataMonitorPlanning;
    },
    GET_ERROR_MONITOR_PLANNING(state, error) {
      state.requestGetMonitorPlanningStatus = "ERROR";
      state.loadingGetMonitorPlanning = false;
      state.dataMonitorPlanning = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // getMonitorPlanningById related
    GET_INIT_MONITOR_PLANNING_BY_ID(state) {
      state.requestGetMonitorPlanningByIdStatus = "PENDING";
      state.loadingGetMonitorPlanningById = true;
    },
    GET_SUCCESS_MONITOR_PLANNING_BY_ID(state, payload) {
      state.requestGetMonitorPlanningByIdStatus = "SUCCESS";
      state.loadingGetMonitorPlanningById = false;
      state.dataMonitorPlanningById = payload;
    },
    GET_ERROR_MONITOR_PLANNING_BY_ID(state, error) {
      state.requestGetMonitorPlanningByIdStatus = "ERROR";
      state.loadingGetMonitorPlanningById = false;
      state.dataMonitorPlanningById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // getMonitorPlanningDetailById related
    GET_INIT_MONITOR_PLANNING_DETAIL_BY_ID(state) {
      state.requestGetMonitorPlanningDetailByIdStatus = "PENDING";
      state.loadingGetMonitorPlanningDetailById = true;
    },
    GET_SUCCESS_MONITOR_PLANNING_DETAIL_BY_ID(state, payload) {
      state.requestGetMonitorPlanningDetailByIdStatus = "SUCCESS";
      state.loadingGetMonitorPlanningDetailById = false;
      state.dataMonitorPlanningDetailById = payload;
    },
    GET_ERROR_MONITOR_PLANNING_DETAIL_BY_ID(state, error) {
      state.requestGetMonitorPlanningDetailByIdStatus = "ERROR";
      state.loadingGetMonitorPlanningDetailById = false;
      state.dataMonitorPlanningDetailById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post/patch related
    POST_PATCH_INIT(state) {
      state.requestPostPatchMonitorPlanningStatus = "PENDING";
      state.loadingPostPatchMonitorPlanning = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestPostPatchMonitorPlanningStatus = "SUCCESS";
      state.loadingPostPatchMonitorPlanning = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestPostPatchMonitorPlanningStatus = "ERROR";
      state.loadingPostPatchMonitorPlanning = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // history relate
    GET_INIT_MONITOR_PLANNING_HISTORY(state) {
      state.requestGetHistoryMonitorPlanningStatus = "PENDING";
      state.loadingGetHistoryMonitorPlanning = true;
      state.dataHistoryMonitorPlanning = [];
    },
    GET_SUCCESS_MONITOR_PLANNING_HISTORY(state, dataHistoryMonitorPlanning) {
      // state.edittedItem = payload;
      state.requestGetHistoryMonitorPlanningStatus = "SUCCESS";
      state.loadingGetHistoryMonitorPlanning = false;
      state.dataHistoryMonitorPlanning = dataHistoryMonitorPlanning;
    },
    GET_ERROR_MONITOR_PLANNING_HISTORY(state, error) {
      state.requestGetHistoryMonitorPlanningStatus = "ERROR";
      state.loadingGetHistoryMonitorPlanning = false;
      state.dataHistoryMonitorPlanning = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default monitorPlanning
