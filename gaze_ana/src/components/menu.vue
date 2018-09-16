<template>
<div>
  <el-container>
    <el-header></el-header>
    <el-main>
      <div id="dataInput">
        <div class="dataInput">
          <el-button v-on:click='analysisWay="App"'>Trajectory</el-button>
          <el-button v-on:click='analysisWay="flow"'>Flow</el-button><br><br>
          <span>Next Page: {{analysisWay}}</span><br><br>
          <el-row>
            <el-button type="primary" v-on:click="click1">　　　　task1　　　　</el-button>
          </el-row>
          <el-row>
            <el-button type="success" v-on:click="click2">　　　　task2　　　　</el-button>
          </el-row>
          <el-row>
            <el-button type="warning" v-on:click="click3">　　　　task3　　　　</el-button>
          </el-row>
          <el-row>
            <el-button type="danger" v-on:click="click4">　　　　task4　　　　</el-button>
          </el-row>
          <br><br>
          <el-row :gutter='20' v-if='nextPage != null'>
            <el-col :span='10' :offset="7">
              <el-alert :closable=false :center=true title="Press enter to start experiments." type="success">
              </el-alert>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-main>
  </el-container>
  <div class="sync">
  </div>
</div>
</template>

<script>
const swal = require('sweetalert')
export default {
  name: 'dataInput',
  data: function() {
    return {
      userName: null,
      age: null,
      gender: "Male",
      nextPage: null,
      analysisWay: 'flow'
    }
  },
  mounted: function() {
    let that = this
    var sync = document.getElementsByClassName('sync')
    for (let i = 0; i < sync.length; i++) {
      if (that.$parent.already == 1) {
        sync[i].style.background = 'black'
        setTimeout(that.toWhite, 2000)
      }
    }
  },
  methods: {
    send: function(event) {
      this.$parent.currentPage = 'Menu'
      this.$parent.userName = this.userName
      this.$parent.age = this.Age
      this.$parent.gender = this.gender
    },
    click1: function(event) {
      if (this.$parent.num1 != 120){
        this.nextPage = this.analysisWay + '1'
        window.addEventListener('keyup', this.submit, false)
      } else {
        swal('You have already done this course.')
      }
    },
    click2: function(event) {
      if (this.$parent.num2 == 60){
        swal('タスクが変わります！\n Enterを押すと実験に進みます。')
      }
      if (this.$parent.num2 != 120){
        this.nextPage = this.analysisWay + '2'
        window.addEventListener('keyup', this.submit, false)
      } else {
        swal('You have already done this course.')
      }
    },
    click3: function(event) {
      if (this.$parent.num3 == 60){
        swal('タスクが変わります！\n Enterを押すと実験に進みます。')
      }
      if (this.$parent.num3 != 120){
        this.nextPage = this.analysisWay + '3'
        window.addEventListener('keyup', this.submit, false)
      } else {
        swal('You have already done this course.')
      }
    },
    click4: function(event) {
      if (this.$parent.num4 != 120){
        this.nextPage = this.analysisWay + '4'
        window.addEventListener('keyup', this.submit, false)
      } else {
        swal('You have already done this course.')
      }
    },
    submit: function(event) {
      // console.log('key')
      if (event.keyCode == 13) {
        if (this.nextPage == null) {
          swal("Choose a task.")
        } else {
          this.$parent.currentPage = this.nextPage
          window.removeEventListener('keyup', this.submit)
        }
      }
    },
    toWhite: function() {
      var that =this
      var sync = document.getElementsByClassName('sync')
      for (let i = 0; i < sync.length; i++) {
        if (that.$parent.already == 1) {
          sync[i].style.background = 'white'
        }
      }
    }
  }
}
</script>

<style>
.el-row {
  margin-bottom: 20px;
  text-align: center;
  margin-left: auto;
}

.el-main{
  box-shadow: 0px 0px 0px rgba(0, 0, 0, .5);
}

.el-button {
  size: small;
}


body {
  width: 100%;
  height: 100%;
  font-family: 'serif';
  text-align: center;
}

table {
  border-collapse: separate;
  border-spacing: 0px 15px;
}

tr {
  margin-top: 10px;
}

.sync {
  background: white;
  height: 60px;
  width: 60px;
  position: absolute;
  right: 0;
  bottom: 0;
}
</style>
