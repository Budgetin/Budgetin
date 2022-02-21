import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/product/";

const masterProduct = {
  namespaced: true,
  state: {
    loadingGetMasterProduct: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchMasterProduct: false, // for loading post/patch
    dataMasterProduct: [], // for v-data-table
    dataActiveMasterProduct: [], //for dropdown
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
    edittedItem: null,
    edittedItemHistories: [],
    loadingDeleteItem:false,
    deleteStatus: "IDLE",
    deleteItem: [],
    requestHistoriesStatus:"IDLE",
    loadingGetEdittedItemHistories: false,
    edittedItemHistories: [],
    requestImportProductStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingImportProduct: false, // for loading data
    errorMsgImportProduct: null,
    loadingImportProductTemplate: false, // for loading download template
    loadingStatus: "IDLE",
  },
  getters: {
    value: (state) => state.value
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
      // commit("SET_EDITTED_ITEM_HISTORIES", []);
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
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Product_name")) {
                    errorMsg += error.response.data.Product_name;
                  }
                  break;

                default:
                  errorMsg += `Please recheck your input or try again later`;
                  break;
              }
            }
            commit("POST_PATCH_ERROR", errorMsg);
            reject(errorMsg);
          });
      });
    },
    patchMasterProduct({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterProduct/getMasterProduct");
            // store.dispatch("masterCategory/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Product_name")) {
                    errorMsg += error.response.data.Product_name;
                  }
                  break;

                default:
                  errorMsg += `${error.response.statusText}: Please recheck your input or try again later`;
                  break;
              }
            }
            reject(errorMsg);
            commit("POST_PATCH_ERROR", error.response.data);
          });
      });
    },
    deleteMasterProductById({ commit }, id) {
      // commit("SET_EDITTED_ITEM_HISTORIES", []);
      commit("SET_LOADING_DELETE_ITEM", true);
      return new Promise((resolve, reject) => {
        getAPI
          .delete(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("SET_DELETE_ITEM", data);
            resolve(data);
            store.dispatch("masterProduct/getMasterProduct");
          })
          .catch((error) => {
            commit("DELETE_ERROR", error);
            reject(error);
          });
      });
    },

    getHistory({ commit }, id) {
      commit("SET_REQUEST_STATUS"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=product&entity=" + `${id}`)
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

    importProductTemplate({ commit }) {
      commit("SET_LOADING_INIT");

      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + "import/template", {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((response) => {
            resolve(response);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", "import_product_template.xlsx");
            document.body.appendChild(link);
            link.click();
            // commit("SET_LOADING_SUCCESS");
          })
          .catch((err) => {
            reject(err);
            commit("SET_LOADING_ERROR", err);
            commit("SET_DOWNLOAD_ERROR", err.message);
          });
      });
    },

    importProduct({ commit }, data) {
      commit("GET_INIT_IMPORT_PRODUCT");
      let formData = new FormData();
      formData.append("file", data.files);

      return new Promise((resolve, reject) => {
        getAPI
          .post((ENDPOINT+"import/"), formData)
          .then((res) => {
            resolve(res);
            store.dispatch('masterProduct/getMasterProduct')
            commit("GET_SUCCESS_IMPORT_PRODUCT");
          })
          .catch((err) => {
            reject(err);
            commit("GET_ERROR_IMPORT_PRODUCT", err.message);
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
    GET_SUCCESS(state, dataMasterProduct) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterProduct = false;
      state.dataMasterProduct = dataMasterProduct;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveMasterProduct) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveMasterProduct = dataActiveMasterProduct;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterProduct = false;
      state.errorMsg = error;
      state.dataMasterProduct = [];
      state.dataActiveMasterProduct = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchMasterProduct = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchMasterProduct = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchMasterProduct = false;
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

    SET_LOADING_INIT(state) {
      state.loadingStatus = "PENDING";
      state.loadingImportProductTemplate = true;
      // state.isLoading = data;
    },
    SET_LOADING_SUCCESS(state) {
      state.loadingStatus = "SUCCESS";
      state.loadingImportProductTemplate = false;
    },
    SET_LOADING_ERROR(state, error) {
      state.loadingStatus = "ERROR";
      state.loadingImportProductTemplate = false;
      state.errorMsg = error;
      console.log(error);
      if (error.response.status == "401"){
        router.push({ name: 'Login'});
      }
    },
    SET_UPLOAD_ERROR(state, error) {
      state.errorMessage = error;
      if (error.response.status == "401") {
        router.push({ name: "Login" });
      }
    },
    SET_DOWNLOAD_ERROR(state, error) {
      state.errorMessage = error;
      if (error.response.status == "401") {
        router.push({ name: "Login" });
      }
    },
  },
};

export default masterProduct;
