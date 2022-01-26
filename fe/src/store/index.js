import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import masterCoa from "./masterCoa"
import masterStrategy from "./masterStrategy"
import masterProduct from "./masterProduct"
import statusInfo from "./statusInfo"
import masterUser from "./masterUser"
import masterEmployee from "./masterEmployee"
import login from "./login"
import startPlanning from "./startPlanning"


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
    statusInfo,
    masterUser,
    masterEmployee,
    login,
    startPlanning
  },
})
