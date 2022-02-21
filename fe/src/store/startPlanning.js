import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
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
    requestHistoriesStatus:"IDLE",
    loadingGetEdittedItemHistories: false,
  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    getStartPlanning({ commit }) {
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
            // let errorMsg =
            //   "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            // if (error.response) {
            //   errorMsg = "";
            //   switch (error.response.status) {
            //     case 400:
            //       if (error.response.data.hasOwnProperty("year")) {
            //         errorMsg += error.response.data.year;
            //       }
            //       break;

            //     default:
            //       errorMsg += `Please recheck your input or try again later`;
            //       break;
            //   }
            // }
            commit("POST_PATCH_ERROR", error);
            reject(error.response.data.year);
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
    getHistory({ commit }, id) {
      commit("SET_REQUEST_STATUS"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=planning&entity=" + `${id}`)
        .then((response) => {
          const data = response.data;
          const sorted = data.sort((a, b) =>
          a.id < b.id ? 1 : -1
        );
          commit("SET_EDITTED_ITEM_HISTORIES", sorted); 
          resolve(sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
          reject(error);
        });
      });
    },
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
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchStartPlanning = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.postPatchStatus = "SUCCESS";
      state.loadingPostPatchStartPlanning = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.postPatchStatus = "ERROR";
      state.loadingPostPatchStartPlanning = false;
      state.errorMsg = error;
      console.log(error);
      if (error.response.status == "401"){
        router.push({ name: 'Login'});
      }
    },
    SET_EDITTED_ITEM(state, payload) {
      state.edittedItem = payload;
    },
    SET_LOADING_GET_EDITTED_ITEM(state, payload) {
      state.loadingGetEdittedItem = payload;
    },

    // history relate
    SET_EDITTED_ITEM_HISTORIES(state, edittedItemHistories) {
      state.requestHistoriesStatus = "SUCCESS";
      state.loadingGetEdittedItemHistories = false;
      state.edittedItemHistories = edittedItemHistories;
    },
    SET_REQUEST_STATUS(state) {
      state.requestHistoriesStatus = "PENDING";
      state.loadingGetEdittedItemHistories = true;
      state.edittedItemHistories = [];
    },

    ON_CHANGE(state, payload) {
      state.value = payload;
    },
    ON_CHANGE_PAGING(state, payload) {
      state.current = payload;
    },
  },
};

export default startPlanning
