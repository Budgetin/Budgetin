import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Index',
    component: () => import("@/views/Index"),
    children: [
      {
        path: '/home',
        name: 'Home',
        component: () => import("@/views/Home/ListTask"),
      },
      {
        path: "myProject",
        name: "MyProject",
        // beforeEnter: (to, from, next) => {
        //   checkSession(next, to.fullPath);
        // },
        component: () => import("@/views/MyProject/MyProject"),
      },
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import("@/views/Login"),
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
