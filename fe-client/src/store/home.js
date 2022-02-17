import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/mytask/";

const home = {
  namespaced: true,
  state: {
    requestTaskStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetTask: false, // for loading table
    dataHome: [], // for v-data-table
    errorMsg: null,

    requestTaskByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetTaskById: false, // for loading table
    dataTaskById: null, // for store data
    errorMsgTaskById: null,

    requestSubmitPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostSubmitPlanning: false, // for loading table
    errorMsgSubmitPlanning: null,

    requestSubmittedTaskStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetSubmittedTask: false, // for loading table
    dataSubmittedTask: [], // for v-data-table
    errorMsgSubmittedTask: null,

    requestDownloadPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDownloadPlanning: false, // for loading data
    errorMsgDownloadPlanning: null,

    loadingGetEdittedItem: false,
    loadingPostPatchHome: false, // for loading post/patch
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    edittedItem: null,
    loadingDeleteItem:false,
    deleteStatus: "IDLE",
    deleteItem: [],
    requestHistoriesStatus:"IDLE",
    loadingGetEdittedItemHistories: false,
    edittedItemHistories: [],
  },
  getters: {
    value: (state) => state.dataHome
  },
  actions: {

    getHome({ commit }) {
      commit("GET_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT)
          .then((response) => {
            const cleanData = response.data
            const sorted = cleanData.sort((a, b) =>
              a.updated_at > b.updated_at ? 1 : -1
            );
            commit("GET_SUCCESS", sorted);
            resolve(sorted);
          })
          .catch((error) => {
            commit("GET_ERROR", error);
            reject(error.message);
          });
      });
    },

    getTaskById({ commit }, id) {
      commit("GET_INIT_TASK_BY_ID");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const cleanData = response.data
            commit("GET_SUCCESS_TASK_BY_ID", cleanData);
            resolve(cleanData);
          })
          .catch((error) => {
            commit("GET_ERROR_TASK_BY_ID", error);
            reject(error.message);
          });
      });
    },

    getSubmittedTaskById({ commit }, id) {
      commit("GET_INIT_SUBMITTED_TASK_ITEM");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT+"submitted_budget/" + `${id}/`)
          .then((response) => {
            let cleanData = response.data
            if(cleanData.length > 1){
              let sorted = cleanData.sort((a, b) =>
              a.updated_at > b.updated_at ? 1 : -1
              );
              cleanData = sorted;
            }
            commit("GET_SUCCESS_SUBMITTED_TASK_ITEM", cleanData);
            resolve(cleanData);
          })
          .catch((error) => {
            commit("GET_ERROR_SUBMITTED_TASK_ITEM", error);
            reject(error.message);
          });
      });
    },

    submitPlanning({ commit }, data) {
      commit("POST_INIT_SUBMIT_PLANNING");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT+`${data.id}/`+"submit/")
          .then((response) => {
            commit("POST_SUCCESS_SUBMIT_PLANNING");
            resolve(response);
          })
          .catch((error) => {
            commit("GET_ERROR_SUBMIT_PLANNING", error);
            console.log(error.message);
            reject(error.message);
          });
      });
    },

    downloadPlanning({ commit }, data) {
      commit("GET_INIT_DOWNLOAD_PLANNING");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT+"submitted_budget/"+ `${data.id}/`+"download/", {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((response) => {
            resolve(response);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", "MyPlanning.xlsx");
            document.body.appendChild(link);
            link.click();
            commit("GET_SUCCESS_DOWNLOAD_PLANNING");
          })
          .catch((err) => {
            reject(err.message);
            commit("GET_ERROR_DOWNLOAD_PLANNING", err);
          });
      });
    },

  },
  mutations: {
    // get Task related
    GET_INIT(state) {
      state.requestTaskStatus = "PENDING";
      state.loadingGetTask = true;
    },
    GET_SUCCESS(state, dataHome) {
      state.requestTaskStatus = "SUCCESS";
      state.loadingGetTask = false;
      state.dataHome = dataHome;
    },
    GET_ERROR(state, error) {
      state.requestTaskStatus = "ERROR";
      state.loadingGetTask = false;
      state.errorMsg = error;
      state.dataHome = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get Task by ID related
    GET_INIT_TASK_BY_ID(state) {
      state.requestTaskByIdStatus = "PENDING";
      state.loadingGetTaskById = true;
    },
    GET_SUCCESS_TASK_BY_ID(state, dataTask) {
      state.requestTaskByIdStatus = "SUCCESS";
      state.loadingGetTaskById = false;
      state.dataTaskById = dataTask;
    },
    GET_ERROR_TASK_BY_ID(state, error) {
      state.requestTaskByIdStatus = "ERROR";
      state.loadingGetTaskById = false;
      state.errorMsgTaskById = error;
      state.dataTaskById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    
    // get Submitted based Task related
    GET_INIT_SUBMITTED_TASK_ITEM(state) {
      state.requestSubmittedTaskStatus = "PENDING";
      state.loadingGetSubmittedTaskItem = true;
    },
    GET_SUCCESS_SUBMITTED_TASK_ITEM(state, payload) {
      state.requestSubmittedTaskStatus = "SUCCESS";
      state.loadingGetSubmittedTaskItem = false;
      state.dataSubmittedTask = payload;
    },
    GET_ERROR_SUBMITTED_TASK_ITEM(state, error) {
      state.requestTaskStatus = "ERROR";
      state.loadingGetSubmittedTaskItem = false;
      state.errorMsgSubmittedTask = error;
      state.dataSubmittedTask = [];
      console.log(error)
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    //Post Status Submit related
    POST_INIT_SUBMIT_PLANNING(state) {
      state.requestSubmitPlanningStatus = "PENDING";
      state.loadingPostSubmitPlanning = true;
    },
    POST_SUCCESS_SUBMIT_PLANNING(state) {
      state.requestSubmitPlanningStatus = "SUCCESS";
      state.loadingPostSubmitPlanning = false;
    },
    GET_ERROR_SUBMIT_PLANNING(state, error) {
      state.requestSubmitPlanningStatus = "ERROR";
      state.loadingPostSubmitPlanning = false;
      state.errorMsgSubmitPlanning = error;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // Download Planning by Task 
    GET_INIT_DOWNLOAD_PLANNING(state) {
      state.requestDownloadPlanningStatus = "PENDING";
      state.loadingGetDownloadPlanning = true;
    },
    GET_SUCCESS_DOWNLOAD_PLANNING(state) {
      state.requestDownloadPlanningStatus = "SUCCESS";
      state.loadingGetDownloadPlanning = false;
    },
    GET_ERROR_DOWNLOAD_PLANNING(state, error) {
      state.requestDownloadPlanningStatus = "ERROR";
      state.loadingGetDownloadPlanning = false;
      state.errorMsg = error;
      state.dataHome = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },


    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchHome = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchHome = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchHome = false;
      state.errorMsg = error;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
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
  },
};

export default home;
