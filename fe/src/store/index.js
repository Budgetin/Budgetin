import Vue from 'vue'
import Vuex from 'vuex'

// List Path Created Module
import breadcrumbs from "./breadcrumbs";
import choosedColumn from "./choosedColumn";
import dashboard from "./dashboard";
import masterCoa from "./masterCoa";
import masterStrategy from "./masterStrategy";
import masterProduct from "./masterProduct";
import statusInfo from "./statusInfo";
import masterUser from "./masterUser";
import masterEmployee from "./masterEmployee";
import login from "./login";
import startPlanning from "./startPlanning";
import monitorPlanning from "./monitorPlanning";
import allBiro from "./allBiro";
import allBiroItHc from "./allBiroItHc";
import listBudget from "./listBudget";
import listProject from "./listProject";
import projectDetail from "./projectDetail";
import projectType from "./projectType";

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
    dashboard,
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
    listBudget,
    listProject,
    projectDetail,
    choosedColumn,
    projectType,
  },
})
