import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import breadcrumbs from "./breadcrumbs";
import choosedColumn from "./choosedColumn"
import login from "./login"
import listBudget from "./listBudget"
import listProject from "./listProject"
import statusInfo from "./statusInfo"
import masterCoa from "./masterCoa"
import masterProduct from "./masterProduct"
import allBiro from "./allBiro"
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
    login,
    listBudget,
    choosedColumn,
    masterCoa,
    masterProduct,
    allBiro,
    projectType,
    statusInfo,
    listProject,
  },
})
