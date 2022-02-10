import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const ENDPOINT = "/api/monitoring/";

const monitorPlanning = {
  namespaced: true,
  state: {
    loadingGetMonitorPlanning: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchMonitorPlanning: false, // for loading post/patch
    dataMonitorPlanning: [], // for v-data-table
    dataActiveMonitorPlanning: [], //for dropdown
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
    getMonitorPlanning() {
      if (store.state.monitorPlanning.requestStatus !== "SUCCESS")
        store.dispatch("monitorPlanning/getFromAPI");
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
    getMonitorPlanningById({ commit }, id) {
      // commit("SET_EDITTED_ITEM_HISTORIES", []);
      commit("SET_LOADING_GET_EDITTED_ITEM", true);

      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + "?planning=" + `${id}`)
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
    getMonitorPlanningDetailById({ commit }, id) {
      // commit("SET_EDITTED_ITEM_HISTORIES", []);
      commit("SET_LOADING_GET_EDITTED_ITEM", true);

      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}`)
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
    postMonitorPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("monitorPlanning/getFromAPI");
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
    patchMonitorPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      console.log("Payload ID: "+payload.id);
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("monitorPlanning/getFromAPI");
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
        .get("/api/auditlog?table=monitoring&entity=" + `${id}`)
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
      state.loadingGetMonitorPlanning = true;
    },
    GET_SUCCESS(state, dataMonitorPlanning) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMonitorPlanning = false;
      state.dataMonitorPlanning = dataMonitorPlanning;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveMonitorPlanning) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveMonitorPlanning = dataActiveMonitorPlanning;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMonitorPlanning = false;
      state.errorMsg = error;
      state.dataMonitorPlanning = [];
      state.dataActiveMonitorPlanning = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchMonitorPlanning = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchMonitorPlanning = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchMonitorPlanning = false;
      state.errorMsg = error;
      if(error.response.status =="401"){
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

export default monitorPlanning
