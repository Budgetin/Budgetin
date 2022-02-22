import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/biro/";

const allBiro = {
  namespaced: true,
  state: {
    //getAllBiro
    requestAllBiroStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetAllBiro: false, // for loading table
    dataAllBiro: [], // for v-data-table

    //postAllBiro & patchAllBiro
    requestPostPatchAllBiroStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchAllBiro: false, // for loading post/patch
  },
  getters: {
  },
  actions: {
    getAllBiro({ commit }) {
      commit("GET_INIT_ALL_BIRO");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_ALL_BIRO", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_ALL_BIRO", error);
        });
    },

    postAllBiro({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("allBiro/getAllBiro");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },

    patchAllBiro({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("allBiro/getAllBiro");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },
  },

  mutations: {
    // get allBiro related
    GET_INIT_ALL_BIRO(state) {
      state.requestAllBiroStatus = "PENDING";
      state.loadingGetAllBiro = true;
    },
    GET_SUCCESS_ALL_BIRO(state, dataAllBiro) {
      state.requestAllBiroStatus = "SUCCESS";
      state.loadingGetAllBiro = false;
      state.dataAllBiro = dataAllBiro;
    },
    GET_ERROR_ALL_BIRO(state, error) {
      state.requestAllBiroStatus = "ERROR";
      state.loadingGetAllBiro = false;
      state.dataAllBiro = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post/patch related
    POST_PATCH_INIT(state) {
      state.requestPostPatchAllBiroStatus = "PENDING";
      state.loadingPostPatchAllBiro = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestPostPatchAllBiroStatus = "SUCCESS";
      state.loadingPostPatchAllBiro = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestPostPatchAllBiroStatus = "ERROR";
      state.loadingPostPatchAllBiro = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default allBiro
