import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import masterCoa from "./masterCoa"
import masterStrategy from "./masterStrategy"
import masterProduct from "./masterProduct"


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
    masterStrategy,
    masterProduct,

  },
})
