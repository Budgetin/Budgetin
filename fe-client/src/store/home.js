import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/mytask/";

const home = {
  namespaced: true,
  state: {
    requestTaskStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetTask: false, // for loading table
    dataHome: [], // for v-data-table
    errorMsg: null,

    requestTaskByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetTaskById: false, // for loading table
    dataTaskById: [], // for v-data-table
    errorMsgTaskById: null,

    requestSubmittedTaskStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetSubmittedTask: false, // for loading table
    dataSubmittedTask: [], // for v-data-table
    errorMsgSubmittedTask: null,

    loadingGetEdittedItem: false,
    loadingPostPatchHome: false, // for loading post/patch
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    edittedItem: null,
    loadingDeleteItem:false,
    deleteStatus: "IDLE",
    deleteItem: [],
    requestHistoriesStatus:"IDLE",
    loadingGetEdittedItemHistories: false,
    edittedItemHistories: [],
  },
  getters: {
    value: (state) => state.dataHome
  },
  actions: {
    getHome({ commit }) {
      commit("GET_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT)
          .then((response) => {
            const cleanData = response.data
            const sorted = cleanData.sort((a, b) =>
              a.updated_at > b.updated_at ? 1 : -1
            );
            commit("GET_SUCCESS", sorted);
            resolve(sorted);
          })
          .catch((error) => {
            commit("GET_ERROR", error);
            reject(error);
          });
      });
    },
    getTaskById({ commit }, id) {
      commit("GET_INIT_BY_ID");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const cleanData = response.data
            const sorted = cleanData.sort((a, b) =>
              a.updated_at > b.updated_at ? 1 : -1
            );
            commit("GET_TASK_BY_ID_SUCCESS", sorted);
            resolve(sorted);
          })
          .catch((error) => {
            commit("GET_TASK_BY_ID_SUCCESS", error);
            reject(error);
          });
      });
    },
    getSubmittedTaskById({ commit }, id) {
      commit("SET_LOADING_GET_SUBMITTED_TASK_ITEM");
      return new Promise((resolve, reject) => {
        getAPI
          .get(ENDPOINT + `${id}/`)
          .then((response) => {
            const cleanData = response.data
            const sorted = cleanData.sort((a, b) =>
              a.updated_at > b.updated_at ? 1 : -1
            );
            commit("SET_SUBMITTED_TASK_ITEM", sorted);
            resolve(sorted);
          })
          .catch((error) => {
            commit("SET_ERROR_SUBMITTED_TASK_ITEM", error);
            reject(error);
          });
      });
    },
    // postHome({ commit }, payload) {
    //   commit("POST_PATCH_INIT");
    //   return new Promise((resolve, reject) => {
    //     getAPI
    //       .post(ENDPOINT, payload)
    //       .then((response) => {
    //         resolve(response);
    //         commit("POST_PATCH_SUCCESS");
    //         store.dispatch("home/getFromAPI");
    //       })
    //       .catch((error) => {
    //         let errorMsg =
    //           "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
    //         if (error.response) {
    //           errorMsg = "";
    //           switch (error.response.status) {
    //             case 400:
    //               if (error.response.data.hasOwnProperty("Coa_name")) {
    //                 errorMsg += error.response.data.Coa_name;
    //               }
    //               break;

    //             default:
    //               errorMsg += `Please recheck your input or try again later`;
    //               break;
    //           }
    //         }
    //         commit("POST_PATCH_ERROR", errorMsg);
    //         reject(errorMsg);
    //       });
    //   });
    // },
    // patchHome({ commit }, payload) {
    //   commit("POST_PATCH_INIT");
    //   const url = `${ENDPOINT}${payload.id}/`;
    //   return new Promise((resolve, reject) => {
    //     getAPI
    //       .patch(url, payload)
    //       .then((response) => {
    //         resolve(response);
    //         commit("POST_PATCH_SUCCESS");
    //         store.dispatch("home/getFromAPI");
    //         // store.dispatch("masterCategory/getFromAPI");
    //       })
    //       .catch((error) => {
    //         let errorMsg =
    //           "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
    //         if (error.response) {
    //           errorMsg = "";
    //           switch (error.response.status) {
    //             case 400:
    //               if (error.response.data.hasOwnProperty("Coa_name")) {
    //                 errorMsg += error.response.data.Coa_name;
    //               }
    //               break;

    //             default:
    //               errorMsg += `${error.response.statusText}: Please recheck your input or try again later`;
    //               break;
    //           }
    //         }
    //         reject(errorMsg);
    //         commit("POST_PATCH_ERROR", error.response.data);
    //       });
    //   });
    // },

    // deleteHomeById({ commit }, id) {
    //   commit("SET_LOADING_DELETE_ITEM", true);
    //   return new Promise((resolve, reject) => {
    //     getAPI
    //       .delete(ENDPOINT + `${id}/`)
    //       .then((response) => {
    //         const data = response.data;
    //         commit("SET_DELETE_ITEM", data);
    //         resolve(data);
    //         store.dispatch("home/getFromAPI");
    //       })
    //       .catch((error) => {
    //         commit("DELETE_ERROR", error);
    //         reject(error);
    //       });
    //   });
    // },

    //   //harus return promise
    // getHistory({ commit }, id) {
    //   commit("SET_REQUEST_STATUS"); 
    //   return new Promise((resolve, reject) => {
    //   getAPI
    //     .get("/api/auditlog?table=coa&entity=" + `${id}`)
    //     .then((response) => {
    //       const data = response.data;
    //       const sorted = data.sort((a, b) =>
    //       a.id < b.id ? 1 : -1
    //     );
    //       commit("SET_EDITTED_ITEM_HISTORIES", sorted); 
    //       resolve(sorted);
    //     })
    //     .catch((error) => {
    //       commit("GET_ERROR", error);
    //       reject(error);
    //     });
    //   });
    // },

  },
  mutations: {
    // get Task related
    GET_INIT(state) {
      state.requestTaskStatus = "PENDING";
      state.loadingGetTask = true;
    },
    GET_SUCCESS(state, dataHome) {
      state.requestTaskStatus = "SUCCESS";
      state.loadingGetTask = false;
      state.dataHome = dataHome;
    },
    GET_ERROR(state, error) {
      state.requestTaskStatus = "ERROR";
      state.loadingGetTask = false;
      state.errorMsg = error;
      state.dataHome = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get Task by ID related
    GET_INIT_BY_ID(state) {
      state.requestTaskByIdStatus = "PENDING";
      state.loadingGetTaskById = true;
    },
    GET_TASK_BY_ID_SUCCESS(state, dataTask) {
      state.requestTaskByIdStatus = "SUCCESS";
      state.loadingGetTaskById = false;
      state.dataTaskById = dataTask;
    },
    GET_TASK_BY_ID_ERROR(state, error) {
      state.requestTaskByIdStatus = "ERROR";
      state.loadingGetTaskById = false;
      state.errorMsgTaskById = error;
      state.dataTaskById = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    
    // get Submitted based Task related
    SET_LOADING_GET_SUBMITTED_TASK_ITEM(state) {
      state.requestSubmittedTaskStatus = "PENDING";
      state.loadingGetSubmittedTaskItem = true;
    },
    SET_SUBMITTED_TASK_ITEM(state, payload) {
      state.requestSubmittedTaskStatus = "SUCCESS";
      state.loadingGetSubmittedTaskItem = false;
      state.dataSubmittedTask = payload;
    },
    SET_ERROR_SUBMITTED_TASK_ITEM(state, error) {
      state.requestTaskStatus = "ERROR";
      state.loadingGetSubmittedTaskItem = false;
      state.errorMsgSubmittedTask = error;
      state.dataSubmittedTask = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },



    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchHome = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestStatus = "SUCCESS";
      state.loadingPostPatchHome = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingPostPatchHome = false;
      state.errorMsg = error;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
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

export default home;
