import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/coa/";

const masterCoa = {
  namespaced: true,
  state: {
    // get All data Master Coa
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterCoa: false, // for loading table
    dataMasterCoa: [], // for v-data-table
    errorMsg: null,

    // get All data Master Coa by ID


    loadingGetEdittedItem: false,
    loadingPostPatchMasterCoa: false, // for loading post/patch
    dataActiveMasterCoa: [], //for dropdown
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    edittedItem: null,
    loadingDeleteItem:false,
    deleteStatus: "IDLE",
    deleteItem: [],
    requestHistoriesStatus:"IDLE",
    loadingGetEdittedItemHistories: false,
    edittedItemHistories: [],

    requestImportCoaStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingImportCoa: false, // for loading data
    errorMsgImportCoa: null,

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
      commit("SET_LOADING_GET_EDITTED_ITEM", true);

      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("SET_EDITTED_ITEM", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR", error);
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
          .patch(url, payload)
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

    deleteMasterCoaById({ commit }, id) {
      commit("SET_LOADING_DELETE_ITEM", true);
      return new Promise((resolve, reject) => {
        getAPI
          .delete(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("SET_DELETE_ITEM", data);
            resolve(data);
            // store.dispatch("masterStatus/getFromAPI");
            store.dispatch("masterCoa/getMasterCoa");
          })
          .catch((error) => {
            commit("DELETE_ERROR", error);
            reject(error);
          });
      });
    },

      //harus return promise
    getHistory({ commit }, id) {
      commit("SET_REQUEST_STATUS"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=coa&entity=" + `${id}`)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("SET_EDITTED_ITEM_HISTORIES", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
          reject(error);
        });
      });
    },

    importCoa({ commit }, data) {
      console.log(data)
      commit("GET_INIT_IMPORT_COA");
      let formData = new FormData();
      formData.append("file", data.files);

      return new Promise((resolve, reject) => {
        getAPI
          .post((ENDPOINT+"import/"), formData , {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((res) => {
            resolve(res);
            store.dispatch('masterCoa/getMasterCoa')
            commit("GET_SUCCESS_IMPORT_COA");
          })
          .catch((err) => {
            const url = window.URL.createObjectURL(new Blob([err.response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", "Error Upload Master Coa.xlsx");
            document.body.appendChild(link);
            link.click();
            reject(err);
            commit("GET_ERROR_IMPORT_COA", err);
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
    GET_SUCCESS(state, dataMasterCoa) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterCoa = false;
      state.dataMasterCoa = dataMasterCoa;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterCoa = false;
      state.errorMsg = error;
      state.dataMasterCoa = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },



    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchMasterCoa = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchMasterCoa = false;
    },
    POST_PATCH_ERROR(state, error) {
      console.log(error.response);
      state.requestStatus = "ERROR";
      state.loadingPostPatchMasterCoa = false;
      state.errorMsg = error;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    SET_EDITTED_ITEM(state, payload) {
      state.edittedItem = payload;
    },
    SET_LOADING_GET_EDITTED_ITEM(state, payload) {
      state.loadingGetEdittedItem = payload;
    },

    // history relate
    SET_EDITTED_ITEM_HISTORIES(state, edittedItemHistories) {
      state.requestHistoriesStatus = "SUCCESS";
      state.loadingGetEdittedItemHistories = false;
      state.edittedItemHistories = edittedItemHistories;
    },
    SET_REQUEST_STATUS(state) {
      state.requestHistoriesStatus = "PENDING";
      state.loadingGetEdittedItemHistories = true;
      state.edittedItemHistories = [];
    },

    ON_CHANGE(state, payload) {
      state.value = payload;
    },
    ON_CHANGE_PAGING(state, payload) {
      state.current = payload;
    },

    // delete item
    SET_DELETE_ITEM(state, payload) {
      state.deleteItem = payload;
    },
    SET_LOADING_DELETE_ITEM(state, payload) {
      state.loadingDeleteItem = payload;
    },
    DELETE_ERROR(state, error) {
      state.deleteStatus = "ERROR";
      state.loadingDeleteItem = false;
      state.errorMsg = error;
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
      console.log(error.response);
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
