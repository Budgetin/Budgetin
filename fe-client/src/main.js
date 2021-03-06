import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import vuetify from "./plugins/vuetify";
import "vuetify/dist/vuetify.min.css";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";


Vue.config.productionTip = false
Vue.use(Antd);


new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
