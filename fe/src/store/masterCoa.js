import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/coa/";

const masterCoa = {
  namespaced: true,
  state: {
    loadingGetMasterCoa: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchMasterCoa: false, // for loading post/patch
    dataMasterCoa: [], // for v-data-table
    dataActiveMasterCoa: [], //for dropdown
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
    getMasterCoa() {
      if (store.state.masterCoa.requestStatus !== "SUCCESS")
        store.dispatch("masterCoa/getFromAPI");
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
    getMasterCoaById({ commit }, id) {
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
    postMasterCoa({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterCoa/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Coa_name")) {
                    errorMsg += error.response.data.Coa_name;
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
    patchMasterCoa({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterCoa/getFromAPI");
            // store.dispatch("masterCategory/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Coa_name")) {
                    errorMsg += error.response.data.Coa_name;
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
    //   const itemID = store.state.masterCoa.edittedItem.id;
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
    // getActiveMasterCoa({ commit }) {
    //   if (store.state.masterCoa.requestActiveStatus !== "SUCCESS")
    //     getAPI
    //       .get(ENDPOINT + "?filter{status}=1")
    //       .then((response) => {
    //         const cleanData = response.data.Coas.map((data) => {
    //           return {
    //             id: data.id,
    //             Coa_name: data.Coa_name,
    //             status: String(data.status),
    //           };
    //         });
    //         commit("GET_ACTIVE_DATA_UPDATE", cleanData);
    //       })
    //       .catch((error) => {
    //         commit("GET_ERROR", error);
    //       });
    // },
  },
  mutations: {
    // get related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetMasterCoa = true;
    },
    GET_SUCCESS(state, dataMasterCoa) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterCoa = false;
      state.dataMasterCoa = dataMasterCoa;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveMasterCoa) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveMasterCoa = dataActiveMasterCoa;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterCoa = false;
      state.errorMsg = error;
      state.dataMasterCoa = [];
      state.dataActiveMasterCoa = [];
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchMasterCoa = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchMasterCoa = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchMasterCoa = false;
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

export default masterCoa;
