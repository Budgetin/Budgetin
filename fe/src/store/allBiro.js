import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/biro/";

const allBiro = {
  namespaced: true,
  state: {
    loadingGetAllBiro: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchAllBiro: false, // for loading post/patch
    dataAllBiro: [], // for v-data-table
    dataActiveAllBiro: [], //for dropdown
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
    getAllBiro() {
      if (store.state.allBiro.requestStatus !== "SUCCESS")
        store.dispatch("allBiro/getFromAPI");
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
    getAllBiroById({ commit }, id) {
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
    postAllBiro({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("allBiro/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("year")) {
                    errorMsg += error.response.data.year;
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
    patchAllBiro({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("allBiro/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("year")) {
                    errorMsg += error.response.data.year;
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
    //   const itemID = store.state.allBiro.edittedItem.id;
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
    // getActiveallBiro({ commit }) {
    //   if (store.state.allBiro.requestActiveStatus !== "SUCCESS")
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
      state.loadingGetAllBiro = true;
    },
    GET_SUCCESS(state, dataAllBiro) {
      state.requestStatus = "SUCCESS";
      state.loadingGetAllBiro = false;
      state.dataAllBiro = dataAllBiro;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveAllBiro) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveAllBiro = dataActiveAllBiro;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetAllBiro = false;
      state.errorMsg = error;
      state.dataAllBiro = [];
      state.dataActiveAllBiro = [];
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchAllBiro = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchAllBiro = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchAllBiro = false;
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

export default allBiro
