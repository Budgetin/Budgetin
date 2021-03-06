import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

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
    loadingDeleteItem:false,
    deleteStatus: "IDLE",
    deleteItem: [],
    requestHistoriesStatus:"IDLE",
    loadingGetEdittedItemHistories: false,
    edittedItemHistories: [],
  },
  getters: {
  },
  actions: {
    getMasterCoa({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data.map((data) => {
            return {
              created_at: data.created_at,
              created_by: data.created_by,
              definition: data.definition,
              deleted_at: data.deleted_at,
              hyperion_name: data.hyperion_name,
              id: data.id,
              is_capex: data.is_capex,
              is_deleted: data.is_deleted,
              minimum_item_origin: data.minimum_item_origin,
              name: data.name,
              updated_at: data.update_at,
              updated_by: data.updated_by,
            };
          });
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
            store.dispatch("masterCoa/getMasterCoa");
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
            store.dispatch("masterCoa/getMasterCoa");
            // store.dispatch("masterCategory/getFromAPI");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(errorMsg);
          });
      });
    },

    deleteMasterCoa({ commit }, id) {
      commit("SET_LOADING_DELETE_ITEM", true);
      return new Promise((resolve, reject) => {
        getAPI
          .delete(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            commit("SET_DELETE_ITEM", data);
            resolve(data);
            store.dispatch("masterCoa/getMasterCoa");
          })
          .catch((error) => {
            commit("DELETE_ERROR", error);
            reject(error);
          });
      });
    },

      //harus return promise
    getHistory({ commit }, id) {
      commit("SET_REQUEST_STATUS"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=coa&entity=" + `${id}`)
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
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
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
  },
};

export default masterCoa;
