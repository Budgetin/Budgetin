import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const PROJECT_TYPE_ENDPOINT = "/api/project_type/";

const projectType = {
  namespaced: true,
  state: {
    // get List All Project Type
    requestListAllProjectTypeStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetListAllProjectType: false, // for loading table
    dataListAllProjectType: [], // for v-data-table
  },
  getters: {
    value: (state) => state.value,
  },
  actions: {
    getAllProjectType({ commit }) {
      commit("GET_INIT_ALL_PROJECT_TYPE");
      return new Promise((resolve, reject) => {
      getAPI
        .get(PROJECT_TYPE_ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          commit("GET_SUCCESS_ALL_PROJECT_TYPE", cleanData);
          resolve(response);
        })
        .catch((error) => {
          commit("GET_ERROR_ALL_PROJECT_TYPE", error.message);
          reject(error.message);
        });
      });
    },
  },

  mutations: {
    // get List All Project Type related
    GET_INIT_ALL_PROJECT_TYPE(state) {
      state.requestListAllProjectTypeStatus = "PENDING";
      state.loadingGetListAllProjectType = true;
    },
    GET_SUCCESS_ALL_PROJECT_TYPE(state, dataListAllProjectType) {
      state.requestListAllProjectTypeStatus = "SUCCESS";
      state.loadingGetListAllProjectType = false;
      state.dataListAllProjectType = dataListAllProjectType;
    },
    GET_ERROR_ALL_PROJECT_TYPE(state, error) {
      state.requestListAllProjectTypeStatus = "ERROR";
      state.loadingGetListAllProjectType = false;
      state.dataProjectType = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default projectType;
