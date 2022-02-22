import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/coa/";
const LOGENDPOINT="/api/auditlog?table=coa&entity=";

const masterCoa = {
  namespaced: true,
  state: {
    // get All data Master Coa
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterCoa: false, // for loading table
    dataMasterCoa: [], // for v-data-table

    // get All data Master Coa by ID    
    requestMasterCoaByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterCoaById: false, // for loading table
    dataMasterCoaById: [], // for v-data-table
    
    // Post/Patch Master COA   
    requestpostPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDeleteMasterCoa: false, // for loading table

    // Delete data Master Coa by ID    
    requestDeleteStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterCoaById: false, // for loading table

    // get History data Master Coa by ID    
    requestHistoryMasterCoaStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetHistoryMasterCoa: false, // for loading table

    // import Master Coa / Add Coa by upload file
    requestImportCoaStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingImportCoa: false, // for loading data

  },
  getters: {
    // value: (state) => state.value
  },
  actions: {
    getMasterCoa({ commit }) {
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
    
    getMasterCoaById({ commit }, id) {
      commit("GET_INIT_MASTER_COA_BY_ID");
      const url = `${ENDPOINT}${id}/`
      return new Promise((resolve, reject) => {
        getAPI
          .get(url)
          .then((response) => {
            const data = response.data;
            commit("GET_MASTER_COA_BY_ID_SUCCESS", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_MASTER_COA_BY_ID_ERROR", error);
            reject(error);
          });
      });
    },

    postMasterCoa({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterCoa/getMasterCoa");
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

    patchMasterCoa({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url,payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterCoa/getMasterCoa");
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

    deleteMasterCoa({ commit },id) {
      commit("DELETE_INIT");
      const url = `${ENDPOINT}${id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .delete(url)
          .then((response) => {
            store.dispatch("masterCoa/getMasterCoa");
            commit("DELETE_SUCCESS");
            resolve(response);
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
      commit("GET_INIT_HISTORY_MASTER_COA"); 
      const url = `${LOGENDPOINT}${id}`;
      return new Promise((resolve, reject) => {
        getAPI
          .get(url)
          .then((response) => {
            const data = response.data;
            const sorted = data.sort((a, b) =>
            a.id < b.id ? 1 : -1
          );
            commit("GET_HISTORY_MASTER_COA_SUCCESS", sorted); 
            resolve(sorted);
          })
          .catch((error) => {
            commit("GET_HISTORY_MASTER_COA_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },

    importCoa({ commit }, data) {
      commit("GET_INIT_IMPORT_COA");
      let formData = new FormData();
      formData.append("file", data.files);
      const url = `${ENDPOINT}import/`;
      return new Promise((resolve, reject) => {
        getAPI
          .post(url, formData , {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((res) => {
            store.dispatch('masterCoa/getMasterCoa')
            commit("GET_SUCCESS_IMPORT_COA");
            resolve(res);
          })
          .catch((error) => {
            const path = window.URL.createObjectURL(new Blob([error.response.data]));
            const link = document.createElement("a");
            link.href = path;
            link.setAttribute("download", "Error Upload Master Coa.xlsx");
            document.body.appendChild(link);
            link.click();
            reject(error);
            commit("GET_ERROR_IMPORT_COA", error);
          });
      });
    },

  },
  mutations: {
    // get related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetMasterCoa = true;
    },
    GET_SUCCESS(state, data) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterCoa = false;
      state.dataMasterCoa = data;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterCoa = false;
      state.dataMasterCoa = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get by ID related
    GET_INIT_MASTER_COA_BY_ID(state) {
      state.requestMasterCoaByIdStatus = "PENDING";
      state.loadingGetMasterCoaById = true;
    },
    GET_MASTER_COA_BY_ID_SUCCESS(state, data) {
      state.requestMasterCoaByIdStatus = "SUCCESS";
      state.loadingGetMasterCoaById = false;
      state.dataMasterCoaById = data;
    },
    GET_MASTER_COA_BY_ID_ERROR(state, error) {
      state.requestMasterCoaByIdStatus = "ERROR";
      state.loadingGetMasterCoaById = false;
      state.dataMasterCoaById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.requestpostPatchStatus = "PENDING";
      state.loadingPostPatchMasterCoa = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestpostPatchStatus = "SUCCESS";
      state.loadingPostPatchMasterCoa = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestpostPatchStatus = "ERROR";
      state.loadingPostPatchMasterCoa = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // Delete related
    DELETE_INIT(state) {
      state.requestDeleteStatus = "PENDING";
      state.loadingDeleteMasterCoa = true;
    },
    DELETE_SUCCESS(state) {
      state.requestDeleteStatus = "SUCCESS";
      state.loadingDeleteMasterCoa = false;
    },
    DELETE_ERROR(state, error) {
      state.requestDeleteStatus = "ERROR";
      state.loadingDeleteMasterCoa = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get History Master COA by ID related
    GET_INIT_HISTORY_MASTER_COA(state) {
      state.requestHistoryMasterCoaStatus = "PENDING";
      state.loadingGetHistoryMasterCoa= true;
    },
    GET_HISTORY_MASTER_COA_SUCCESS(state, data) {
      state.requestHistoryMasterCoaStatus = "SUCCESS";
      state.loadingGetHistoryMasterCoa = false;
      state.dataHistoryMasterCoa = data;
    },
    GET_HISTORY_MASTER_COA_ERROR(state, error) {
      state.requestHistoryMasterCoaStatus = "ERROR";
      state.loadingGetHistoryMasterCoa = false;
      state.dataHistoryMasterCoa = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // import related
    GET_INIT_IMPORT_COA(state) {
      state.requestImportCoaStatus = "PENDING";
      state.loadingImportCoa = true;
    },
    GET_SUCCESS_IMPORT_COA(state) {
      state.requestImportCoaStatus = "SUCCESS";
      state.loadingImportCoa = false;
    },
    GET_ERROR_IMPORT_COA(state, error) {
      state.requestImportCoaStatus = "ERROR";
      state.loadingImportCoa = false;
      state.errorMsgImportCoa = error;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default masterCoa;
