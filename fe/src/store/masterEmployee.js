import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/user/imo/";

const masterEmployee = {
  namespaced: true,
  state: {
    loadingGetMasterEmployee: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchMasterEmployee: false, // for loading post/patch
    dataMasterEmployee: [], // for v-data-table
    dataActiveMasterEmployee: [], //for dropdown
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
    edittedItem: null,
    edittedItemHistories: [],
  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    getMasterEmployee() {
      if (store.state.masterEmployee.requestStatus !== "SUCCESS")
        store.dispatch("masterEmployee/getFromAPI");
    },
    getFromAPI({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data.map((data) => {
            return {
              id: data.id,
              name: data.name,
              username: data.username,
              option: String(data.name+" - "+data.username),
            };
          });
          const sorted = cleanData.sort((a, b) =>
            a.name > b.name ? 1 : -1
          );

          commit("GET_SUCCESS", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
        });
    },
  },
  mutations: {
    // get related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetMasterEmployee = true;
    },
    GET_SUCCESS(state, dataMasterEmployee) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterEmployee = false;
      state.dataMasterEmployee = dataMasterEmployee;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveMasterEmployee) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveMasterEmployee = dataActiveMasterEmployee;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterEmployee = false;
      state.errorMsg = error;
      state.dataMasterEmployee = [];
      state.dataActiveMasterEmployee = [];
    },
  },
};

export default masterEmployee;
