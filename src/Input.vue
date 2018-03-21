<template>
<div id="input">
  <div class="input">
    <label>Name</label>
    <input v-model="message" placeholder="fill your name">
    <button v-on:click="send">Confirm</button>
  </div>
</div>
</template>

<script>
export default {
  name: 'Input',
  methods: {
    send: function(event) {
      this.$parent.message = 'App'
    }
  }
}
</script>

<style>
body {
  width: 100%;
  height: 100%;
  font-family: monospace;
}
label {
  display: block;
}
</style>
