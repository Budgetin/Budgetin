import store from ".";
import { getAPI } from "@/plugins/axios-api.js";
import router from "@/router/index.js"

const ENDPOINT = "/api/ithc/biro";

const allBiroItHc = {
  namespaced: true,
  state: {
    //getAllBiroItHc
    requestAllBiroItHcStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingGetAllBiroItHc: false, // for loading table
    dataAllBiroItHc: [], // for v-data-table

    //postAllBiroItHc & patchAllBiroItHc
    requestPostPatchAllBiroItHcStatus: "IDLE", // possible values: IDLE (does nothing), SUCCESS (get success), ERROR (get error)
    loadingPostPatchAllBiroItHc: false, // for loading post/patch
  },
  getters: {
  },
  actions: {
    getAllBiroItHc({ commit }) {
      commit("GET_INIT_ALL_BIRO_IT_HC");
      getAPI
        .get(ENDPOINT)
        .then((response) => {
          const cleanData = response.data
          const sorted = cleanData.sort((a, b) =>
            a.update_at > b.update_at ? 1 : -1
          );
          commit("GET_SUCCESS_ALL_BIRO_IT_HC", sorted);
        })
        .catch((error) => {
          commit("GET_ERROR_ALL_BIRO_IT_HC", error);
        });
    },

    postAllBiroItHc({ commit }, payload) {
      commit("POST_PATCH_INIT");
      return new Promise((resolve, reject) => {
        getAPI
          .post(ENDPOINT, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("allBiroItHc/getAllBiroItHc");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },

    patchAllBiroItHc({ commit }, payload) {
      commit("POST_PATCH_INIT");
      const url = `${ENDPOINT}${payload.id}/`;
      return new Promise((resolve, reject) => {
        getAPI
          .patch(url, payload)
          .then((response) => {
            resolve(response);
            commit("POST_PATCH_SUCCESS");
            store.dispatch("allBiroItHc/getAllBiroItHc");
          })
          .catch((error) => {
            commit("POST_PATCH_ERROR", error.response.data);
            reject(error.message);
          });
      });
    },
  },

  mutations: {
    // get allBiroItHc related
    GET_INIT_ALL_BIRO_IT_HC(state) {
      state.requestAllBiroItHcStatus = "PENDING";
      state.loadingGetAllBiroItHc = true;
    },
    GET_SUCCESS_ALL_BIRO_IT_HC(state, dataAllBiroItHc) {
      state.requestAllBiroItHcStatus = "SUCCESS";
      state.loadingGetAllBiroItHc = false;
      state.dataAllBiroItHc = dataAllBiroItHc;
    },
    GET_ERROR_ALL_BIRO_IT_HC(state, error) {
      state.requestAllBiroItHcStatus = "ERROR";
      state.loadingGetAllBiroItHc = false;
      state.dataAllBiroItHc = [];
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },

    // post/patch related
    POST_PATCH_INIT(state) {
      state.requestPostPatchAllBiroItHcStatus = "PENDING";
      state.loadingPostPatchAllBiroItHc = true;
    },
    POST_PATCH_SUCCESS(state) {
      state.requestPostPatchAllBiroItHcStatus = "SUCCESS";
      state.loadingPostPatchAllBiroItHc = false;
    },
    POST_PATCH_ERROR(state, error) {
      state.requestPostPatchAllBiroItHcStatus = "ERROR";
      state.loadingPostPatchAllBiroItHc = false;
      if(error.response.status =="401"){
        router.push({ name: 'Login'});
      }
    },
  },
};

export default allBiroItHc
