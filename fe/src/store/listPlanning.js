import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"
const LIST_PLANNING_ENDPOINT = "/api/budget/list_planning/";
const BUDGET_ENDPOINT = "/api/budget/";
const PLANNING_ENPOINT = "/api/planning/"
const UPLOAD_PLANNING = "/api/import/list_planning/"
const UPLOAD_REALIZATION = "/api/import/realisasi/"

const listPlanning = {
  namespaced: true,
  state: {
    isLoading : false, //for loading when import planning
    errorMessage : "",
    loadingGetListPlanning: false, // for loading table
    loadingGetListInactivePlanning: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchListPlanning: false, // for loading post/patch
    dataListPlanning: [], // for v-data-table
    dataListInactivePlanning: [], // for v-data-table
    dataActiveListPlanning: [], //for dropdown
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    requestInactiveStatus: "IDLE", //listplanning inactive
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
    
//==Page ListPlanning.vue

    //Get List Budget Planning (Active)
    getListPlanning() {
      if (store.state.listPlanning.requestStatus !== "SUCCESS")
        store.dispatch("listPlanning/getFromAPI");
    },
    getFromAPI({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(BUDGET_ENDPOINT + "active/")
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

    getListInactivePlanning() {
      if (store.state.listPlanning.requestInactiveStatus !== "SUCCESS")
        store.dispatch("listPlanning/getFromInactiveAPI");
    },
    getFromInactiveAPI({ commit }) {
      commit("GET_INACTIVE_INIT");
      getAPI
        .get(BUDGET_ENDPOINT + "inactive/")
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_INACTIVE_SUCCESS", sorted);
        })
        .catch((error) => {
          commit("GET_INACTIVE_ERROR", error);
        });
    },

    getListActivePlanning() {
      if (store.state.listPlanning.requestActiveStatus !== "SUCCESS")
        store.dispatch("listPlanning/getFromActiveAPI");
    },
    getFromActiveAPI({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(PLANNING_ENPOINT + "active")
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_ACTIVE_DATA_UPDATE", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
        });
    },
    
    getListPlanningById({ commit }, id) {
      // commit("SET_EDITTED_ITEM_HISTORIES", []);
      commit("SET_LOADING_GET_EDITTED_ITEM", true);

      return new Promise((resolve, reject) => {
        getAPI
          .get(BUDGET_ENDPOINT + `${id}/`)
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

    postListPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(BUDGET_ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("listPlanning/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Planning_name")) {
                    errorMsg += error.response.data.Planning_name;
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

    postNewPlanning({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(LIST_PLANNING_ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            //store.dispatch("listPlanning/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Planning_name")) {
                    errorMsg += error.response.data.Planning_name;
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


    importPlanning({ commit }, data) {
      commit("SET_LOADING", true);
      let formData = new FormData();
      formData.append("file", data.files);

      return new Promise((resolve, reject) => {
        getAPI
          .post(UPLOAD_PLANNING, formData)
          .then((res) => {
            resolve(res);
            commit("SET_LOADING", false);
          })
          .catch((err) => {
            reject(err);
            commit("SET_UPLOAD_ERROR", err.message);
            commit("SET_LOADING", false);
          });
      });
    },


    importRealization({ commit }, data) {
      commit("SET_LOADING", true);
      let formData = new FormData();
      formData.append("file", data.files);

      return new Promise((resolve, reject) => {
        getAPI
          .post(UPLOAD_REALIZATION, formData)
          .then((res) => {
            resolve(res);
            commit("SET_LOADING", false);
          })
          .catch((err) => {
            reject(err);
            commit("SET_UPLOAD_ERROR", err.message);
            commit("SET_LOADING", false);
          });
      });
    },
    // patchListPlanning({ commit }, payload) {
    //   commit("POST_PATCH_INIT");
    //   const url = `${BUDGET_ENDPOINT}${payload.id}/`;
    //   return new Promise((resolve, reject) => {
    //     getAPI
    //       .patch(url, payload)
    //       .then((response) => {
    //         resolve(response);
    //         commit("POST_PATCH_SUCCESS");
    //         store.dispatch("listPlanning/getFromAPI");
    //         // store.dispatch("masterCategory/getFromAPI");
    //       })
    //       .catch((error) => {
    //         let errorMsg =
    //           "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
    //         if (error.response) {
    //           errorMsg = "";
    //           switch (error.response.status) {
    //             case 400:
    //               if (error.response.data.hasOwnProperty("Planning_name")) {
    //                 errorMsg += error.response.data.Planning_name;
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
  },
  mutations: {
    // import related
    SET_LOADING(state, data) {
      state.isLoading = data;
    },
    SET_UPLOAD_ERROR(state,error){
      state.errorMessage = error
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // get related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetListPlanning = true;
    },
    GET_SUCCESS(state, dataListPlanning) {
      state.requestStatus = "SUCCESS";
      state.loadingGetListPlanning = false;
      state.dataListPlanning = dataListPlanning;
    },
    GET_INACTIVE_INIT(state) {
      state.requestInactiveStatus = "PENDING";
      state.loadingGetListPlanning = true;
    },
    GET_INACTIVE_SUCCESS(state, dataListInactivePlanning) {
      state.requestInactiveStatus = "SUCCESS";
      state.loadingGetListInactivePlanning = false;
      state.dataListInactivePlanning = dataListInactivePlanning;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveListPlanning) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveListPlanning = dataActiveListPlanning;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetListPlanning = false;
      state.errorMsg = error;
      state.dataListPlanning = [];
      state.dataActiveListPlanning = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    GET_INACTIVE_ERROR(state, error) {
      state.requestInactiveStatus = "ERROR";
      state.loadingGetListInactivePlanning = false;
      state.errorMsg = error;
      state.dataListInactivePlanning = [];
      state.dataActiveListPlanning = [];
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchListPlanning = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.postPatchStatus = "SUCCESS";
      state.loadingPostPatchListPlanning = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.postPatchStatus = "ERROR";
      state.loadingPostPatchListPlanning = false;
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

export default listPlanning;
