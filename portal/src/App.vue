<template>
  <div id="app">
    <h3>Your devices</h3>
    <device
      v-for="device in devices"
      v-bind:key="device.name"
      v-bind:name="device.name"
      v-bind:topic="device.topic"
    />
  </div>
</template>

<script>
import Device from './components/Device'
export default {
  name: 'app',
  components: {
    Device
  },
  data: function() {
    return {
      devices: this.devices,
    }
  },
  created () {
    this.devices = []
    this.names = []
    this.$mqtt.subscribe('home/#')
    console.log("subscribed!")
  },
  mqtt: {
    'home/#' (data, topic) {
      let name = topic.split('/')[1]
      let device = {'name': name, 'topic': topic}
      console.log("received: " + data + " on topic " +  topic)
      if (!this.names.includes(name)) {
        this.names.push(name)
        this.devices.push(device)
      }
    }
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
