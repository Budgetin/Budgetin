import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const ENDPOINT = "/api/user/imo/";

const masterEmployee = {
  namespaced: true,
  state: {
    // get data employee
    requestEmployeeStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetEmployee: false, // for loading table
    dataEmployee: [], // for dropdown
  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    getEmployee({ commit }) {
      commit("GET_INIT_EMPLOYEE");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT)
          .then((response) => {
            const cleanData = response.data
            const sorted = cleanData.sort((a, b) =>
              a.name > b.name ? 1 : -1
            );
            commit("GET_EMPLOYEE_SUCCESS", sorted);
            resolve(response)
          })
          .catch((error) => {
            commit("GET_EMPLOYEE_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },
  },
  mutations: {
    // Get List of Employee related
    GET_INIT_EMPLOYEE(state) {
      state.requestEmployeeStatus = "PENDING";
      state.loadingGetEmployee = true;
    },
    GET_EMPLOYEE_SUCCESS(state, data) {
      state.requestEmployeeStatus = "SUCCESS";
      state.loadingGetEmployee = false;
      state.dataEmployee = data;
    },
    GET_EMPLOYEE_ERROR(state, error) {
      state.requestEmployeeStatus = "ERROR";
      state.loadingGetEmployee = false;
      state.dataEmployee = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default masterEmployee;
