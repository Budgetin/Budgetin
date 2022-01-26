import store from ".";
import { getAPI } from "@/plugins/axios-api.js";

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
  },
  getters: {
    value: (state) => state.value
  },
  actions: {
    getMasterUser() {
      if (store.state.masterUser.requestStatus !== "SUCCESS")
        store.dispatch("masterUser/getFromAPI");
    },
    getFromAPI({ commit }) {
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
            store.dispatch("masterUser/getFromAPI");
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
            store.dispatch("masterUser/getFromAPI");
            // store.dispatch("masterCategory/getFromAPI");
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
    //   const itemID = store.state.masterUser.edittedItem.id;
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
    // getActiveMasterUser({ commit }) {
    //   if (store.state.masterUser.requestActiveStatus !== "SUCCESS")
    //     getAPI
    //       .get(ENDPOINT + "?filter{status}=1")
    //       .then((response) => {
    //         const cleanData = response.data.Users.map((data) => {
    //           return {
    //             id: data.id,
    //             User_name: data.User_name,
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

export default masterUser;
