import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/product/";
const LOGENDPOINT="/api/auditlog?table=product&entity=";

const masterProduct = {
  namespaced: true,
  state: {
    // get All data Master Product
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterProduct: false, // for loading table
    dataMasterProduct: [], // for v-data-table

    // get All data Master Product by ID    
    requestMasterProductByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterProductById: false, // for loading table
    dataMasterProductById: [], // for v-data-table
    
    // Post/Patch Master PRODUCT   
    requestpostPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDeleteMasterProduct: false, // for loading table

    // Delete data Master Product by ID    
    requestDeleteStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterProductById: false, // for loading table

    // get History data Master Product by ID    
    requestHistoryMasterProductStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetHistoryMasterProduct: false, // for loading table

    // import Master Product / Add Product by upload file
    requestImportProductStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingImportProduct: false, // for loading data

  },
  getters: {
    // value: (state) => state.value
  },
  actions: {
    getMasterProduct({ commit }) {
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
    
    getMasterProductById({ commit }, id) {
      commit("GET_INIT_MASTER_PRODUCT_BY_ID");
      const url = `${ENDPOINT}${id}/`
      return new Promise((resolve, reject) => {
        getAPI
          .get(url)
          .then((response) => {
            const data = response.data;
            commit("GET_MASTER_PRODUCT_BY_ID_SUCCESS", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_MASTER_PRODUCT_BY_ID_ERROR", error);
            reject(error);
          });
      });
    },

    postMasterProduct({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterProduct/getMasterProduct");
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

    patchMasterProduct({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url,payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterProduct/getMasterProduct");
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

    deleteMasterProduct({ commit },id) {
      commit("DELETE_INIT");
      const url = `${ENDPOINT}${id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .delete(url)
          .then((response) => {
            store.dispatch("masterProduct/getMasterProduct");
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
      commit("GET_INIT_HISTORY_MASTER_PRODUCT"); 
      const url = `${LOGENDPOINT}${id}`;
      return new Promise((resolve, reject) => {
        getAPI
          .get(url)
          .then((response) => {
            const data = response.data;
            const sorted = data.sort((a, b) =>
            a.id < b.id ? 1 : -1
          );
            commit("GET_HISTORY_MASTER_PRODUCT_SUCCESS", sorted); 
            resolve(sorted);
          })
          .catch((error) => {
            commit("GET_HISTORY_MASTER_PRODUCT_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },

    importTemplateProduct({ commit }) {
      commit("GET_INIT_IMPORT_PRODUCT");
      const url = `${ENDPOINT}import/template/`;
      return new Promise((resolve, reject) => {
        getAPI
          .get(url, {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((response) => {
            const path = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = path;
            link.setAttribute("download", "Template Upload Master Product.xlsx");
            document.body.appendChild(link);
            link.click();
            store.dispatch('masterProduct/getMasterProduct')
            commit("GET_SUCCESS_IMPORT_PRODUCT");
            resolve(response);
          })
          .catch((error) => {
            commit("GET_ERROR_IMPORT_PRODUCT", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },

    importProduct({ commit }, data) {
      commit("GET_INIT_IMPORT_PRODUCT");
      let formData = new FormData();
      formData.append("file", data.files);
      const url = `${ENDPOINT}import/`;
      return new Promise((resolve, reject) => {
        getAPI
          .post(url, formData , {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((response) => {
            store.dispatch('masterProduct/getMasterProduct')
            commit("GET_SUCCESS_IMPORT_PRODUCT");
            resolve(response);
          })
          .catch((error) => {
            const path = window.URL.createObjectURL(new Blob([error.response.data]));
            const link = document.createElement("a");
            link.href = path;
            link.setAttribute("download", "Error Upload Master Product.xlsx");
            document.body.appendChild(link);
            link.click();
            commit("GET_ERROR_IMPORT_PRODUCT", error);
            reject(error);
          });
      });
    },

  },
  mutations: {
    // get related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetMasterProduct = true;
    },
    GET_SUCCESS(state, data) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterProduct = false;
      state.dataMasterProduct = data;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterProduct = false;
      state.dataMasterProduct = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get by ID related
    GET_INIT_MASTER_PRODUCT_BY_ID(state) {
      state.requestMasterProductByIdStatus = "PENDING";
      state.loadingGetMasterProductById = true;
    },
    GET_MASTER_PRODUCT_BY_ID_SUCCESS(state, data) {
      state.requestMasterProductByIdStatus = "SUCCESS";
      state.loadingGetMasterProductById = false;
      state.dataMasterProductById = data;
    },
    GET_MASTER_PRODUCT_BY_ID_ERROR(state, error) {
      state.requestMasterProductByIdStatus = "ERROR";
      state.loadingGetMasterProductById = false;
      state.dataMasterProductById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.requestpostPatchStatus = "PENDING";
      state.loadingPostPatchMasterProduct = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestpostPatchStatus = "SUCCESS";
      state.loadingPostPatchMasterProduct = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestpostPatchStatus = "ERROR";
      state.loadingPostPatchMasterProduct = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // Delete related
    DELETE_INIT(state) {
      state.requestDeleteStatus = "PENDING";
      state.loadingDeleteMasterProduct = true;
    },
    DELETE_SUCCESS(state) {
      state.requestDeleteStatus = "SUCCESS";
      state.loadingDeleteMasterProduct = false;
    },
    DELETE_ERROR(state, error) {
      state.requestDeleteStatus = "ERROR";
      state.loadingDeleteMasterProduct = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get History Master PRODUCT by ID related
    GET_INIT_HISTORY_MASTER_PRODUCT(state) {
      state.requestHistoryMasterProductStatus = "PENDING";
      state.loadingGetHistoryMasterProduct= true;
    },
    GET_HISTORY_MASTER_PRODUCT_SUCCESS(state, data) {
      state.requestHistoryMasterProductStatus = "SUCCESS";
      state.loadingGetHistoryMasterProduct = false;
      state.dataHistoryMasterProduct = data;
    },
    GET_HISTORY_MASTER_PRODUCT_ERROR(state, error) {
      state.requestHistoryMasterProductStatus = "ERROR";
      state.loadingGetHistoryMasterProduct = false;
      state.dataHistoryMasterProduct = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // import related
    GET_INIT_IMPORT_PRODUCT(state) {
      state.requestImportProductStatus = "PENDING";
      state.loadingImportProduct = true;
    },
    GET_SUCCESS_IMPORT_PRODUCT(state) {
      state.requestImportProductStatus = "SUCCESS";
      state.loadingImportProduct = false;
    },
    GET_ERROR_IMPORT_PRODUCT(state, error) {
      state.requestImportProductStatus = "ERROR";
      state.loadingImportProduct = false;
      state.errorMsgImportProduct = error;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default masterProduct;
