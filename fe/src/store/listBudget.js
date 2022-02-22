import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js";

const BUDGET_ENDPOINT = "/api/budget/";
const PLANNING_ENPOINT = "/api/planning/";
const UPLOAD_REALIZATION = "/api/import/";
const AUDITLOG_ENDPOINT = "/api/auditlog/"

const DOWNLOAD_BUDGET_FILE_NAME = "ListBudget.xlsx";
const DOWNLOAD_IMPORT_BUDGET_TEMPLATE_FILENAME = "TemplateBudgetPlanning.xlsx";

const listBudget = {
  namespaced: true,
  state: {
    // get List All Budget
    requestListAllBudgetStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListAllBudget: false, // for loading table
    dataListAllBudget: [], // for v-data-table
    // get List Active Budget
    requestListActiveBudgetStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListActiveBudget: false, // for loading table
    dataListActiveBudget: [], // for v-data-table
    // get List Inactive Budget
    requestListInactiveBudgetStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListInactiveBudget: false, // for loading table
    dataListInactiveBudget: [], // for v-data-table
    // get Budget by Id
    requestBudgetByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetBudgetById: false, // for loading table
    dataBudgetById: null, // for data item
    // save Budget by Id
    requestSaveBudgetByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingSaveBudgetById: false, // for loading
    // delete Budget by Id
    requestDeleteBudgetByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDeleteBudgetById: false, // for loading
    // cancel Budget by Id
    requestCancelBudgetByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingCancelBudgetById: false, // for loading
    // restore Budget by Id
    requestRestoreBudgetByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingRestoreBudgetById: false, // for loading
    // save Budget Planning
    requestSaveBudgetPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingSaveBudgetPlanning: false, // for loading
    // get List Active Planning
    requestListActivePlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListActivePlanning: false, // for loading table
    dataListActivePlanning: [], // for v-data-table
    // import Budget
    requestImportBudgetStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingImportBudget: false, // for loading
    // import Realization
    requestImportRealizationStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingImportRealization: false, // for loading
    // Download Budget
    requestDownloadBudgetStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDownloadBudget: false, // for loading
    // Download Import Budget Template
    requestDownloadImportBudgetTemplateStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDownloadImportBudgetTemplate: false, // for loading
    // get List Budget History By Id
    requestListBudgetHistoryByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListBudgetHistoryById: false, // for loading table
    dataListBudgetHistoryById: [], // for v-data-table


    // isLoading : false, //for loading when import planning
    // errorMessage : "", // standard
    // loadingGetListBudget: false, // for loading table
    // loadingGetListInactiveBudget: false, // for loading table
    // loadingGetEdittedItem: false, //
    // loadingPostPatchListBudget: false, // for loading post/patch
    // dataListBudget: [], // for v-data-table
    // dataListInactiveBudget: [], // for v-data-table
    // dataActiveListBudget: [], //for dropdown
    // requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    // requestInactiveStatus: "IDLE", //listplanning inactive
    // requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    // postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    // errorMsg: null,
    // edittedItem: null,
    // edittedItemHistories: [],
  },
  getters: {
    value: (state) => state.value,
  },
  actions: {
    getAllBudget({ commit }) {
      commit("GET_INIT_ALL_BUDGET");
      getAPI
        .get(BUDGET_ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_ALL_BUDGET", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_ALL_BUDGET", error.message);
        });
    },

    getListActiveBudget({ commit }) {
      commit("GET_INIT_ACTIVE_BUDGET");
      getAPI
        .get(BUDGET_ENDPOINT + "active/")
        .then((response) => {
          const cleanData = response.data;
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_ACTIVE_BUDGET", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_ACTIVE_BUDGET", error.message);
        });
    },

    getListInactiveBudget({ commit }) {
      commit("GET_INIT_INACTIVE_BUDGET");
      getAPI
        .get(BUDGET_ENDPOINT + "inactive/")
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_INACTIVE_BUDGET", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_INACTIVE_BUDGET", error.message);
        });
    },

    getBudgetById({ commit }, id) {
      commit("GET_INIT_BUDGET_BY_ID");
      return new Promise((resolve, reject) => {
        getAPI
          .get(BUDGET_ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("GET_SUCCESS_BUDGET_BY_ID", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR_BUDGET_BY_ID", error.message);
            reject(error.message);
          });
      });
    },

    saveBudgetById({ commit }, payload) {
      commit("PATCH_INIT_SAVE_BUDGET_BY_ID");
      const url = `${BUDGET_ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("PATCH_SUCCESS_SAVE_BUDGET_BY_ID");
            // store.dispatch("allBudget/getAllBudget");
          })
          .catch((error) => {
            commit("PATCH_ERROR_SAVE_BUDGET_BY_ID", error.message);
            reject(error.message);
          });
      });
    },

    deleteBudgetById({ commit }, id) {
      commit("DELETE_INIT_DELETE_BUDGET_BY_ID");
      return new Promise((resolve, reject) => {
        getAPI
          .delete(BUDGET_ENDPOINT + `${id}/`)
          .then((response) => {
            // const data = response.data;
            commit("DELETE_SUCCESS_DELETE_BUDGET_BY_ID");
            resolve(response);
            // store.dispatch("allBudget/getAllBudget");
          })
          .catch((error) => {
            commit("DELETE_ERROR_DELETE_BUDGET_BY_ID", error.message);
            reject(error.message);
          });
      });
    },

    cancelBudgetById({ commit }, id) {
      commit("POST_INIT_CANCEL_BUDGET_BY_ID");
      return new Promise((resolve, reject) => {
        getAPI
          .post(BUDGET_ENDPOINT + `${id}/` + "deactivate/")
          .then((response) => {
            // const data = response.data;
            commit("POST_SUCCESS_CANCEL_BUDGET_BY_ID");
            resolve(response);
            // store.dispatch("allBudget/getAllBudget");
          })
          .catch((error) => {
            commit("POST_ERROR_CANCEL_BUDGET_BY_ID", error.message);
            reject(error.message);
          });
      });
    },

    restoreBudgetById({ commit }, id) {
      commit("POST_INIT_RESTORE_BUDGET_BY_ID");
      return new Promise((resolve, reject) => {
        getAPI
          .post(BUDGET_ENDPOINT + `${id}/` + "restore/")
          .then((response) => {
            // const data = response.data;
            commit("POST_SUCCESS_RESTORE_BUDGET_BY_ID");
            resolve(response);
            // store.dispatch("allBudget/getAllBudget");
          })
          .catch((error) => {
            commit("POST_ERROR_RESTORE_BUDGET_BY_ID", error.message);
            reject(error.message);
          });
      });
    },

    saveBudgetPlanning({ commit }, payload) {
      commit("POST_INIT_SAVE_BUDGET_PLANNING");
      return new Promise((resolve, reject) => {
        getAPI
          .post(BUDGET_ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_SUCCESS_SAVE_BUDGET_PLANNING");
            // store.dispatch("listBudget/getListActiveBudget");
          })
          .catch((error) => {
            commit("POST_ERROR_SAVE_BUDGET_PLANNING", error.message);
            reject(error.message);
          });
      });
    },
    
    getListActivePlanning({ commit }) {
      commit("GET_INIT_ACTIVE_PLANNING");
      getAPI
        .get(PLANNING_ENPOINT + "active")
        .then((response) => {
          const cleanData = response.data;
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_ACTIVE_PLANNING", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_ACTIVE_PLANNING", error.message);
        });
    },

    importBudget({ commit }, data) {
      commit("POST_INIT_IMPORT_BUDGET");
      let formData = new FormData();
      formData.append("file", data.files);

      return new Promise((resolve, reject) => {
        getAPI
          .post(BUDGET_ENDPOINT + "import/", formData)
          .then((response) => {
            resolve(response);
            commit("POST_SUCCESS_IMPORT_BUDGET");
          })
          .catch((error) => {
            commit("POST_ERROR_IMPORT_BUDGET", error.message);
            reject(error.message);
          });
      });
    },

    importRealization({ commit }, data) {
      commit("POST_INIT_IMPORT_REALIZATION");
      let formData = new FormData();
      formData.append("file", data.files);

      return new Promise((resolve, reject) => {
        getAPI
          .post(UPLOAD_REALIZATION + "realisasi/", formData)
          .then((res) => {
            resolve(res);
            commit("POST_SUCCESS_IMPORT_REALIZATION");
          })
          .catch((error) => {
            commit("POST_ERROR_IMPORT_REALIZATION", error.message);
            reject(error.message);
          });
      });
    },

    downloadBudget({ commit }, data) {
      commit("GET_INIT_DOWNLOAD_BUDGET");

      return new Promise((resolve, reject) => {
        getAPI
          .get(BUDGET_ENDPOINT + "export/", {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((response) => {
            resolve(response);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", DOWNLOAD_BUDGET_FILE_NAME);
            document.body.appendChild(link);
            link.click();
            commit("GET_SUCCESS_DOWNLOAD_BUDGET");
          })
          .catch((error) => {
            commit("GET_ERROR_DOWNLOAD_BUDGET", error.message);
            reject(error.message);
          });
      });
    },

    downloadImportBudgetTemplate({ commit }) {
      commit("GET_INIT_DOWNLOAD_IMPORT_BUDGET_TEMPLATE");
      return new Promise((resolve, reject) => {
        getAPI
          .get(BUDGET_ENDPOINT + "import/template/", {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((response) => {
            resolve(response);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", DOWNLOAD_IMPORT_BUDGET_TEMPLATE_FILENAME);
            document.body.appendChild(link);
            link.click();
            commit("GET_SUCCESS_DOWNLOAD_IMPORT_BUDGET_TEMPLATE");
          })
          .catch((error) => {
            commit("GET_ERROR_DOWNLOAD_IMPORT_BUDGET_TEMPLATE", error.message);
            reject(error.message);
          });
      });
    },

    getListBudgetHistoryById({ commit }, id) {
      commit("GET_INIT_LIST_BUDGET_HISTORY_BY_ID"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get(AUDITLOG_ENDPOINT + "?table=budget&entity=" + `${id}`)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("GET_SUCCESS_LIST_BUDGET_HISTORY_BY_ID", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_LIST_BUDGET_HISTORY_BY_ID", error.message);
          reject(error.message);
        });
      });
    },
  },
  mutations: {
    // get List All Budget related
    GET_INIT_ALL_BUDGET(state) {
      state.requestListAllBudgetStatus = "PENDING";
      state.loadingGetListAllBudget = true;
    },
    GET_SUCCESS_ALL_BUDGET(state, dataListAllBudget) {
      state.requestListAllBudgetStatus = "SUCCESS";
      state.loadingGetListAllBudget = false;
      state.dataListAllBudget = dataListAllBudget;
    },
    GET_ERROR_ALL_BUDGET(state, error) {
      state.requestListAllBudgetStatus = "ERROR";
      state.loadingGetListAllBudget = false;
      state.dataListAllBudget = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get List Active Budget related
    GET_INIT_ACTIVE_BUDGET(state) {
      state.requestListActiveBudgetStatus = "PENDING";
      state.loadingGetListActiveBudget = true;
    },
    GET_SUCCESS_ACTIVE_BUDGET(state, dataListActiveBudget) {
      state.requestListActiveBudgetStatus = "SUCCESS";
      state.loadingGetListActiveBudget = false;
      state.dataListActiveBudget = dataListActiveBudget;
    },
    GET_ERROR_ACTIVE_BUDGET(state, error) {
      state.requestListActiveBudgetStatus = "ERROR";
      state.loadingGetListActiveBudget = false;
      state.dataListActiveBudget = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get List Inactive Budget related
    GET_INIT_INACTIVE_BUDGET(state) {
      state.requestListInactiveBudgetStatus = "PENDING";
      state.loadingGetListInactiveBudget = true;
    },
    GET_SUCCESS_INACTIVE_BUDGET(state, dataListInactiveBudget) {
      state.requestListInactiveBudgetStatus = "SUCCESS";
      state.loadingGetListInactiveBudget = false;
      state.dataListInactiveBudget = dataListInactiveBudget;
    },
    GET_ERROR_INACTIVE_BUDGET(state, error) {
      state.requestListInactiveBudgetStatus = "ERROR";
      state.loadingGetListInactiveBudget = false;
      state.dataListInactiveBudget = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get Budget By Id related
    GET_INIT_BUDGET_BY_ID(state) {
      state.requestBudgetByIdStatus = "PENDING";
      state.loadingGetBudgetById = true;
    },
    GET_SUCCESS_BUDGET_BY_ID(state, dataBudgetById) {
      state.requestBudgetByIdStatus = "SUCCESS";
      state.loadingGetBudgetById = false;
      state.dataBudgetById = dataBudgetById;
    },
    GET_ERROR_BUDGET_BY_ID(state, error) {
      state.requestBudgetByIdStatus = "ERROR";
      state.loadingGetBudgetById = false;
      state.dataBudgetById = null;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // save Budget By Id related
    PATCH_INIT_SAVE_BUDGET_BY_ID(state) {
      state.requestSaveBudgetByIdStatus = "PENDING";
      state.loadingSaveBudgetById = true;
    },
    PATCH_SUCCESS_SAVE_BUDGET_BY_ID(state) {
      state.requestSaveBudgetByIdStatus = "SUCCESS";
      state.loadingSaveBudgetById = false;
    },
    PATCH_ERROR_SAVE_BUDGET_BY_ID(state, error) {
      state.requestSaveBudgetByIdStatus = "ERROR";
      state.loadingSaveBudgetById = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    
    // delete Budget By Id related
    DELETE_INIT_DELETE_BUDGET_BY_ID(state) {
      state.requestDeleteBudgetByIdStatus = "PENDING";
      state.loadingDeleteBudgetById = true;
    },
    DELETE_SUCCESS_DELETE_BUDGET_BY_ID(state) {
      state.requestDeleteBudgetByIdStatus = "SUCCESS";
      state.loadingDeleteBudgetById = false;
    },
    DELETE_ERROR_DELETE_BUDGET_BY_ID(state, error) {
      state.requestDeleteBudgetByIdStatus = "ERROR";
      state.loadingDeleteBudgetById = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // cancel Budget By Id related
    POST_INIT_CANCEL_BUDGET_BY_ID(state) {
      state.requestCancelBudgetByIdStatus = "PENDING";
      state.loadingCancelBudgetById = true;
    },
    POST_SUCCESS_CANCEL_BUDGET_BY_ID(state) {
      state.requestCancelBudgetByIdStatus = "SUCCESS";
      state.loadingCancelBudgetById = false;
    },
    POST_ERROR_CANCEL_BUDGET_BY_ID(state, error) {
      state.requestCancelBudgetByIdStatus = "ERROR";
      state.loadingCancelBudgetById = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // restore Budget By Id related
    POST_INIT_RESTORE_BUDGET_BY_ID(state) {
      state.requestRestoreBudgetByIdStatus = "PENDING";
      state.loadingRestoreBudgetById = true;
    },
    POST_SUCCESS_RESTORE_BUDGET_BY_ID(state) {
      state.requestRestoreBudgetByIdStatus = "SUCCESS";
      state.loadingRestoreBudgetById = false;
    },
    POST_ERROR_RESTORE_BUDGET_BY_ID(state, error) {
      state.requestRestoreBudgetByIdStatus = "ERROR";
      state.loadingRestoreBudgetById = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // save Budget Planning related
    POST_INIT_SAVE_BUDGET_PLANNING(state) {
      state.requestSaveBudgetPlanningStatus = "PENDING";
      state.loadingSaveBudgetPlanning = true;
    },
    POST_SUCCESS_SAVE_BUDGET_PLANNING(state) {
      state.requestSaveBudgetPlanningStatus = "SUCCESS";
      state.loadingSaveBudgetPlanning = false;
    },
    POST_ERROR_SAVE_BUDGET_PLANNING(state, error) {
      state.requestSaveBudgetPlanningStatus = "ERROR";
      state.loadingSaveBudgetPlanning = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get List Active Planning related
    GET_INIT_ACTIVE_PLANNING(state) {
      state.requestListActivePlanningStatus = "PENDING";
      state.loadingGetListActivePlanning = true;
    },
    GET_SUCCESS_ACTIVE_PLANNING(state, dataListActivePlanning) {
      state.requestListActivePlanningStatus = "SUCCESS";
      state.loadingGetListActivePlanning = false;
      state.dataListActivePlanning = dataListActivePlanning;
    },
    GET_ERROR_ACTIVE_PLANNING(state, error) {
      state.requestListActivePlanningStatus = "ERROR";
      state.loadingGetListActivePlanning = false;
      state.dataListActivePlanning = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // import Budget related
    POST_INIT_IMPORT_BUDGET(state) {
      state.requestImportBudgetStatus = "PENDING";
      state.loadingImportBudget = true;
    },
    POST_SUCCESS_IMPORT_BUDGET(state) {
      state.requestImportBudgetStatus = "SUCCESS";
      state.loadingImportBudget = false;
    },
    POST_ERROR_IMPORT_BUDGET(state, error) {
      state.requestImportBudgetStatus = "ERROR";
      state.loadingImportBudget = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // import Realization related
    POST_INIT_IMPORT_REALIZATION(state) {
      state.requestImportRealizationStatus = "PENDING";
      state.loadingImportRealization = true;
    },
    POST_SUCCESS_IMPORT_REALIZATION(state) {
      state.requestImportRealizationStatus = "SUCCESS";
      state.loadingImportRealization = false;
    },
    POST_ERROR_IMPORT_REALIZATION(state, error) {
      state.requestImportRealizationStatus = "ERROR";
      state.loadingImportRealization = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // download Budget related
    GET_INIT_DOWNLOAD_BUDGET(state) {
      state.requestDownloadBudgetStatus = "PENDING";
      state.loadingDownloadBudget = true;
    },
    GET_SUCCESS_DOWNLOAD_BUDGET(state) {
      state.requestDownloadBudgetStatus = "SUCCESS";
      state.loadingDownloadBudget = false;
    },
    GET_ERROR_DOWNLOAD_BUDGET(state, error) {
      state.requestDownloadBudgetStatus = "ERROR";
      state.loadingDownloadBudget = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // download Import Budget Template related
    GET_INIT_DOWNLOAD_IMPORT_BUDGET_TEMPLATE(state) {
      state.requestDownloadImportBudgetTemplateStatus = "PENDING";
      state.loadingDownloadImportBudgetTemplate = true;
    },
    GET_SUCCESS_DOWNLOAD_IMPORT_BUDGET_TEMPLATE(state) {
      state.requestDownloadImportBudgetTemplateStatus = "SUCCESS";
      state.loadingDownloadImportBudgetTemplate = false;
    },
    GET_ERROR_DOWNLOAD_IMPORT_BUDGET_TEMPLATE(state, error) {
      state.requestDownloadImportBudgetTemplateStatus = "ERROR";
      state.loadingDownloadImportBudgetTemplate = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get List Budget History By Id related
    GET_INIT_LIST_BUDGET_HISTORY_BY_ID(state) {
      state.requestListBudgetHistoryByIdStatus = "PENDING";
      state.loadingGetListBudgetHistoryById = true;
    },
    GET_SUCCESS_LIST_BUDGET_HISTORY_BY_ID(state, dataListBudgetHistoryById) {
      state.requestListBudgetHistoryByIdStatus = "SUCCESS";
      state.loadingGetListBudgetHistoryById = false;
      state.dataListBudgetHistoryById = dataListBudgetHistoryById;
    },
    GET_ERROR_LIST_BUDGET_HISTORY_BY_ID(state, error) {
      state.requestListActiveBudgetStatus = "ERROR";
      state.loadingGetListActiveBudget = false;
      state.dataListBudgetHistoryById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default listBudget;
