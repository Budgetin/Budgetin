import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import breadcrumbs from "./breadcrumbs";
import choosedColumn from "./choosedColumn"
import masterCoa from "./masterCoa"
import masterStrategy from "./masterStrategy"
import masterProduct from "./masterProduct"
import statusInfo from "./statusInfo"
import masterUser from "./masterUser"
import masterEmployee from "./masterEmployee"
import login from "./login"
import startPlanning from "./startPlanning"
import monitorPlanning from "./monitorPlanning"
import allBiro from "./allBiro"
import allBiroItHc from "./allBiroItHc"
import listPlanning from "./listPlanning"
import listProject from "./listProject"
import projectType from "./projectType"

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
    masterCoa,
    masterStrategy,
    masterProduct,
    statusInfo,
    masterUser,
    masterEmployee,
    login,
    startPlanning,
    monitorPlanning,
    allBiro,
    allBiroItHc,
    listPlanning,
    listProject,
    choosedColumn,
    projectType,
  },
})
