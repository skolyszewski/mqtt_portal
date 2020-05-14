<template>
  <div class="device">
        <p v-html="status">Status:</p>
        <button @click=changeState>on/off</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      status: 'State:' + this.state
    }
  },
  mqtt: {
    /** on messages on that topic, update the state */
    'home/room/lamp1/state' (data) {
      this.status = data.toString()
      console.log(this.state)
    }
  }
}
</script>