import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import masterCoa from "./masterCoa"

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
    masterCoa,
  },
})
