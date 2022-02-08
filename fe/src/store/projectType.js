import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/project_type/";

const projectType = {
  namespaced: true,
  state: {
    loadingGetListPlanning: false, // for loading table
    dataProjectType: [], 
    
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
  },
  getters: {
    valueNew: (state) => {let value = state.dataProjectType.find((x)=> x.name="New")
      return value;
    },
    valueCarryForward: (state) => {let value = state.dataProjectType.find((x)=> x.name="Carry Forward")
      return value;
    },
    valueReguler: (state) => {let value = state.dataProjectType.find((x)=> x.name="Regular")
      return value;
    }
  },
  actions: {
    getAllProjectType() {
      if (store.state.projectType.requestStatus !== "SUCCESS")
        store.dispatch("projectType/getFromAPI");
    },
    getFromAPI({ commit }) {
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
    },
  },
};

export default projectType;
