import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

const ENDPOINT = "/api/planning/";

const startPlanning = {
  namespaced: true,
  state: {
    loadingGetStartPlanning: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchStartPlanning: false, // for loading post/patch
    dataStartPlanning: [], // for v-data-table
    dataActiveStartPlanning: [], //for dropdown
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
    getStartPlanning() {
      if (store.state.startPlanning.requestStatus !== "SUCCESS")
        store.dispatch("startPlanning/getFromAPI");
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
    getStartPlanningById({ commit }, id) {
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
    postStartPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("startPlanning/getFromAPI");
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
    patchStartPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("startPlanning/getFromAPI");
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
    //   const itemID = store.state.startPlanning.edittedItem.id;
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
    // getActivestartPlanning({ commit }) {
    //   if (store.state.startPlanning.requestActiveStatus !== "SUCCESS")
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
      state.loadingGetStartPlanning = true;
    },
    GET_SUCCESS(state, dataStartPlanning) {
      state.requestStatus = "SUCCESS";
      state.loadingGetStartPlanning = false;
      state.dataStartPlanning = dataStartPlanning;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveStartPlanning) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveStartPlanning = dataActiveStartPlanning;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetStartPlanning = false;
      state.errorMsg = error;
      state.dataStartPlanning = [];
      state.dataActiveStartPlanning = [];
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchStartPlanning = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchStartPlanning = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchStartPlanning = false;
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

export default startPlanning;
