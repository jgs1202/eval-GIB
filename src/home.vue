<template>
<div id="home">
  <component :is="currentPage"></component>
</div>
</template>

<script>
import Vue from 'vue'
import App from './App.vue'
import App1 from './App1.vue'
import dataInput from './dataInput.vue'
Vue.component('App', App)
Vue.component('dataInput', dataInput)
Vue.component('App1', App1)
export default {
  name: 'home',
  data: function() {
    return {
      currentPage: 'dataInput',
      userName: 'null',
      gender: 'null',
      age: null,
    }
  }
}
</script>
