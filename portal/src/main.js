import Vue from 'vue'
import App from './App'
import VueMqtt from 'vue-mqtt'

Vue.use(VueMqtt, 'ws://127.0.0.1:9001/ws', {clientId: 'WebClient-' + parseInt(Math.random() * 100000)})

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount("#app");