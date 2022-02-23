import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js";

const ENDPOINT = "/api/dashboard/group_budget/";

const masterCoa = {
  namespaced: true,
  state: {
    // get data planning and realization in every group
    requestBudgetRealizationEveryGroupStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetBudgetRealizationEveryGroup: false, // for loading table
    dataGroup: [], // for data column chart
    dataBudgetEveryGroup: [], // for data column chart
  },
  getters: {},
  actions: {
    getBudgetRealizationEveryGroup({ commit }) {
      commit("GET_INIT_BUDGET_REALIZATION_EVERY_GROUP");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT)
          .then((response) => {
            let dataGroup = [];
            let dataBudget = [];
            response.data.map((data, index) => {
              dataGroup[index] = data.Group,
              dataBudget[index] = data.Budget
            });
            commit("GET_BUDGET_REALIZATION_EVERY_GROUP_SUCCESS",{dataGroup,dataBudget});
            resolve({ dataGroup,dataBudget});
          })
          .catch((error) => {
            commit("GET_BUDGET_REALIZATION_EVERY_GROUP_ERROR", error);
            reject(error);
          });
      });
    },
  },
  mutations: {
    // get budget and realization in every group related
    GET_INIT_BUDGET_REALIZATION_EVERY_GROUP(state) {
      state.requestBudgetRealizationEveryGroupStatus = "PENDING";
      state.loadingGetBudgetRealizationEveryGroup = true;
    },
    GET_BUDGET_REALIZATION_EVERY_GROUP_SUCCESS(state, {dataGroup, dataBudget}) {
      state.requestBudgetRealizationEveryGroupStatus = "SUCCESS";
      state.loadingGetBudgetRealizationEveryGroup = false;
      state.dataGroup = dataGroup;
      state.dataBudgetEveryGroup = dataBudget;
    },
    GET_BUDGET_REALIZATION_EVERY_GROUP_ERROR(state, error) {
      state.requestBudgetRealizationEveryGroupStatus = "ERROR";
      state.loadingGetBudgetRealizationEveryGroup = false;
      state.dataGroup = [];
      state.dataBudgetEveryGroup = [];
      console.log(error);
      // if(error.response.status =="401"){
      //   router.push({ name: 'Login'});
      // }
    },
  },
};

export default masterCoa;
