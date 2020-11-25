import Vue from 'vue'
import Vuex from 'vuex'
import vuetify from './plugins/vuetify'
import i18n from './plugins/i18n'
import glovue from './plugins/glovue'
import router from './router'
import { store } from './store'
import App from './App.vue'

Vue.use(Vuex)
Vue.use(glovue);
Vue.config.productionTip = false

new Vue({
  vuetify,
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
