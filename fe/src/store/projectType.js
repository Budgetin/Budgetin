import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const ENDPOINT = "/api/project_type/";

const projectType = {
  namespaced: true,
  state: {
    loadingGetListPlanning: false, // for loading table
    dataProjectType: [], 
    dataProjectTypeExisting: [], 
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    requestStatusExisting: "IDLE",
    errorMsg: null,
  },
  getters: {
    
  },
  actions: {
    getAllProjectType({ commit }) {
      commit("GET_INIT");
      return new Promise((resolve, reject) => {
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          commit("GET_SUCCESS", cleanData);
          resolve(response);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
          reject(errorMsg);
        });
      });
    },
  },

  mutations: {
    // get related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetListPlanning = true;
    },
    GET_SUCCESS(state, dataProjectType) {
      state.requestStatus = "SUCCESS";
      state.loadingGetListPlanning = false;
      state.dataProjectType = dataProjectType;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetListPlanning = false;
      state.errorMsg = error;
      state.dataProjectType = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    GET_EXISTING_INIT(state) {
      state.requestStatusExisting = "PENDING";
      state.loadingGetListPlanning = true;
    },
    GET_EXISTING_SUCCESS(state, dataProjectTypeExisting) {
      state.requestStatusExisting = "SUCCESS";
      state.loadingGetListPlanning = false;
      state.dataProjectTypeExisting = dataProjectTypeExisting;
    },
    GET_EXISTING_ERROR(state, error) {
      state.requestStatusExisting = "ERROR";
      state.loadingGetListPlanning = false;
      state.errorMsg = error;
      state.dataProjectTypeExisting = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default projectType;
