import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Index from "@/views/Index";
import store from "@/store";

Vue.use(VueRouter);

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
        component: () => import("@/views/COA/ListCoa"),
      },
      {
        path: "/coa/:id/edit",
        name: "EditMasterCoa",
        component: () => import("@/views/COA/EditMasterCoa"),
      },
      {
        path: "product",
        name: "MasterProduct",
        component: () => import("@/views/MasterProduct/MasterProduct"),
      },
      {
        path: "/product/:id/edit",
        name: "EditMasterProduct",
        component: () => import("@/views/MasterProduct/EditMasterProduct"),
      },
      {
        path: "strategy",
        name: "MasterStrategy",
        component: () => import("@/views/MasterStrategy/MasterStrategy"),
      },
      {
        path: "/strategy/:id/edit",
        name: "EditMasterStrategy",
        component: () => import("@/views/MasterStrategy/EditMasterStrategy"),
      },
      {
        path: "/user/:id/edit",
        name: "EditMasterUser",
        component: () => import("@/views/MasterUser/EditMasterUser"),
      },
      {
        path: "user",
        name: "MasterUser",
        component: () => import("@/views/MasterUser/MasterUser"),
      },
      {
        path: "startPlanning",
        name: "StartPlanning",
        component: () => import("@/views/StartPlanning/StartPlanning"),
      },
      {
        path: "/startPlanning/:id/monitor",
        name: "MonitorPlanning",
        component: () => import("@/views/StartPlanning/MonitorPlanning"),
      },
      {
        path: "/startPlanning/:id/view",
        name: "ViewPlanning",
        component: () => import("@/views/StartPlanning/ViewPlanning"),
      },
      {
        path: "/startPlanning/:id/viewStatusMonitor",
        name: "ViewStatusMonitoring",
        component: () => import("@/views/StartPlanning/ViewStatusMonitoring"),
      },
      {
        path: "listProject",
        name: "ListProject",
        component: () => import("@/views/ListProject/ListProject"),
      },
      {
        path: "/listProject/:id/view",
        name: "ViewListProject",
        component: () => import("@/views/ListProject/ViewListProject"),
      },
      {
        path: "/listProject/:id/viewProjectDetail",
        name: "ViewListProjectDetail",
        component: () => import("@/views/ListProject/ViewListProjectDetail"),
      },
      {
        path: "/listProject/:id/viewBudgetPlanning",
        name: "ViewListBudgetPlanning",
        component: () => import("@/views/ListProject/ViewListBudgetPlanning"),
      },
      {
        path: "/listProject/:id/viewBudgetRealization",
        name: "ViewListBudgetRealization",
        component: () => import("@/views/ListProject/ViewListBudgetRealization"),
      },
      {
        path: "listBudget",
        name: "ListBudget",
        component: () => import("@/views/ListBudget/ListBudget"),
      },
      {
        path: "/listBudget/new",
        name: "ListBudgetNew",
        component: () => import("@/views/ListBudget/ListBudgetNew"),
      },
      {
        path: "/listBudget/existing",
        name: "ListBudgetExisting",
        component: () => import("@/views/ListBudget/ListBudgetExisting"),
      },
      {
        path: "/listBudget/:id/view",
        name: "EditListPlanning",
        component: () => import("@/views/ListBudget/EditListPlanning"),
      },
      {
        path: "/login",
        name: "Login",
        beforeEnter: (to, from, next) => {
          try {
            if (store.getters["login/isAuthenticated"]) {
              store
                .dispatch("login/setInitial")
                .then(() => {
                  if (!store.getters["login/isAuthenticated"]) {
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
            } else {
              next();
              return;
            }
          } catch (e) {
            ("masuk e");
            next();
            return;
          }
        },
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
