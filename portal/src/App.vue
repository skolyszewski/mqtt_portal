<template>
  <div id="app">
    <img alt="smart home" src="./assets/homelamp.png" width=100>
    <device></device>
  </div>
</template>

<script>
import Device from './components/Device'
export default {
  name: 'app',
  components: {
    Device
  },
  created () {
    this.$mqtt.subscribe('home/#')
    console.log("subscribed!")
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
