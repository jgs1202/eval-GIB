<template>
<div>
  <div id="app" class="app">
    <el-container>
      <el-aside width='20%'>
        <div class="controls">
          <br>
          <label>Adjust width</label>
          <el-slider v-model="settings.width"></el-slider>
          <!-- <input type="range" v-model="settings.width" min="0" max="100" /> -->
        </div>
        <div id="selectQue" style="margin-left: auto;">
          <div id="task">
            <el-button v-on:click='previousTask'>Previous</el-button>
            Task: <el-input placeholder="task number" v-model="taskNum" style='width:60px;'></el-input>
            <el-button v-on:click='nextTask'>Next</el-button>
          </div><br>
          <div id='question'>
            <el-button v-on:click='previousQue'>Previous</el-button>
            Question: <el-input placeholder="question number" v-model="queNum" style='width:60px;'></el-input>
            <el-button v-on:click='nextQue'>Next</el-button>
          </div><br>
          <el-button v-on:click='reload'>Select</el-button>
        </div><br>
        <div id='information' style='margin-left: auto;'>
          <span>accuracy: {{accuracy}}</span><br><br>
          <span>completion time: {{meanTime}}</span><br><br>
          <span>layout: {{layout}}</span>
        </div>
      </el-aside>
      <el-main>
        <div class="svg-container" :style="{width: settings.width + '%'}">
          <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
          </svg>
        </div>
      </el-main>
    </el-container>
  </div>
  <div id="load" style='margin-top: auto; padding-top: 30%;'>
    loading...
  </div>
</div>
</template>

