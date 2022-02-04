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
        path: 'strategy',
        name: 'MasterStrategy',
        component: () => import("@/views/MasterStrategy/MasterStrategy"),
      },
      {
        path: '/strategy/:id/edit',
        name: 'EditMasterStrategy',
        component: () => import("@/views/MasterStrategy/EditMasterStrategy"),
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
        path: '/startPlanning/:id/viewStatusMonitor',
        name: 'ViewStatusMonitoring',
        component: () => import("@/views/StartPlanning/ViewStatusMonitoring")
      },
      {
        path: 'listProject',
        name: 'ListProject',
        component: () => import("@/views/ListProject/ListProject"),
      },
      {
        path: '/listProject/:id/view',
        name: 'ViewListProject',
        component: () => import("@/views/ListProject/ViewListProject")
      },
      {
        path: 'listPlanning',
        name: 'ListPlanning',
        component: () => import("@/views/ListPlanning/ListPlanning"),
      },
      {
        path: '/listPlanning/new',
        name: 'AddListPlanning',
        component: () => import("@/views/ListPlanning/AddListPlanning"),
      },
      {
        path: '/listPlanning/:id/view',
        name: 'EditListPlanning',
        component: () => import("@/views/ListPlanning/EditListPlanning")
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
