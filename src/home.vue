<template>
<div id="home">
  <component :is="currentPage"></component>
</div>
</template>

<script>
import Vue from 'vue'
import App from './App.vue'
import dataInput from './dataInput.vue'
Vue.component('App', App)
Vue.component('dataInput', dataInput)
export default {
  name: 'home',
  data: function() {
    return {
      currentPage: 'dataInput',
      userName: 'null',
    }
  }
}
</script>
