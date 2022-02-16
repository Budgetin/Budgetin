import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import login from "./login";
import breadcrumbs from "./breadcrumbs";
import myProject from "./myProject"
import home from "./home";
import choosedColumn from "./choosedColumn"
import listBudget from "./listBudget"
import listProject from "./listProject"
import statusInfo from "./statusInfo"
import masterCoa from "./masterCoa"
import masterProduct from "./masterProduct"
import allBiro from "./allBiro"
import projectType from "./projectType"
import projectDetail from "./projectDetail"
import allBudget from "./allBudget"

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
    home,
    listBudget,
    choosedColumn,
    masterCoa,
    masterProduct,
    allBiro,
    projectType,
    statusInfo,
    listProject,
    projectDetail,
    allBudget,
  },
})
