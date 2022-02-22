import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/mytask/";
const BUDGET_ENDPOINT = "/api/budget/";

const home = {
  namespaced: true,
  state: {
    // get Task
    requestTaskStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetTask: false, // for loading table
    dataHome: [], // for v-data-table
    
    // get task by id
    requestTaskByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetTaskById: false, // for loading table
    dataTaskById: null, // for store data
    
    // get List My Planning based on task id
    requestSubmittedTaskItemStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetSubmittedTaskItem: false, // for loading table
    dataSubmittedTask: [], // for v-data-table
    
    // set monitoring status as Submitted
    requestSubmitPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostSubmitPlanning: false, // for loading table
    
    // save planning
    requestSavePlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostSavePlanning: false, // for loading table
    
    // download My Planning
    requestDownloadPlanningStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingDownloadPlanning: false, // for loading data

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
            commit("GET_TASK_BY_ID_SUCCESS", cleanData);
            resolve(cleanData);
          })
          .catch((error) => {
            commit("GET_TASK_BY_ID_ERROR", error);
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
    
    submitPlanning({ commit }, payload) {
      commit("POST_INIT_PLANNING");
      return new Promise((resolve, reject) => {
        getAPI
          .post(BUDGET_ENDPOINT,payload)
          .then((response) => {
            commit("POST_SUCCESS_PLANNING");
            resolve(response);
          })
          .catch((error) => {
            commit("POST_ERROR_PLANNING", error);
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
    GET_SUCCESS(state, data) {
      state.requestTaskStatus = "SUCCESS";
      state.loadingGetTask = false;
      state.dataHome = data;
    },
    GET_ERROR(state, error) {
      state.requestTaskStatus = "ERROR";
      state.loadingGetTask = false;
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
    GET_TASK_BY_ID_SUCCESS(state, dataTask) {
      state.requestTaskByIdStatus = "SUCCESS";
      state.loadingGetTaskById = false;
      state.dataTaskById = dataTask;
    },
    GET_TASK_BY_ID_ERROR(state, error) {
      state.requestTaskByIdStatus = "ERROR";
      state.loadingGetTaskById = false;
      state.dataTaskById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    
    // get Submitted based Task related
    GET_INIT_SUBMITTED_TASK_ITEM(state) {
      state.requestSubmittedTaskItemStatus = "PENDING";
      state.loadingGetSubmittedTaskItem = true;
    },
    GET_SUCCESS_SUBMITTED_TASK_ITEM(state, data) {
      state.requestSubmittedTaskItemStatus = "SUCCESS";
      state.loadingGetSubmittedTaskItem = false;
      state.dataSubmittedTask = data;
    },
    GET_ERROR_SUBMITTED_TASK_ITEM(state, error) {
      state.requestSubmittedTaskItemStatus = "ERROR";
      state.loadingGetSubmittedTaskItem = false;
      state.dataSubmittedTask = [];
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
    POST_ERROR_SUBMIT_PLANNING(state, error) {
      state.requestSubmitPlanningStatus = "ERROR";
      state.loadingPostSubmitPlanning = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    //Post Planning related
    POST_INIT_PLANNING(state) {
      state.requestSavePlanningStatus = "PENDING";
      state.loadingPostSavePlanning = true;
    },
    POST_SUCCESS_PLANNING(state) {
      state.requestSavePlanningStatus = "SUCCESS";
      state.loadingPostSavePlanning = false;
    },
    POST_ERROR_PLANNING(state, error) {
      state.requestSavePlanningStatus = "ERROR";
      state.loadingPostSavePlanning = false;
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
      state.dataHome = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default home;
