<template>
<el-container>
  <el-header></el-header>
  <el-main>
    <div id="dataInput">
      <div class="dataInput">
        <table align="center">
          <tr>
            <td>
              <el-input placeholder="Please input" v-model="userName">
                <template slot="prepend">Name</template>
              </el-input>
            </td>
          </tr>
          <tr>
            <td>
              <el-input placeholder="Please input" v-model="age">
                <template slot="prepend">Age</template>
              </el-input>
            </td>
          </tr>
          <tr>
            <td>
              <template>
                <el-radio v-model="gender" label="Male" border>Male</el-radio>
                <el-radio v-model="gender" label="Female" border>Female</el-radio>
              </template>
            </td>
          </tr>
          <tr>
            <td><br>
              <el-button type="primary" v-on:click='send'>Primary</el-button>
            </td>
          </tr>
        </table>
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
      this.$parent.currentPage = 'App'
      this.$parent.userName = this.userName
      this.$parent.age = this.Age
      this.$parent.gender = this.gender
    }
  }
}
</script>

<style>
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
