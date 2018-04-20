<template>
<div id="home">
  <component :is="currentPage"></component>
</div>
</template>

<script>
import Vue from 'vue'
import App1 from './components/App1.vue'
import App2 from './components/App2.vue'
import App3 from './components/App3.vue'
import App4 from './components/App4.vue'
import Menu from './components/menu.vue'
import dataInput from './components/dataInput.vue'
Vue.component('dataInput', dataInput)
Vue.component('App1', App1)
Vue.component('App2', App2)
Vue.component('App3', App3)
Vue.component('App4', App4)
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
