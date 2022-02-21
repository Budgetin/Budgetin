import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/strategy/";
const LOGENDPOINT="/api/auditlog?table=strategy&entity=";

const masterStrategy = {
  namespaced: true,
  state: {
    // Get All Data Strategy
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterStrategy: false, // for loading table
    dataMasterStrategy: [], // for v-data-table
    
    // Get Master Strategy By Id
    requestMasterStrategyByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterStrategyById: false, // for loading table
    dataMasterStrategyById: [], // for v-data-table

    // Post/Patch Master Strategy
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchMasterStrategy: false, // for loading action

    // Delete Master Strategy
    requestDeleteStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDeleteMasterStrategy: false, // for loading action

    // Get History Master Strategy By Id
    requestHistoryMasterStrategyStatus:"IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetHistoryMasterStrategy:false, // for loading table
    dataHistoryMasterStrategy:[], // for v-data-table
   
    // Upload Master Strategy
    requestImportStrategyStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingImportStrategy: false, // for loading data
    errorMsgImportStrategy: null,
  },
  getters: {
  },
  actions: {
    getMasterStrategy({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.id < b.id ? 1 : -1
          );
          commit("GET_SUCCESS", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
        });
    },
    
    getMasterStrategyById({ commit }, id) {
      commit("GET_INIT_STRATEGY_BY_ID");
      const url = `${ENDPOINT}${id}/`
      return new Promise((resolve, reject) => {
        getAPI
          .get(url)
          .then((response) => {
            const data = response.data;
            commit("GET_SUCCESS_STRATEGY_BY_ID", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR_STRATEGY_BY_ID", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },

    postMasterStrategy({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterStrategy/getMasterStrategy");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },

    patchMasterStrategy({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterStrategy/getMasterStrategy");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },
       
    deleteMasterStrategyById({ commit }, id) {
      commit("DELETE_INIT");
      const url = `${ENDPOINT}${id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .delete(url)
          .then((response) => {
            const data = response.data;
            commit("DELETE_SUCCESS");
            resolve(data);
            store.dispatch("masterStrategy/getMasterStrategy");
          })
          .catch((error) => {
            commit("DELETE_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },

    getHistory({ commit }, id) {
      commit("GET_INIT_HISTORY_MASTER_STRATEGY");
      const url = `${LOGENDPOINT}${id}`;
      return new Promise((resolve, reject) => {
      getAPI
        .get(url)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("GET__HISTORY_MASTER_STRATEGY_SUCCESS", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET__HISTORY_MASTER_STRATEGY_ERROR", error);
          if(error.response.data.message){
            reject(error.response.data.message);
          }else{
            reject(error);
          }
        });
      });
    },
    
    importStrategy({ commit }, data) {
      commit("GET_INIT_IMPORT_STRATEGY");
      let formData = new FormData();
      formData.append("file", data.files);

      return new Promise((resolve, reject) => {
        getAPI
          .post((ENDPOINT+"import/"), formData)
          .then((res) => {
            resolve(res);
            store.dispatch('masterStrategy/getMasterStrategy')
            commit("GET_SUCCESS_IMPORT_STRATEGY");
          })
          .catch((err) => {
            commit("GET_ERROR_IMPORT_STRATEGY", err);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    }
  },
  mutations: {

    // Get List of Strategy Related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetMasterStrategy = true;
    },
    GET_SUCCESS(state, data) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterStrategy = false;
      state.dataMasterStrategy = data;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterStrategy = false;
      state.dataMasterStrategy = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // Get Data Strategy By ID
    GET_INIT_STRATEGY_BY_ID(state) {
      state.requestMasterStrategyByIdStatus = "PENDING";
      state.loadingGetMasterStrategyById = true;
    },
    GET_SUCCESS_STRATEGY_BY_ID(state, data) {
      state.requestMasterStrategyByIdStatus = "SUCCESS";
      state.loadingGetMasterStrategyById = false;
      state.dataMasterStrategyById = data;
    },
    GET_ERROR_STRATEGY_BY_ID(state, error) {
      state.requestMasterStrategyByIdStatus = "ERROR";
      state.loadingGetMasterStrategyById = false;
      state.dataMasterStrategyById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // Post / Patch Master Strategy
    POST_PATCH_INIT(state) {
      state.requestPostPatchStatus = "PENDING";
      state.loadingPostPatchMasterStrategy = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestPostPatchStatus = "SUCCESS";
      state.loadingPostPatchMasterStrategy = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestPostPatchStatus = "ERROR";
      state.loadingPostPatchMasterStrategy = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    
    // delete Master Strategy By ID
    DELETE_INIT(state, payload) {
      state.requestDeleteStatus = "PENDING";
      state.loadingDeleteMasterStrategy = true;
    },
    DELETE_SUCCESS(state, payload) {
      state.requestDeleteStatus = "SUCCESS";
      state.loadingDeleteMasterStrategy = false;
    },
    DELETE_ERROR(state, error) {
      state.requestDeleteStatus = "ERROR";
      state.loadingDeleteMasterStrategy = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // Get History Master Strategy By ID
    GET_INIT_HISTORY_MASTER_STRATEGY(state) {
      state.requestHistoryMasterStrategyStatus = "PENDING";
      state.loadingGetHistoryMasterStrategy = true;
    },
    GET__HISTORY_MASTER_STRATEGY_SUCCESS(state, data) {
      state.requestHistoryMasterStrategyStatus = "SUCCESS";
      state.loadingGetHistoryMasterStrategy = false;
      state.dataHistoryMasterStrategy = data;
    },
    GET__HISTORY_MASTER_STRATEGY_ERROR(state, error) {
      state.requestHistoryMasterStrategyStatus = "ERROR";
      state.loadingGetHistoryMasterStrategy = false;
      state.dataHistoryMasterStrategy = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // import related
    GET_INIT_IMPORT_STRATEGY(state) {
      state.requestImportStrategyStatus = "PENDING";
      state.loadingImportStrategy = true;
    },
    GET_SUCCESS_IMPORT_STRATEGY(state) {
      state.requestImportStrategyStatus = "SUCCESS";
      state.loadingImportStrategy = false;
    },
    GET_ERROR_IMPORT_STRATEGY(state, error) {
      state.requestImportStrategyStatus = "ERROR";
      state.loadingImportStrategy = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default masterStrategy;
