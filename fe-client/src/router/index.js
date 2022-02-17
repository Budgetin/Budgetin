import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Index from "@/views/Index";
import store from "@/store";

Vue.use(VueRouter)

function checkSession(next, url) {
  try {
    if (store.getters["login/isAuthenticated"] && store.getters["login/isUser"]) {
      next();
      return;
    } else {
      store
        .dispatch("login/setInitial")
        .then(() => {
          if (store.getters["login/isAuthenticated"] && store.getters["login/isUser"] && url!=='/login') {
            next();
            return;
          }
          else if(store.getters["login/isAuthenticated"] && store.getters["login/isUser"] && url=='/login'){
            router.push({ name: 'Home'});
            return;
          }else{
            if(store.getters["login/isAuthenticated"] && !store.getters["login/isUser"]){
              router.push({ name: '403Unauthorized'});
              return;
            }else{
              router.push({ name: 'Login', params: { redirectUrl: url !== '' ? url : '/home/' } });
              return;
            }
          }
         }).catch((err) => {
           if(err.response.status == 401 && url!=='/login'){
            if(store.getters["login/isAuthenticated"] && !store.getters["login/isUser"]){
              router.push({ name: '403Unauthorized'});
              return;
            }else{
              router.push({ name: 'Login', params: { redirectUrl: url !== '' ? url : '/home/' } });
              return;
            }
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
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
      },
      {
        path: "/home/:id/submitted",
        name: 'SubmittedList',
        component: () => import("@/views/Home/SubmittedList"),
      },
      {
        path: "/home/:id/submitted/new",
        name: 'AddNewProjectBudget',
        component: () => import("@/views/Home/AddNewProjectBudget"),
      },
      {
        path: "/home/:id/submitted/:id_project/view",
        name: "ViewMyPlanning",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MyProject/ViewMyPlanning"),
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
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MyProject/MyProject"),
      },
      {
        path: "/myProject/:id/view",
        name: "ViewMyProject",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MyProject/ViewMyProject"),
      },
      {
        path: "/myproject/:id/view/:id_project_detail/viewProjectDetail",
        name: "ViewMyProjectDetail",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MyProject/ViewMyProjectDetail"),
      },
      {
        path: "/myProject/:id/view/:id_budget_planning/viewBudgetPlanning",
        name: "ViewMyBudgetPlanning",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MyProject/ViewMyBudgetPlanning"),
      },
      {
        path: "/myProject/:id/view/:id_budget_realization/viewBudgetRealization",
        name: "ViewMyBudgetRealization",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MyProject/ViewMyBudgetRealization"),
      },
    ]
  },
  {
    path: '/login',
    name: 'Login',
    beforeEnter: (to, from, next) => {
      checkSession(next, to.fullPath);
    },
    // beforeEnter: (to, from, next) => {
    //   try {
    //     store
    //         .dispatch("login/setInitial")
    //         .then(() => {
    //           if (!store.getters["login/isAuthenticated"]) {
    //             next();
    //             return;
    //           } else {
    //             var url = to.params.redirectUrl.toString();
    //             router.push(url);
    //             return;
    //           }
    //         })
    //         .catch((err) => {
    //           next();
    //           return;
    //         });
    //   } catch (e) {
    //     ("masuk e");
    //     next();
    //     return;
    //   }
    // },
    component: () => import("@/views/Login"),
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: "*",
    name: "404NotFound",
    beforeEnter: (to, from, next) => {
      checkSession(next, to.fullPath);
    },
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/404NotFound.vue"),
  },
  {
    path: "/no-access",
    name: "403Unauthorized",
    beforeEnter: (to, from, next) => {
      if(store.getters["login/isAuthenticated"] && !store.getters["login/isUser"]){
        next();
        return;
      }
      else{
        router.push({ name: '404NotFound'});
        return;
      }
    },
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/403Unauthorized.vue"),
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
