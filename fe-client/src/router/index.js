import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Index from "@/views/Index";
import store from "@/store";

Vue.use(VueRouter)

function checkSession(next, url) {
  try {
    if (store.getters["login/isAuthenticated"]) {
      next();
      return;
    } else {
      store
        .dispatch("login/setInitial")
        .then(() => {
          if (store.getters["login/isAuthenticated"] && url!=='/login') {
            next();
            return;
          }
          else if(store.getters["login/isAuthenticated"] && url=='/login'){
            router.push({ name: 'StartPlanning'});
            return;
          }else{
            router.push({ name: 'Login', params: { redirectUrl: url !== '' ? url : '/startPlanning/' } });
            return;
          }
         }).catch((err) => {
           if(err.response.status == 401 && url!=='/login'){
            router.push({ name: 'Login', params: { redirectUrl: url !== '' ? url : '/startPlanning/' } });
            return;
           }else{
            next();
            return;
           }
          });;
      return;
    }
  } catch (e) {
    ("masuk e");
    next();
    return;
  }
}

const routes = [
  {
    path: '/',
    name: 'Index',
    redirect : '/login',
    component: () => import("@/views/Index"),
    children: [
      {
        path: '/home',
        name: 'Home',
        component: () => import("@/views/Home/ListTask"),
      },
      {
        path: "/myBudget",
        name: "ListBudget",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListBudget/ListBudget"),
      },
      {
        path: "/myBudget/new",
        name: "ListBudgetNew",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListBudget/ListBudgetNew"),
      },
      {
        path: "/myBudget/existing",
        name: "ListBudgetExisting",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListBudget/ListBudgetExisting"),
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
    beforeEnter: (to, from, next) => {
      try {
        console.log(from)
          store
            .dispatch("login/setInitial")
            .then(() => {
              if (!store.getters["login/isAuthenticated"]) {
                console.log(store.getters["login/isAuthenticated"]);
                next();
                return;
              } else {
                router.go(-1);
                return;
              }
            })
            .catch((err) => {
              next();
              return;
            });
      } catch (e) {
        ("masuk e");
        next();
        return;
      }
    },
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
