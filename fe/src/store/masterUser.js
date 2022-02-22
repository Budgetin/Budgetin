import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/user/";
const LOGENDPOINT="/api/auditlog?table=user&entity=";

const masterUser = {
  namespaced: true,
  state: {
    // get list of user
    requestStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetMasterUser: false, // for loading table
    dataMasterUser: [], // for v-data-table
  
    // get data user by id
    requestUserByIdStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetUserById: false, // for loading table
    dataUserById: [], // for form

    // post/patch master user
    postPatchStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchMasterUser: false, // for loading post/patch

    // get history user by id
    requestHistoryMasterUserStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetHistoryMasterUser: false, // for loading table
    dataHistoryMasterUser: [], // for form

  },
  getters: {
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
                  name: data.display_name,
                  username: data.username,
                  option: String(data.name+" - "+data.username),                  
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
            a.id < b.id ? 1 : -1
          );
          commit("GET_SUCCESS", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR", error);
        });
    },
        
    getMasterUserById({ commit }, id) {
      commit("GET_INIT_USER_BY_ID");
      const url = `${ENDPOINT}${id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .get(url)
          .then((response) => {
            const data = response.data;
            let getData = {
                id: data.id,
                name: {
                  id: data.employee_id,
                  name: data.display_name,
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
            commit("GET_USER_BY_ID_SUCCESS", getData);
            resolve(getData);
          })
          .catch((error) => {
            commit("GET_USER_BY_ID_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },

    postMasterUser({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterUser/getMasterUser");
            resolve(response);
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
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
            commit("POST_PATCH_SUCCESS");
            store.dispatch("masterUser/getMasterUser");
            resolve(response);
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },
    
    getHistory({ commit }, id) {
      commit("GET_INIT_HISTORY_MASTER_USER"); 
      let url = `${LOGENDPOINT}${id}`;
      return new Promise((resolve, reject) => {
        getAPI
          .get(url)
          .then((response) => {
            const data = response.data;
            const sorted = data.sort((a, b) =>
            a.id < b.id ? 1 : -1
          );
            commit("GET_HISTORY_MASTER_USER_SUCCESS", sorted); 
            resolve(sorted);
          })
          .catch((error) => {
            commit("GET_HISTORY_MASTER_USER_ERROR", error);
            if(error.response.data.message){
              reject(error.response.data.message);
            }else{
              reject(error);
            }
          });
      });
    },
  },
  mutations: {
    // Get List of User related
    GET_INIT(state) {
      state.requestStatus = "PENDING";
      state.loadingGetMasterUser = true;
    },
    GET_SUCCESS(state, data) {
      state.requestStatus = "SUCCESS";
      state.loadingGetMasterUser = false;
      state.dataMasterUser = data;
    },
    GET_ERROR(state, error) {
      state.requestStatus = "ERROR";
      state.loadingGetMasterUser = false;
      state.dataMasterUser = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // Get User by Id
    GET_INIT_USER_BY_ID(state) {
      state.requestUserByIdStatus = "PENDING";
      state.loadingGetUserById = true;
    },
    GET_USER_BY_ID_SUCCESS(state, data) {
      state.requestUserByIdStatus = "SUCCESS";
      state.loadingGetUserById = false;
      state.dataUserById = data;
    },
    GET_USER_BY_ID_ERROR(state, error) {
      state.requestUserByIdStatus = "ERROR";
      state.loadingGetUserById = false;
      state.dataUserById = [];
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
      state.postPatchStatus = "SUCCESS";
      state.loadingPostPatchMasterUser = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.postPatchStatus = "ERROR";
      state.loadingPostPatchMasterUser = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // Get History List of User related
    GET_INIT_HISTORY_MASTER_USER(state) {
      state.requestHistoryMasterUserStatus = "PENDING";
      state.loadingGetHistoryMasterUser = true;
    },
    GET_HISTORY_MASTER_USER_SUCCESS(state, data) {
      state.requestHistoryMasterUserStatus = "SUCCESS";
      state.loadingGetHistoryMasterUser = false;
      state.dataHistoryMasterUser = data;
    },
    GET_HISTORY_MASTER_USER_ERROR(state, error) {
      state.requestHistoryMasterUserStatus = "ERROR";
      state.loadingGetHistoryMasterUser = false;
      state.dataHistoryMasterUser = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default masterUser;
