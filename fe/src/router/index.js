import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Index from "@/views/Index";
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index,
    children:[  
      {
        path: 'coa',
        name: 'Coa',
        component: () => import("@/views/COA/ListCoa"),
      },
      {
        path: '/coa/:id/edit',
        name: 'EditMasterCoa',
        component: () => import("@/views/COA/EditMasterCoa"),
      },
      {
        path: 'product',
        name: 'MasterProduct',
        component: () => import("@/views/MasterProduct/MasterProduct"),
      },
      {
        path: '/product/:id/edit',
        name: 'EditMasterProduct',
        component: () => import("@/views/MasterProduct/EditMasterProduct"),
      },
      {
        path: '/user/:id/edit',
        name: 'EditMasterUser',
        component: () => import("@/views/MasterUser/EditMasterUser"),
      },
      {
        path: 'user',
        name: 'MasterUser',
        component: () => import("@/views/MasterUser/MasterUser"),
      },
      {
        path: 'startPlanning',
        name: 'StartPlanning',
        component: () => import("@/views/StartPlanning/StartPlanning"),
      }, 
      {
        path: '/startPlanning/:id/monitor',
        name: 'MonitorPlanning',
        component: () => import("@/views/StartPlanning/MonitorPlanning")
      },
      {
        path: '/startPlanning/:id/view',
        name: 'ViewPlanning',
        component: () => import("@/views/StartPlanning/ViewPlanning")
      },
      {
        path: '/startPlanning/edit',
        name: 'EditPlanning',
        component: () => import("@/views/StartPlanning/EditPlanning")
      },
      {
        path: '/startPlanning/viewStatusMonitor',
        name: 'ViewStatusMonitoring',
        component: () => import("@/views/StartPlanning/ViewStatusMonitoring")
      },
      {
        path: '/startPlanning/editStatusMonitor',
        name: 'EditStatusMonitoring',
        component: () => import("@/views/StartPlanning/EditStatusMonitoring")
      },
      {
        path: 'listProject',
        name: 'ListProject',
        component: () => import("@/views/ListProject/ListProject"),
      },   
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import("@/views/Login")
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