<script>
import axios from 'axios'
const d3 = require('d3')
const swal = require('sweetalert')
export default {
  name: 'app',
  data: function() {
    return {
      settings: {
        strokeColor: "#29B5FF",
        width: 100,
        svgWigth: 960,
        svgHeight: 600
      },
      abstinfo: null,
      scarfData: null,
      choice: [],
      dataArray: [],
      dataNum: 0,
      dataMax: 120,
      task: [],
      taskNum: 0,
      queNum: 0,
      maxQue: 120,
      maxTask: 3,
      accuracy: null,
      meanTime: null,
      layout: null,
    }
  },
  mounted: function() {
    var that = this;
    document.getElementById('app').style.display = 'none'
    d3.json("./src/trajectory/queInfo.json").then(function(data1) {
      that.abstinfo = data1
      d3.json("./src/trajectory/scarfData.json").then(function(data2) {
        console.log('load end')
        that.scarfData = data2
        that.loadEnd()
      })
    })
  },
  methods: {
    loadEnd: function() {
      document.getElementById('load').style.display = 'none'
      document.getElementById('app').style.display = 'block'
    },
    previousQue: function() {
      let that = this
      if (that.queNum != 0){
        that.queNum = parseInt(that.queNum) - 1
        that.reload()
      }
    },
    nextQue: function() {
      let that = this
      if (that.queNum != that.maxQue){
        that.queNum = parseInt(that.queNum) + 1
        that.reload()
      }
    },
    previousTask: function() {
      let that = this
      if (that.taskNum != 0){
        that.taskNum = parseInt(that.taskNum) - 1
        that.reload()
      }
    },
    nextTask: function() {
      let that = this
      if (that.taskNum != that.maxTask){
        that.taskNum = parseInt(that.taskNum) + 1
        that.reload()
      }
    },
    reload: function() {
      d3.selectAll('rect').remove()
      d3.selectAll('line').remove()
      d3.selectAll('text').remove()
      var that = this;
      let scarf = {}
      scarf.graph = that.scarfData[that.taskNum][that.queNum]
      scarf.colors = []
      scarf.groupSize = that.abstinfo[that.taskNum][that.queNum].groupSize
      scarf.answers = that.abstinfo[that.taskNum][that.queNum].answers
      console.log(scarf.answers)
      scarf.margin_left = 100
      scarf.margin_top = 20
      scarf.width = 700
      scarf.height = 570
      scarf.eachHeight = scarf.height / scarf.graph.length - 10
      let a = [0]
      let b = [0, 1]

      that.accuracy = Math.round(parseInt(that.abstinfo[that.taskNum][that.queNum].correct) / parseInt(that.abstinfo[that.taskNum][that.queNum].people) * 1000) / 10
      that.meanTime = Math.round(parseInt(that.abstinfo[that.taskNum][that.queNum].meanTime))
      that.layout = that.abstinfo[that.taskNum][that.queNum].layout

      scarf.legend = {}
      scarf.legend.left = 850
      scarf.legend.top = 180
      scarf.legend.square = 20
      scarf.legend.margin = 10

      console.log(scarf.eachHeight, scarf.graph.length)
      for (let i=0; i<scarf.groupSize; i++){
        scarf.colors.push(d3.interpolateRainbow(i / scarf.groupSize))
      }
      for(let person=0; person<scarf.graph.length; person++){
        d3.select('svg').append('g')
          .attr('class', 'canpas')
          .selectAll('rect')
          .data(scarf.graph[person].data)
          .enter()
          .append('rect')
          .attr('x', function(d, num){
            return scarf.margin_left + parseFloat(d.start) * scarf.width
          })
          .attr('y', function(d, num){
            if (scarf.answers != null){
              for (let i=0; i<3; i++){
                if (parseInt(d.AOI) == parseInt(scarf.answers[i])){
                  return scarf.margin_top + person / scarf.graph.length * scarf.height + scarf.eachHeight / 2  / 3 * (i)
                } else if (i == 2){
                  return scarf.margin_top + person / scarf.graph.length * scarf.height + scarf.eachHeight / 2
                }
              }
            } else {
              return scarf.margin_top + person / scarf.graph.length * scarf.height
            }
          })
          .attr('width', function(d, num){
            if (parseFloat(d.length) * scarf.width + parseFloat(d.start) * scarf.width > scarf.width){
              return scarf.width - (scarf.margin_left + parseFloat(d.start) * scarf.width)
            } else {
              return parseFloat(d.length) * scarf.width
            }
          })
          .attr('height', function(d, num){
            if (scarf.answers != null){
              for (let i=0; i<3; i++){
                if (parseInt(d.AOI) == parseInt(scarf.answers[i])){
                  return scarf.eachHeight / 2 + scarf.eachHeight / 2 /3 * (3 - i)
                } else if (i == 2){
                  return scarf.eachHeight / 2
                }
              }
            } else {
              return scarf.eachHeight
            }
          })
          .attr('stroke', function(d, num){
            return scarf.colors[parseInt(d.AOI)]
          })
          .attr('stroke-width', '0.4')
          .attr('fill', function(d, num){
            return scarf.colors[parseInt(d.AOI)]
          })
        d3.select('svg').append('g')
          .attr('class', 'border')
          .selectAll('line')
          .data(b)
          .enter().append("line")
          .attr('stroke', function(d, num){
            return d3.rgb(255 * num * 4 / 5, 255 * num * 4 / 5, 255 * num * 4 / 5)
          })
          .attr("stroke-width", 1.0)
          .attr('x1', scarf.margin_left)
          .attr('x2', scarf.margin_left + scarf.width)
          .attr('y1', function(d, num){
            return scarf.margin_top + person / scarf.graph.length * scarf.height + scarf.eachHeight - num * scarf.eachHeight
          })
          .attr('y2', function(d, num){
            return scarf.margin_top + person / scarf.graph.length * scarf.height + scarf.eachHeight - num * scarf.eachHeight
          })
        d3.select('svg').append('g')
          .attr('class', 'participants')
          .selectAll('text')
          .data(a)
          .enter().append("text")
          .text('participants ' + ''  + person)
          .attr('x', scarf.margin_left / 10)
          .attr('y', scarf.margin_top + person / scarf.graph.length * scarf.height + scarf.eachHeight / 4 * 3)
          .attr("font-family", "sans-serif")
          .attr("font-size", "12px")
          .attr("fill", "black");
      }
      d3.select('svg').append('g')
        .attr('class', 'legend')
        .selectAll('rect')
        .data(scarf.colors)
        .enter()
        .append('rect')
        .attr('x', scarf.legend.left)
        .attr('y', function(d, num){
          return scarf.legend.top + num * (scarf.legend.square + scarf.legend.margin)
        })
        .attr('width', scarf.legend.square)
        .attr('height', scarf.legend.square)
        .attr('stroke', function(d, num){
          return scarf.colors[num]
        })
        .attr('stroke-width', '0.4')
        .attr('fill', function(d, num){
          return scarf.colors[num]
        })
      d3.select('svg').append('g')
          .attr('class', 'AOI_ name')
          .selectAll('text')
          .data(scarf.colors)
          .enter().append("text")
          .text(function(d, num){
            return 'AOI ' + ''  + num
          })
          .attr('x', scarf.legend.left + scarf.legend.square + scarf.legend.margin)
          .attr('y', function(d, num){
            return scarf.legend.top + num * (scarf.legend.square + scarf.legend.margin) + scarf.legend.square * 3 / 4
          })
          .attr("font-family", "sans-serif")
          .attr("font-size", "16px")
          .attr("fill", "black")

        d3.select('svg').append('g')
          .attr('class', 'AOI_title')
          .selectAll('text')
          .data(a)
          .enter().append("text")
          .text('AOIs')
          .attr('x', scarf.legend.left + scarf.legend.square / 2)
          .attr('y', function(d, num){
            return scarf.legend.top - (1) * (scarf.legend.margin + scarf.legend.square) + scarf.legend.square * 3 / 4
          })
          .attr("font-family", "sans-serif")
          .attr("font-size", "16px")
          .attr("fill", "black");


      if (scarf.answers !== null){
        d3.select('svg').append('g')
          .attr('class', 'answer')
          .selectAll('rect')
          .data(scarf.answers)
          .enter()
          .append('rect')
          .attr('x', scarf.legend.left)
          .attr('y', function(d, num) {
            return scarf.legend.top - (5 - num) * (scarf.legend.margin + scarf.legend.square)
          })
          .attr('width', scarf.legend.square)
          .attr('height', scarf.legend.square)
          .attr('stroke', function(d, num){
            return scarf.colors[parseInt(scarf.answers[num])]
          })
          .attr('stroke-width', '0.4')
          .attr('fill', function(d, num){
            return scarf.colors[parseInt(scarf.answers[num])]
          })

        d3.select('svg').append('g')
          .attr('class', 'answer_ name')
          .selectAll('text')
          .data(scarf.answers)
          .enter().append("text")
          .text(function(d, num){
            return 'AOI ' + ''  + scarf.answers[num]
          })
          .attr('x', scarf.legend.left + scarf.legend.square + scarf.legend.margin)
          .attr('y', function(d, num){
            return scarf.legend.top - (5 - num) * (scarf.legend.margin + scarf.legend.square) + scarf.legend.square * 3 / 4
          })
          .attr("font-family", "sans-serif")
          .attr("font-size", "16px")
          .attr("fill", "black");

        d3.select('svg').append('g')
          .attr('class', 'answer_title')
          .selectAll('text')
          .data(a)
          .enter().append("text")
          .text('Answer')
          .attr('x', scarf.legend.left + scarf.legend.square / 2)
          .attr('y', function(d, num){
            return scarf.legend.top - (6) * (scarf.legend.margin + scarf.legend.square) + scarf.legend.square * 3 / 4
          })
          .attr("font-family", "sans-serif")
          .attr("font-size", "16px")
          .attr("fill", "black");
      }


      console.log('draw end')
    },
  },
}
</script>


<style>
body {
  margin: auto;
  width: 100%;
  height: 100%;
  font-family: 'serif';
}

.app {
  margin: auto;
  width: 95%;
  height: 95%;
  font-family: 'serif';
}

.controls {
  text-align: center;
  width: 80%;
  margin: auto;
  padding-bottom: 10px;
  margin-top: 2rem;
  /* margin: auto; */
  background: #f8f8f8;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.svg-container {
  position: relative;
  height: 100%;
  /* display: table; */
  margin: auto;
  border: 0px solid #f8f8f8;
  /* box-shadow: 1px 2px 4px rgba(0, 0, 0, .5); */
}

.controls>*+* {
  margin-top: 1rem;
}

.question {
  margin: auto;
  text-align: center;
}

.container {
  text-align: center;
}

label {
  display: block;
}

.text {
  width: 80%;
  margin: auto;
  text-align: center;
  margin-top: 20%;
  font-size: 1.3rem;
}

.el-aside {
  /* border: 1px solid #67C23A; */
  box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
}

.el-main {
  box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
  text-align: center;
}

.el-radio {
  width: 40%;
}

/*.nodes circle {
  stroke: #fff;
  stroke-width: 1.0px;
}*/
</style>
