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
      </div>
    </div>
  </el-main>
</el-container>
</template>

<script>
export default {
  name: 'dataInput',
  data: function() {
    return {
      userName: null,
      age: null,
      gender: "Male",
    }
  },
  methods: {
    send: function(event) {
      this.$parent.currentPage = 'Menu'
      this.$parent.userName = this.userName
      this.$parent.age = this.Age
      this.$parent.gender = this.gender
    },
    click1: function(event){
      this.$parent.currentPage = 'App'
    },
    click2: function(event){
      this.$parent.currentPage = 'App1'
    },
    click3: function(event){
      this.$parent.currentPage = 'App'
    },
    click4: function(event){
      this.$parent.currentPage = 'App1'
    }
  }
}
</script>

<style>

.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}

.el-button{
  size: small;
}


body {
  width: 100%;
  height: 100%;
  font-family: monospace;
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
