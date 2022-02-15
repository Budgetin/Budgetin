import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import login from "./login";
import breadcrumbs from "./breadcrumbs";
import home from "./home";

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
  },
})
