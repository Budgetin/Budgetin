import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const ENDPOINT = "api/budget/";

const allBudget = {
  namespaced: true,
  state: {
    loadingGetAllBudget: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchAllBudget: false, // for loading post/patch
    dataAllBudget: [], // for v-data-table
    dataActiveAllBudget: [], //for dropdown
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
    edittedItem: null,
    loadingDeleteItem:false,
    deleteStatus: "IDLE",
    deleteItem: [],
    loadingRestoreItem:false,
    restoreStatus: "IDLE",
    restoreItem: [],
    edittedItemHistories: [],
    requestHistoriesStatus:"IDLE",
    loadingGetEdittedItemHistories: false,
  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    getAllBudget() {
      if (store.state.allBudget.requestStatus !== "SUCCESS")
        store.dispatch("allBudget/getFromAPI");
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
    getAllBudgetById({ commit }, id) {
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
    postAllBudget({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("allBudget/getFromAPI");
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
    patchAllBudget({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("allBudget/getFromAPI");
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
    deleteAllBudgetById({ commit }, id) {
      commit("SET_LOADING_DELETE_ITEM", true);
      return new Promise((resolve, reject) => {
        getAPI
          .delete(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("SET_DELETE_ITEM", data);
            resolve(data);
            store.dispatch("allBudget/getFromAPI");
          })
          .catch((error) => {
            commit("DELETE_ERROR", error);
            reject(error);
          });
      });
    },
    restoreAllBudgetById({ commit }, id) {
      commit("SET_LOADING_RESTORE_ITEM", true);
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT + `${id}/` + "restore/")
          .then((response) => {
            const data = response.data;
            commit("SET_RESTORE_ITEM", data);
            resolve(data);
            store.dispatch("allBudget/getFromAPI");
          })
          .catch((error) => {
            commit("RESTORE_ERROR", error);
            reject(error);
          });
      });
    },
    getHistory({ commit }, id) {
      commit("SET_REQUEST_STATUS"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=budget&entity=" + `${id}`)
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
      state.loadingGetAllBudget = true;
    },
    GET_SUCCESS(state, dataAllBudget) {
      state.requestStatus = "SUCCESS";
      state.loadingGetAllBudget = false;
      state.dataAllBudget = dataAllBudget;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveAllBudget) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveAllBudget = dataActiveAllBudget;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetAllBudget = false;
      state.errorMsg = error;
      state.dataAllBudget = [];
      state.dataActiveAllBudget = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchAllBudget = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchAllBudget = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchAllBudget = false;
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

    // delete item
    SET_DELETE_ITEM(state, payload) {
      state.deleteItem = payload;
    },
    SET_LOADING_DELETE_ITEM(state, payload) {
      state.loadingDeleteItem = payload;
    },
    DELETE_ERROR(state, error) {
      state.deleteStatus = "ERROR";
      state.loadingDeleteItem = false;
      state.errorMsg = error;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // restore item
    SET_RESTORE_ITEM(state, payload) {
      state.restoreItem = payload;
    },
    SET_LOADING_RESTORE_ITEM(state, payload) {
      state.loadingRestoreItem = payload;
    },
    RESTORE_ERROR(state, error) {
      state.restoreStatus = "ERROR";
      state.loadingRestoreItem = false;
      state.errorMsg = error;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default allBudget
