<template>
  <div class="device">
    <div class="column" id="name">
      Name:<br>{{name}}
    </div>
    <div class="column" id="status">
      <div class="innerColumn" id="statusRead">
        Status: {{status}}
      </div>
      <div class="innerColumn" id="statusSwitch">
        <button v-on:click=changeState>on/off</button>
      </div>
      </div>
    <div v-if="temp" class="column" id="temp">
      <div  class="innerColumn" id="tempRead">
        Temperature (*C): {{temp}}
      </div>
      <div class="innerColumn" id="tempWrite">
        <input v-model="wantedTemperature">
        <button v-on:click=changeTemp>set</button>
      </div>
    </div>
    <div v-if="rpm" class="column" id="RPM">
      <div  class="innerColumn" id="RPMRead">
        RPM (/min): {{rpm}}
      </div>
      <div class="innerColumn" id="RPMWrite">
        <input v-model="wantedRPM">
        <button v-on:click=changeRPM>set</button>
      </div>
    </div>
    <div v-if="ct" class="column" id="ct">
      <div  class="innerColumn" id="CTRead">
        Color temperature (K): {{ct}}
      </div>
      <div class="innerColumn" id="CTWrite">
        <input v-model="wantedCT">
        <button v-on:click=changeCT>set</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'name',
    'topic',
  ],
  data: function () {
    return {
      status: this.status,
      temp: this.temp,
      rpm: this.rpm,
      ct: this.ct
    }
  },
  created () {
    this.shortTopic = 'home/' + this.name + '/'
  },
  mqtt: {
    /** on messages on that topic, update the state */
    '#' (data, topic) {
      console.log(this.shortTopic)
      if (topic.includes(this.shortTopic)) {
        let param = topic.split('/').pop()
        console.log(param)
        if (param == 'state') {
          this.status = data.toString()
        }
        else if (param == 'temp') {
          this.temp = data.toString()
        }
        else if (param == 'rpm') {
          this.rpm = data.toString()
        }
        else if (param == 'ct') {
          this.ct = data.toString()
        }
        console.log('received:' + data.toString())
      }
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
      this.$mqtt.publish(this.shortTopic + 'state', nextStatus)
      console.log('sent:' + nextStatus)
    },
    changeTemp: function() {
      var nextTemperature = this.wantedTemperature
      this.$mqtt.publish(this.shortTopic + 'temp', nextTemperature)
      console.log('sent:' + nextTemperature)
    },
    changeRPM: function() {
      var nextRPM = this.wantedRPM
      this.$mqtt.publish(this.shortTopic + 'rpm', nextRPM)
      console.log('sent:' + nextRPM)
    },
    changeCT: function() {
      var nextCT = this.wantedCT
      this.$mqtt.publish(this.shortTopic + 'ct', nextCT)
      console.log('sent:' + nextCT)
    }
  }
}
</script>

<style scoped>
.device {
  float: left;
  width: 100%;
  margin-bottom: 1em;
}

.column {
  float: left;
  width: 30%;
}

.column.innerColumn {
  float: left;
  width: auto;
}

</style>