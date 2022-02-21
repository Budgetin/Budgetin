import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js";
const BUDGET_ENDPOINT = "/api/budget/";
const PLANNING_ENPOINT = "/api/planning/";
const UPLOAD_PLANNING = "/api/import/list_budget/";
const UPLOAD_REALIZATION = "/api/import/realisasi/";

const listBudget = {
  namespaced: true,
  state: {
    isLoading : false, //for loading when import planning
    errorMessage : "",
    loadingGetListBudget: false, // for loading table
    loadingGetListInactiveBudget: false, // for loading table
    loadingGetEdittedItem: false,
    loadingPostPatchListBudget: false, // for loading post/patch
    dataListBudget: [], // for v-data-table
    dataListInactiveBudget: [], // for v-data-table
    dataActiveListBudget: [], //for dropdown
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    requestInactiveStatus: "IDLE", //listplanning inactive
    requestActiveStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    errorMsg: null,
    edittedItem: null,
    edittedItemHistories: [],
  },
  getters: {
    value: (state) => state.value,
  },
  actions: {
    
//==Page ListBudget.vue

    //Get List Budget (Active)
    getListBudget({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(BUDGET_ENDPOINT + "active/")
        .then((response) => {
          const cleanData = response.data;
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
        });
    },

    getListInactiveBudget({ commit }) {
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

    getListActivePlanning({ commit }) {
      commit("GET_INIT");
      getAPI
        .get(PLANNING_ENPOINT + "active")
        .then((response) => {
          const cleanData = response.data;
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_ACTIVE_DATA_UPDATE", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
        });
    },
    
    getListBudgetById({ commit }, id) {
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

    postListBudget({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(BUDGET_ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("listBudget/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Budget_name")) {
                    errorMsg += error.response.data.Budget_name;
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

    postNewBudget({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(BUDGET_ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            //store.dispatch("listBudget/getFromAPI");
          })
          .catch((error) => {
            let errorMsg =
              "Unknown error. Please try again later. If this problem persisted, please contact System Administrator";
            if (error.response) {
              errorMsg = "";
              switch (error.response.status) {
                case 400:
                  if (error.response.data.hasOwnProperty("Budget_name")) {
                    errorMsg += error.response.data.Budget_name;
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


    importBudget({ commit }, data) {
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
            commit("SET_LOADING", false);
            commit("SET_UPLOAD_ERROR", err.message);
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
            commit("SET_LOADING", false);
            commit("SET_UPLOAD_ERROR", err.message);
          });
      });
    },
    downloadBudget({ commit }, data) {
      commit("SET_LOADING", true);

      return new Promise((resolve, reject) => {
        getAPI
          .get(BUDGET_ENDPOINT + "download/", {
            responseType: "arraybuffer", //Khusus download file
          })
          .then((response) => {
            resolve(response);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", "ListPlanning.xlsx");
            document.body.appendChild(link);
            link.click();
            commit("SET_LOADING", false);
          })
          .catch((err) => {
            reject(err);
            commit("SET_LOADING", false);
            commit("SET_DOWNLOAD_ERROR", err.message);
          });
      });
    },
  },
  mutations: {
    // import related
    SET_LOADING(state, data) {
      state.isLoading = data;
    },
    SET_UPLOAD_ERROR(state, error) {
      state.errorMessage = error;
      if (error.response.status == "401") {
        router.push({ name: "Login" });
      }
    },
    SET_DOWNLOAD_ERROR(state, error) {
      state.errorMessage = error;
      if (error.response.status == "401") {
        router.push({ name: "Login" });
      }
    },


    // get related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetListBudget = true;
    },
    GET_SUCCESS(state, dataListBudget) {
      state.requestStatus = "SUCCESS";
      state.loadingGetListBudget = false;
      state.dataListBudget = dataListBudget;
    },
    GET_INACTIVE_INIT(state) {
      state.requestInactiveStatus = "PENDING";
      state.loadingGetListBudget = true;
    },
    GET_INACTIVE_SUCCESS(state, dataListInactiveBudget) {
      state.requestInactiveStatus = "SUCCESS";
      state.loadingGetListInactiveBudget = false;
      state.dataListInactiveBudget = dataListInactiveBudget;
    },
    GET_ACTIVE_DATA_UPDATE(state, dataActiveListBudget) {
      state.requestActiveStatus = "IDLE";
      state.dataActiveListBudget = dataActiveListBudget;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetListBudget = false;
      state.errorMsg = error;
      state.dataListBudget = [];
      state.dataActiveListBudget = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
    GET_INACTIVE_ERROR(state, error) {
      state.requestInactiveStatus = "ERROR";
      state.loadingGetListInactiveBudget = false;
      state.errorMsg = error;
      state.dataListInactiveBudget = [];
      state.dataActiveListBudget = [];
    },

    // post / patch related
    POST_PATCH_INIT(state) {
      state.postPatchStatus = "PENDING";
      state.loadingPostPatchListBudget = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.postPatchStatus = "SUCCESS";
      state.loadingPostPatchListBudget = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.postPatchStatus = "ERROR";
      state.loadingPostPatchListBudget = false;
      state.errorMsg = error;
      if (error.response.status == "401") {
        router.push({ name: "Login" });
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

export default listBudget;
