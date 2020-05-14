<template>
  <div class="device">
        <p>Status:</p>
        <p v-html="status"></p>
        <button v-on:click=changeState>on/off</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      status: "off"
    }
  },
  mqtt: {
    /** on messages on that topic, update the state */
    'home/room/lamp1/state' (data) {
      this.status = data.toString()
      console.log('received:' + this.status)
    }
  },
  methods: {
    changeState: function() {
      var nextStatus
      if (this.status == 'on') {
        nextStatus = 'off'
      }
      else if (this.status == 'off') {
        nextStatus = 'on'
      }
      this.$mqtt.publish('home/room/lamp1/state', nextStatus)
      console.log('sent:' + nextStatus)
    }
  }
}
</script>