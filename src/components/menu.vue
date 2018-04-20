<template>
<el-container>
  <el-header></el-header>
  <el-main>
    <div id="dataInput">
      <div class="dataInput">
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
      this.nextPage = 'App1'
      window.addEventListener('keyup', this.submit, false)
    },
    click2: function(event) {
      this.nextPage = 'App2'
      window.addEventListener('keyup', this.submit, false)
    },
    click3: function(event) {
      this.nextPage = 'App3'
      window.addEventListener('keyup', this.submit, false)
    },
    click4: function(event) {
      this.nextPage = 'App4'
      window.addEventListener('keyup', this.submit, false)
    },
    submit: function(event) {
      // console.log('key')
      if (event.keyCode == 13) {
        if (this.nextPage == null) {
          swal("Choose a task.")
        } else {
          this.$parent.currentPage = this.nextPage
        }
      }
    }

  }
}
</script>

<style>
.el-row {
  margin-bottom: 20px;
  text-align:  center;
  margin-left: auto;
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

.dataInput {
  margin: auto;
}
</style>
