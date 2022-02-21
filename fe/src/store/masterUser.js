import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/user/";

const masterUser = {
  namespaced: true,
  state: {
    loadingGetMasterUser: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchMasterUser: false, // for loading post/patch
    dataMasterUser: [], // for v-data-table
    dataActiveMasterUser: [], //for dropdown
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
    edittedItem: null,
    edittedItemHistories: [],
    requestHistoriesStatus:"IDLE",
    loadingGetEdittedItemHistories: false,
    edittedItemHistories: [],
  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    getMasterUser({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data.map((data) => {
              return {
                id: data.id,
                name: {
                  id: data.employee_id,
                  display_name: data.display_name,
                  username: data.username,
                  option: String(data.display_name+" - "+data.username),                  
                },
                role: data.role,
                status: {
                  id: data.is_active,
                  label: data.is_active?"Active":"Inactive"
                },
                updated_by: data.updated_by,
                updated_at: data.updated_at
            }
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
    getEmployee({ commit }) {
      commit("GET_DROPDOWN");
      getAPI
        .get(ENDPOINT+'imo/')
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.display_name > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
        });
    },
    getMasterUserById({ commit }, id) {
      // commit("SET_EDITTED_ITEM_HISTORIES", []);
      commit("SET_LOADING_GET_EDITTED_ITEM", true);

      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const data = response.data;
            let getData = {
                id: data.id,
                name: {
                  id: data.employee_id,
                  display_name: data.display_name,
                  username: data.username,
                  option: String(data.display_name+" - "+data.username),                  
                },
                role: data.role,
                status: {
                  id: data.is_active,
                  label: data.is_active?"Active":"Inactive"
                }
            }
            commit("SET_EDITTED_ITEM", getData);
            resolve(getData);
          })
          .catch((error) => {
            commit("GET_ERROR", error);
            reject(error);
          });
      });
    },
    postMasterUser({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterUser/getMasterUser");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("User_name")) {
                    errorMsg += error.response.data.User_name;
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
    patchMasterUser({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterUser/getMasterUser");
            // store.dispatch("masterCategory/getFromAPI");
          })
          .catch((error) => {
            reject(error);
            commit("POST_PATCH_ERROR", error);
          });
      });
    },
    getHistory({ commit }, id) {
      commit("SET_REQUEST_STATUS"); 
      return new Promise((resolve, reject) => {
      getAPI
        .get("/api/auditlog?table=user&entity=" + `${id}`)
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
      state.loadingGetMasterUser = true;
    },
    GET_SUCCESS(state, dataMasterUser) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterUser = false;
      state.dataMasterUser = dataMasterUser;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveMasterUser) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveMasterUser = dataActiveMasterUser;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterUser = false;
      state.errorMsg = error;
      state.dataMasterUser = [];
      state.dataActiveMasterUser = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchMasterUser = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchMasterUser = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchMasterUser = false;
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

export default masterUser;
