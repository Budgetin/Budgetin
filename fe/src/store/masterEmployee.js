import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/user/imo/";

const masterImo = {
  namespaced: true,
  state: {
    loadingGetMasterImo: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchMasterImo: false, // for loading post/patch
    dataMasterImo: [], // for v-data-table
    dataActiveMasterImo: [], //for dropdown
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
    getMasterImo() {
      if (store.state.masterImo.requestStatus !== "SUCCESS")
        store.dispatch("masterImo/getFromAPI");
    },
    getFromAPI({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
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
      state.loadingGetMasterImo = true;
    },
    GET_SUCCESS(state, dataMasterImo) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterImo = false;
      state.dataMasterImo = dataMasterImo;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveMasterImo) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveMasterImo = dataActiveMasterImo;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterImo = false;
      state.errorMsg = error;
      state.dataMasterImo = [];
      state.dataActiveMasterImo = [];
    },
  },
};

export default masterImo;
