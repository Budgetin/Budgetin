import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Index from "@/views/Index";
import store from "@/store";

Vue.use(VueRouter);

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
    path: "/",
    name: "Index",
    redirect: '/login',
    component: Index,
    children: [
      {
        path: "coa",
        name: "Coa",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/COA/ListCoa"),
      },
      {
        path: "/coa/:id/edit",
        name: "EditMasterCoa",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/COA/EditMasterCoa"),
      },
      {
        path: "product",
        name: "MasterProduct",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MasterProduct/MasterProduct"),
      },
      {
        path: "/product/:id/edit",
        name: "EditMasterProduct",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MasterProduct/EditMasterProduct"),
      },
      {
        path: "strategy",
        name: "MasterStrategy",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MasterStrategy/MasterStrategy"),
      },
      {
        path: "/strategy/:id/edit",
        name: "EditMasterStrategy",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MasterStrategy/EditMasterStrategy"),
      },
      {
        path: "/user/:id/edit",
        name: "EditMasterUser",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MasterUser/EditMasterUser"),
      },
      {
        path: "user",
        name: "MasterUser",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/MasterUser/MasterUser"),
      },
      {
        path: "startPlanning",
        name: "StartPlanning",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/StartPlanning/StartPlanning"),
      },
      {
        path: "/startPlanning/:id/monitor",
        name: "MonitorPlanning",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/StartPlanning/MonitorPlanning"),
      },
      {
        path: "/startPlanning/:id/view",
        name: "ViewPlanning",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/StartPlanning/ViewPlanning"),
      },
      {
        path: "/startPlanning/:id/viewStatusMonitor",
        name: "ViewStatusMonitoring",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/StartPlanning/ViewStatusMonitoring"),
      },
      {
        path: "projectList",
        name: "ListProject",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListProject/ListProject"),
      },
      {
        path: "/projectList/:id/view",
        name: "ViewListProject",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListProject/ViewListProject"),
      },
      {
        path: "/projectList/:id/viewProjectDetail",
        name: "ViewListProjectDetail",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListProject/ViewListProjectDetail"),
      },
      {
        path: "/projectList/:id/viewBudgetPlanning",
        name: "ViewListBudgetPlanning",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListProject/ViewListBudgetPlanning"),
      },
      {
        path: "/projectList/:id/viewBudgetRealization",
        name: "ViewListBudgetRealization",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListProject/ViewListBudgetRealization"),
      },
      {
        path: "/budgetList",
        name: "ListBudget",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListBudget/ListBudget"),
      },
      {
        path: "/budgetList/new",
        name: "ListBudgetNew",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListBudget/ListBudgetNew"),
      },
      {
        path: "/budgetList/existing",
        name: "ListBudgetExisting",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListBudget/ListBudgetExisting"),
      },
      {
        path: "/budgetList/:id/view",
        name: "EditListPlanning",
        beforeEnter: (to, from, next) => {
          checkSession(next, to.fullPath);
        },
        component: () => import("@/views/ListBudget/EditListPlanning"),
      },
      {
        path: "/login",
        name: "Login",
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
    ],
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});
export default router;
