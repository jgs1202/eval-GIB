<template>
<div id="home">
  <component :is="currentPage"></component>
</div>
</template>

<script>
import Vue from 'vue'
import App from './components/App.vue'
import App1 from './components/App1.vue'
import Menu from './components/menu.vue'
import dataInput from './components/dataInput.vue'
Vue.component('App', App)
Vue.component('dataInput', dataInput)
Vue.component('App1', App1)
Vue.component('Menu', Menu)
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
