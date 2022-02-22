import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const PROJECT_DETAIL_ENDPOINT = "api/project_detail/";
const AUDITLOG_ENDPOINT = "/api/auditlog/"

const projectDetail = {
  namespaced: true,
  state: {
    // get All Project Detail
    requestListAllProjectDetailStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListAllProjectDetail: false, // for loading table
    dataListAllProjectDetail: [], // for v-data-table
    // get Project Detail by Id
    requestProjectDetailByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetProjectDetailById: false, // for loading table
    dataProjectDetailById: null, // for data item
    // save Project Detail by Id
    requestSaveProjectDetailByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingSaveProjectDetailById: false, // for loading
    // delete Project Detail by Id
    requestDeleteProjectDetailByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDeleteProjectDetailById: false, // for loading
    // get List Project Detail History By Id
    requestListProjectDetailHistoryByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListProjectDetailHistoryById: false, // for loading table
    dataListProjectDetailHistoryById: [], // for v-data-table  

  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    getProjectDetail({ commit }) {
      commit("GET_INIT_ALL_PROJECT_DETAIL");
      getAPI
        .get(PROJECT_DETAIL_ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_ALL_PROJECT_DETAIL", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_ALL_PROJECT_DETAIL", error.message);
        });
    },

    getProjectDetailById({ commit }, id) {
      commit("GET_INIT_PROJECT_DETAIL_BY_ID");

      return new Promise((resolve, reject) => {
        getAPI
          .get(PROJECT_DETAIL_ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("GET_SUCCESS_PROJECT_DETAIL_BY_ID", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR_PROJECT_DETAIL_BY_ID", error.message);
            reject(error.message);
          });
      });
    },

    saveProjectDetailById({ commit }, payload) {
      commit("PATCH_INIT_SAVE_PROJECT_DETAIL_BY_ID");
      const url = `${PROJECT_DETAIL_ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("PATCH_SUCCESS_SAVE_PROJECT_DETAIL_BY_ID");
            // store.dispatch("projectDetail/getProjectDetail");
          })
          .catch((error) => {
            commit("PATCH_ERROR_SAVE_PROJECT_DETAIL_BY_ID", error.message);
            reject(error.message);
          });
      });
    },

    deleteProjectDetailById({ commit }, id) {
      commit("DELETE_INIT_DELETE_PROJECT_DETAIL_BY_ID");
      return new Promise((resolve, reject) => {
        getAPI
          .delete(PROJECT_DETAIL_ENDPOINT + `${id}/`)
          .then((response) => {
            commit("DELETE_SUCCESS_DELETE_PROJECT_DETAIL_BY_ID");
            resolve(response);
            // store.dispatch("projectDetail/getProjectDetail");
          })
          .catch((error) => {
            commit("DELETE_ERROR_DELETE_PROJECT_DETAIL_BY_ID", error.message);
            reject(error.message);
          });
      });
    },

    getListProjectDetailHistoryById({ commit }, id) {
      commit("GET_INIT_LIST_PROJECT_DETAIL_HISTORY_BY_ID"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get(AUDITLOG_ENDPOINT + "?table=project_detail&entity=" + `${id}`)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("GET_SUCCESS_LIST_PROJECT_DETAIL_HISTORY_BY_ID", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_LIST_PROJECT_DETAIL_HISTORY_BY_ID", error.message);
          reject(error.message);
        });
      });
    },
  },
  mutations: {
    // get List All Project Detail related
    GET_INIT_ALL_PROJECT_DETAIL(state) {
      state.requestListAllProjectDetailStatus = "PENDING";
      state.loadingGetListAllProjectDetail = true;
    },
    GET_SUCCESS_ALL_PROJECT_DETAIL(state, dataListAllProjectDetail) {
      state.requestListAllProjectDetailStatus = "SUCCESS";
      state.loadingGetListAllProjectDetail = false;
      state.dataListAllProjectDetail = dataListAllProjectDetail;
    },
    GET_ERROR_ALL_PROJECT_DETAIL(state, error) {
      state.requestListAllProjectDetailStatus = "ERROR";
      state.loadingGetListAllProjectDetail = false;
      state.dataListAllProjectDetail = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get Project Detail By Id related
    GET_INIT_PROJECT_DETAIL_BY_ID(state) {
      state.requestProjectDetailByIdStatus = "PENDING";
      state.loadingGetProjectDetailById = true;
    },
    GET_SUCCESS_PROJECT_DETAIL_BY_ID(state, dataProjectDetailById) {
      state.requestProjectDetailByIdStatus = "SUCCESS";
      state.loadingGetProjectDetailById = false;
      state.dataProjectDetailById = dataProjectDetailById;
    },
    GET_ERROR_PROJECT_DETAIL_BY_ID(state, error) {
      state.requestProjectDetailByIdStatus = "ERROR";
      state.loadingGetProjectDetailById = false;
      state.dataProjectDetailById = null;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // save Project Detail By Id related
    PATCH_INIT_SAVE_PROJECT_DETAIL_BY_ID(state) {
      state.requestSaveProjectDetailByIdStatus = "PENDING";
      state.loadingSaveProjectDetailById = true;
    },
    PATCH_SUCCESS_SAVE_PROJECT_DETAIL_BY_ID(state) {
      state.requestSaveProjectDetailByIdStatus = "SUCCESS";
      state.loadingSaveProjectDetailById = false;
    },
    PATCH_ERROR_SAVE_PROJECT_DETAIL_BY_ID(state, error) {
      state.requestSaveProjectDetailByIdStatus = "ERROR";
      state.loadingSaveProjectDetailById = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // delete Project Detail By Id related
    DELETE_INIT_DELETE_PROJECT_DETAIL_BY_ID(state) {
      state.requestDeleteProjectDetailByIdStatus = "PENDING";
      state.loadingDeleteProjectDetailById = true;
    },
    DELETE_SUCCESS_DELETE_PROJECT_DETAIL_BY_ID(state) {
      state.requestDeleteProjectDetailByIdStatus = "SUCCESS";
      state.loadingDeleteProjectDetailById = false;
    },
    DELETE_ERROR_DELETE_PROJECT_DETAIL_BY_ID(state, error) {
      state.requestDeleteProjectDetailByIdStatus = "ERROR";
      state.loadingDeleteProjectDetailById = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get List Project Detail History By Id related
    GET_INIT_LIST_PROJECT_DETAIL_HISTORY_BY_ID(state) {
      state.requestListProjectDetailHistoryByIdStatus = "PENDING";
      state.loadingGetListProjectDetailHistoryById = true;
    },
    GET_SUCCESS_LIST_PROJECT_DETAIL_HISTORY_BY_ID(state, dataListProjectDetailHistoryById) {
      state.requestListProjectDetailHistoryByIdStatus = "SUCCESS";
      state.loadingGetListProjectDetailHistoryById = false;
      state.dataListProjectDetailHistoryById = dataListProjectDetailHistoryById;
    },
    GET_ERROR_LIST_PROJECT_DETAIL_HISTORY_BY_ID(state, error) {
      state.requestListProjectDetailHistoryByIdStatus = "ERROR";
      state.loadingGetListProjectDetailHistoryById = false;
      state.dataListProjectDetailHistoryById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default projectDetail
