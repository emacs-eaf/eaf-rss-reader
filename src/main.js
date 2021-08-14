import Vue from 'vue'
import App from './App.vue'
import router from './router'
import MuseUI from 'muse-ui';
import 'muse-ui/dist/muse-ui.css';
import store from './store'
Vue.use(MuseUI);

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
