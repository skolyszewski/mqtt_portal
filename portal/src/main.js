import Vue from 'vue'
import App from './App'
import VueMqtt from 'vue-mqtt'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


Vue.use(VueMqtt, 'ws://127.0.0.1:9001/ws', {clientId: 'WebClient-' + parseInt(Math.random() * 100000)})
// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount("#app");
