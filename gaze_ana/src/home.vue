<template>
<div id="home">
  <component :is="currentPage"></component>
</div>
</template>

<script>
const d3 = require('d3')
import Vue from 'vue'
import App1 from './components/App1.vue'
import App2 from './components/App2.vue'
import App3 from './components/App3.vue'
import App4 from './components/App4.vue'
import flow1 from './components/flow1.vue'
import flow2 from './components/flow2.vue'
import flow3 from './components/flow3.vue'
import flow4 from './components/flow4.vue'
import Menu from './components/menu.vue'
import dataInput from './components/dataInput.vue'
Vue.component('dataInput', dataInput)
Vue.component('App1', App1)
Vue.component('App2', App2)
Vue.component('App3', App3)
Vue.component('App4', App4)
Vue.component('flow1', flow1)
Vue.component('flow2', flow2)
Vue.component('flow3', flow3)
Vue.component('flow4', flow4)
Vue.component('Menu', Menu)
export default {
  name: 'home',
  data: function() {
    return {
      currentPage: null,
      userName: 'null',
      gender: 'null',
      age: null,
      already: null,
      set1: [],
      num1: 0,
      set2: [],
      num2: 0,
      set3: [],
      num3: 0,
      set4: [],
      num4: 0,
      traje: null,
    }
  },
  mounted: function(){
    var that = this
    d3.json("./src/trajectory/data.json").
      then(function(data) {
        that.traje = data
        that.currentPage = 'Menu'
    })
  },
}
</script>

<style>
body {
  font-family: 'Avenir';
  margin-top: 4%;
}
</style>