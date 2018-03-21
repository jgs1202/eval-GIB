<template>
<div id="dataInput">
  <div class="dataInput">
    <label>Name</label>
    <input v-model='userName' placeholder="fill your name">
    <button v-on:click="send">Confirm</button>
  </div>
</div>
</template>

<script>
export default {
  name: 'dataInput',
  data: function(){
    return{
      userName: null,
    }
  },
  methods: {
    send: function(event) {
      this.$parent.currentPage = 'App'
      this.$parent.userName = this.userName
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
