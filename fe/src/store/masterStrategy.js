import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/strategy/";

const masterStrategy = {
  namespaced: true,
  state: {
    loadingGetMasterStrategy: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchMasterStrategy: false, // for loading post/patch
    dataMasterStrategy: [], // for v-data-table
    dataActiveMasterStrategy: [], //for dropdown
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
    getMasterStrategy() {
      if (store.state.masterStrategy.requestStatus !== "SUCCESS")
        store.dispatch("masterStrategy/getFromAPI");
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
    getMasterStrategyById({ commit }, id) {
      // commit("SET_EDITTED_ITEM_HISTORIES", []);
      commit("SET_LOADING_GET_EDITTED_ITEM", true);

      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("SET_EDITTED_ITEM", data);
            resolve(data);
          })
          .catch((error) => {
            commit("GET_ERROR", error);
            reject(error);
          });
      });
    },
    postMasterStrategy({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterStrategy/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Strategy_name")) {
                    errorMsg += error.response.data.Strategy_name;
                  }
                  break;

                default:
                  errorMsg += `Please recheck your input or try again later`;
                  break;
              }
            }
            commit("POST_PATCH_ERROR", errorMsg);
            reject(errorMsg);
          });
      });
    },
    patchMasterStrategy({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterStrategy/getFromAPI");
            // store.dispatch("masterCategory/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Strategy_name")) {
                    errorMsg += error.response.data.Strategy_name;
                  }
                  break;

                default:
                  errorMsg += `${error.response.statusText}: Please recheck your input or try again later`;
                  break;
              }
            }
            reject(errorMsg);
            commit("POST_PATCH_ERROR", error.response.data);
          });
      });
    },
    // getEdittedItemHistories({ commit }) {
    //   const itemID = store.state.masterStrategy.edittedItem.id;
    //   if (!itemID) return;
    //   getAPI
    //     .get(ENDPOINT + `${itemID}/histories/`)
    //     .then((response) => {
    //       commit("SET_LOADING_GET_EDITTED_ITEM", false);
    //       commit("SET_EDITTED_ITEM_HISTORIES", response.data);
    //     })
    //     .catch((error) => {
    //       commit("GET_ERROR", error.response.data);
    //     });
    // },
  },
  mutations: {
    // get related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetMasterStrategy = true;
    },
    GET_SUCCESS(state, dataMasterStrategy) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterStrategy = false;
      state.dataMasterStrategy = dataMasterStrategy;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveMasterStrategy) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveMasterStrategy = dataActiveMasterStrategy;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterStrategy = false;
      state.errorMsg = error;
      state.dataMasterStrategy = [];
      state.dataActiveMasterStrategy = [];
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchMasterStrategy = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchMasterStrategy = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchMasterStrategy = false;
      state.errorMsg = error;
    },
    SET_EDITTED_ITEM(state, payload) {
      state.edittedItem = payload;
    },
    SET_LOADING_GET_EDITTED_ITEM(state, payload) {
      state.loadingGetEdittedItem = payload;
    },

    // history related
    SET_EDITTED_ITEM_HISTORIES(state, payload) {
      state.edittedItemHistories = payload;
    },

    SET_REQUEST_STATUS(state, payload) {
      state.requestStatus = payload;
    },

    ON_CHANGE(state, payload) {
      state.value = payload;
    },
    ON_CHANGE_PAGING(state, payload) {
      state.current = payload;
    },
  },
};

export default masterStrategy;
