import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import breadcrumbs from "./breadcrumbs";
import login from "./login";
import myProject from "./myProject"

Vue.use(Vuex)

export default new Vuex.Store({
  // state: {
  // },
  // mutations: {
  // },
  // actions: {
  // },
  // modules: {
  // }
  namespaced: true,
  modules: {
    breadcrumbs,
    login,
    myProject,
  },
})
