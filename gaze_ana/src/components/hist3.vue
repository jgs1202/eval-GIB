<template>
<div>
  <div id="app" class="app">
    <el-container>
      <el-aside width='20%'>
        <div class='text'>
          Which box does have the most intra-links?<br><br>
          グループ内リングか一番多いものを選んでください。
        </div>
        <div class="controls">
          <br>
          <label>Adjust width</label>
          <el-slider v-model="settings.width"></el-slider>
        </div>
        <div id='info' class='text'>
          accuracy : {{accuracy}} %<br>
          time : {{meanTime}} ms<br>
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
          <el-button v-on:click='restart'>Select</el-button>
        </div><br>
      </el-aside>
      <el-main>
        <div class="svg-container" :style="{width: settings.width + '%'}">
          <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
      <g id="nodes">{{nodes}}</g>
      <g id="links">{{links}}</g>
      <g id='boxes'>{{boxes}}</g>
      <g id='hist'>{{hist}}</g>
    </svg>
        </div>
      </el-main>
    </el-container>
  </div>
  <div class="sync">
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
      graph: null,
      simulation: null,
      // color: d3.scaleOrdinal(d3.interpolateRainbow),
      settings: {
        strokeColor: "#29B5FF",
        width: 100,
        svgWigth: 960,
        svgHeight: 600
      },
      nodes: [],
      links: [],
      boxes: [],
      choice: [],
      dataNum: 0,
      dataArray: [],
      dataMax: 120,
      startTime: null,
      time: null,
      answer: null,
      trajes: [],
      traje: [],
      hists: [],
      hist: [],
      queNum: 0,
      taskNum: 0, 
      accuracy: null,
      meanTime: null,
    }
  },
  mounted: function() {
    var that = this;
    that.dataNum = 0
    if (that.queNum >= that.dataMax){
      var txt = document.getElementsByClassName('text')
      txt[0].firstChild.data = 'Which box does have the least intra-links?'
      txt[0].childNodes[3].data = 'グループ内リンクが一番少ないBOXを選んでください。'
    }
    console.log("mounted");
  },
  methods: {
    restart: function() {
      var that = this;
      d3.selectAll('rect').remove()
      d3.selectAll('line').remove()
      d3.selectAll('circle').remove()

      if (that.queNum >= 120) {
        this.$parent.already = 1
        this.$parent.currentPage = 'Menu'
      } else {
        d3.json("./src/data/task"+ '' + (that.taskNum + 1) + '/' + that.queNum + ".json").then(function(graph) {
          that.graph = graph
          // console.log(that.graph.linkMax)
          that.graph.groups.pop()
          that.$set(that.nodes, that.reNodes())
          that.$set(that.links, that.reLinks())
          console.log('link end')
          that.$set(that.boxes, that.reBoxes())
          console.log('box end')
          that.reHist()
          that.abstinfo()
        })
      }
    },
    previousTask: function() {
      let that = this
      if (that.taskNum != 0){
        that.taskNum = parseInt(that.taskNum) - 1
        that.restart()
      }
    },
    nextTask: function() {
      let that = this
      if (that.taskNum != that.maxTask){
        that.taskNum = parseInt(that.taskNum) + 1
        that.restart()
      }
    },
    previousQue: function() {
      let that = this
      if (that.queNum != 0){
        that.queNum = parseInt(that.queNum) - 1
        that.restart()
      }
    },
    nextQue: function() {
      let that = this
      if (that.queNum != that.maxQue){
        that.queNum = parseInt(that.queNum) + 1
        that.restart()
      }
    },
    abstinfo: function() {
      var that = this
      let tmp = that.$parent.abstData[that.taskNum][that.queNum]
      that.accuracy = Math.round(parseInt(tmp['correct']) / parseInt(tmp['people']) * 1000) / 10
      that.meanTime = Math.round(parseInt(tmp['meanTime']))
    },
    reHist: function(dataNum) {
      console.log('hist calculation')
      var that = this
      let hist = {}
      hist.data = that.$parent.timeSeriese[that.taskNum][that.queNum]
      hist.plotData = Array(that.graph.gruopSize)
      for (let i=0; i<that.graph.groupSize; i++){
        hist.plotData[i] = Array(1000)
        if (i == that.graph.groupSize - 1){
        }
        for (let j=0; j<1000; j++){
          hist.plotData[i][j] = Array(2)
          hist.plotData[i][j][0] = j
          hist.plotData[i][j][1] = parseFloat(hist.data[i][j])
        }
        let a = [0]
        d3.select('svg').append('g')
          .attr('class', 'canpas')
          .selectAll('rect')
          .data(a)
          .enter()
          .append('rect')
          .attr('x', parseInt(that.graph.groups[i].x) + 5)
          .attr('y', parseInt(that.graph.groups[i].y) + 5)
          .attr('width', 100)
          .attr('height', 50)
          .attr('stroke', 'black')
          .attr('stroke-width', '0.4')
          .attr('fill', 'white')
        d3.select('svg').append('g')
          .attr('class', 'bar')
          .selectAll('rect')
          .data(hist.plotData[i])
          .enter()
          .append('rect')
          .attr('x', function(d, num){
            return parseInt(that.graph.groups[i].x) + num * 0.1 + 5
          })
          .attr('y', function(d, num){
            return parseInt(that.graph.groups[i].y) + 50 - hist.plotData[i][num][1] * 50 + 5
        })
          .attr('width', 0.1)
          .attr('height', function(d, num){
            return hist.plotData[i][num][1] * 50
          })
          // .attr("stroke", "black")
          // .attr("stroke-width", 5)
          // .attr("fill", 'transparent')
          .attr('fill', d3.rgb(152, 0 ,192))
        d3.select('svg').append('g')
          .attr('class', 'border')
          .selectAll('line')
          .data(that.graph.links)
          .enter().append("line")
          .attr('stroke', 'black')
          .attr("stroke-width", 1.0)
          .attr('x1', that.graph.groups[i].x + 5)
          .attr('x2', that.graph.groups[i].x + 100 + 5)
          .attr('y1', that.graph.groups[i].y + 50 + 5)
          .attr('y2', that.graph.groups[i].y + 50 + 5)
      }
      console.log('draw')
    },
    reFlow: function(dataNum) {
      console.log('flow calculation')
      var that = this
      let svg = d3.select('svg')
      svg.append("defs").append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 5)
        .attr("refY", 0)
        .attr('markerUnits', 'strokeWidth')
        .attr("markerWidth", 3)
        .attr("markerHeight", 3)
        .attr("orient", "auto")
      .append('svg:path')
        .attr("d", "M0,-5L10,0L0,5")
        .attr('fill', 'rgba(204,153,255,0.9)')

      let centers = []
      let arrows = []
      let overlaps = []
      let threshold = 5

      let max = 0
      for (let i=0; i<that.graph.groups.length - 1; i++){
        let dic = {}
        dic.x = that.graph.groups[i].x + that.graph.groups[i].dx / 2
        dic.y = that.graph.groups[i].y + that.graph.groups[i].dy / 2
        centers.push(dic)
      }
      console.log('reading')
      d3.json('./src/flows/task3/' + '' + dataNum + '.json').then(function(graph) {
        let container = d3.select('svg')
        for (let i=0; i<graph.length; i++){
          for (let j=0; j<graph[i].length; j++){
            if ((graph[i][j] > threshold) && (i !== j)) {
              let dic = {}
              dic.src = i
              dic.target = j
              dic.value = graph[i][j]
              arrows.push(dic)
              if (dic.value > max){
                max = dic.value
              }
            }
          }
        }
        for (let i=0; i<arrows.length; i++){
          for (let j=0; j<arrows.length; j++){
            if ((arrows[i].src === arrows[j].target) && (arrows[j].src === arrows[i].target)){
              if (parseInt(arrows[i].src) < parseInt(arrows[j].src)){
                overlaps.push([parseInt(arrows[i].src), parseInt(arrows[j].src)])
              }
            } 
          }
        }
        console.log(overlaps)
        for (let i=0; i<arrows.length; i++){
          let array1 = [arrows[i].src, arrows[i].target]
          let array2 = [arrows[i].target, arrows[i].src]
          let ver = 0
          for (let j=0; j<overlaps.length; j++){
            let ver1 = (array1[0] == overlaps[j][0]) && (array1[1] == overlaps[j][1])
            let ver2 = (array2[0] == overlaps[j][0]) && (array2[1] == overlaps[j][1])
            if (ver1 || ver2) {
              ver = 1
              break
            }
          }
          if (ver === 0){
            let dx = centers[arrows[i].src].x - centers[arrows[i].target].x
            let dy = centers[arrows[i].src].y - centers[arrows[i].target].y
            let line = container.append('line')
              .attr('x1', centers[arrows[i].src].x - dx / 8) //- 433)/1.477)
              .attr('x2', centers[arrows[i].target].x + dx / 8) // - 433)/1.477)
              .attr('y1', centers[arrows[i].src].y - dy / 8) // - 124)/1.477)
              .attr('y2', centers[arrows[i].target].y + dy / 8) // - 124)/1.477)
              .attr('stroke', 'rgba(204,153,255,0.9)')
              .attr('stroke-width', arrows[i].value * 1.3)
              .attr('marker-end', 'url(#arrowhead)')
          } else {
            console.log('ver is ' + '' + ver)
            let dirx = 0
            let diry = 0
            let comx = 0
            let comy = 0
            let tan = 0
            let Source = centers[arrows[i].src]
            let Target = centers[arrows[i].target]
            let margin = arrows[i].value * 1.7
            if ((Source.x > Target.x) && (Source.y > Target.y)) {
              dirx = -1
              diry = 1
              comx = 1
              comy = 1
              // sx = -
              // tx = +
              // sy = -
              // ty = +
            } else if ((Source.x > Target.x) && (Source.y < Target.y)){
              dirx = 1
              diry = 1
              comx = 1
              comy = -1
            } else if ((Source.x < Target.x) && (Source.y > Target.y)) {
              dirx = -1
              diry = -1
              comx = -1
              comy = 1
            } else if ((Source.x < Target.x) && (Source.y < Target.y)) {
              dirx = 1
              diry = -1
              comx = -1
              comy = -1
            } else if ((Source.x == Target.x) && (Source.y < Target.y)) {
              dirx = -1
              diry = 0
              comx = 0
              comy = -1
            } else if ((Source.x == Target.x) && (Source.y > Target.y)) {
              dirx = 1
              diry = 0
              comx = 0
              comy = 1
            } 
            let dx = Math.abs(centers[arrows[i].src].x - centers[arrows[i].target].x)
            let dy = Math.abs(centers[arrows[i].src].y - centers[arrows[i].target].y)
            let cos = Math.abs(dx / Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2)))
            let sin = Math.abs(dy / Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2)))
            console.log(cos, sin, cos*margin)
            let line = container.append('line')
              .attr('x1', centers[arrows[i].src].x - comx * dx / 5 + dirx * sin * margin) //- 433)/1.477)
              .attr('x2', centers[arrows[i].target].x + comx * dx / 5 + dirx * sin * margin) // - 433)/1.477)
              .attr('y1', centers[arrows[i].src].y - comy * dy / 5 + diry * cos * margin) // - 124)/1.477)
              .attr('y2', centers[arrows[i].target].y + comy * dy / 5 + diry * cos * margin) // - 124)/1.477)
              .attr('stroke', 'rgba(204,153,255,0.9)')
              .attr('stroke-width', arrows[i].value * 1.3)
              .attr('marker-end', 'url(#arrowhead)')

            // let line2 = container.append('line')
            //   .attr('x1', centers[arrows[i].src].x - comx * dx / 8) //- 433)/1.477)
            //   .attr('x2', centers[arrows[i].target].x + comx * dx / 8) // - 433)/1.477)
            //   .attr('y1', centers[arrows[i].src].y - comy * dy / 8) // - 124)/1.477)
            //   .attr('y2', centers[arrows[i].target].y + comy * dy / 8) // - 124)/1.477)
            //   .attr('stroke', 'red')
            //   .attr('stroke-width', arrows[i].value * 1)
          }
        }
        console.log('d3 end')
        obj._groups = d3.selectAll('.flow')._groups[0][0].childNodes
        return obj
      })
    },
    reNodes: function() {
      var that = this;
      if (that.graph) {
        d3.selectAll('circle').remove()
        d3.select("svg").append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(that.graph.nodes)
          .enter().append("circle")
          .attr('cx', that.settings.svgWigth / 2)
          .attr('cy', that.settings.svgHeight / 2)
          .attr("r", 3)
        return d3.selectAll("circle")
          .each(function(d, i) {
            var selection = d3.select(this)
            selection.transition()
              .attr('cx', that.graph.nodes[i].cx)
              .attr("cy", that.graph.nodes[i].cy)
              .attr("fill", function(d, i) {
                // return that.color(d.group / that.graph.groups.length);
                return d3.interpolateRainbow(d.group / that.graph.groups.length)
              })
          })
      }
    },
    onClick: function(event) {
      if (event.keyCode == '13') {
        var that = this
          that.choice = []
          d3.selectAll('rect').attr('stroke-width', 0.6).attr('stroke', 'black')
          d3.selectAll('circle').remove()
          d3.selectAll('line').remove()
          d3.selectAll('rect').remove()
          // that.graph = 0
          // d3.select('svg').remove()
          that.restart()
          // console.log('boxes')
          // } else {
          //   swal('Choose 1 boxes.')
          // }
        }
    },
    reLinks: function() {
      var that = this;
      if (that.graph) {
        d3.select("svg").append("g")
          .attr("class", "links")
          .selectAll("line")
          .data(that.graph.links)
          .enter().append("line")
          .attr('stroke', d3.rgb(200, 200, 200))
          .attr("stroke-width", function(d) {
            // return Math.sqrt(d.value);
            return 0.4;
          })
        d3.selectAll("line")
          .each(function(d, i) {
            // console.log('d is ')
            // console.log(d)
            if (d.source.x){
              var a = 0
            }
            else {
              var selection = d3.select(this)
              selection.attr('x1', function(d) {
                  // console.log(that.graph.nodes[d.source].cx)
                  return that.graph.nodes[d.source].cx
                })
                .attr('y1', function(d) {
                  return that.graph.nodes[d.source].cy
                })
                .attr('x2', function(d) {
                  return that.graph.nodes[d.target].cx
                })
                .attr('y2', function(d) {
                  return that.graph.nodes[d.target].cy
                })
              }
            })
          d3.selection.prototype.moveToFront = function() {
            return this.each(function() {
              this.parentNode.parentNode.appendChild(this.parentNode);
            })
          }
        d3.select('circle').moveToFront()
      }
      return d3.selectAll(".links")._groups[0][0].chileNodes
    },
    reBoxes: function() {
      var that = this
      if (that.graph) {
        d3.select("svg").append("g")
          .attr("class", "rect")
          .selectAll("rect")
          .data(that.graph.groups)
          .enter().append("rect")
          .attr("stroke", "black")
          .attr("stroke-width", 1)
          .attr("fill", 'transparent')

        function func(event) {
          // console.log(event)
          d3.selectAll('rect')
            .each(function(d, i) {
              if (event.x == d.x && event.y == d.y) {
                var selection = d3.select(this)
                if (selection.attr('stroke') == 'black') {
                  d3.selectAll('rect')
                    .attr("stroke-width", 1)
                    .attr('stroke', 'black')
                  this.parentNode.appendChild(this)
                  selection.attr("stroke-width", 3)
                    .attr('stroke', d3.rgb(102, 200, 255))
                  for (let i in that.graph.groups) {
                    if (event.x == that.graph.groups[i].x && event.y == that.graph.groups[i].y) {
                      that.choice = [i]
                      break
                    }
                  }
                } else if (selection.attr('stroke') == d3.rgb(102, 200, 255)) {
                  selection.attr("stroke-width", 1)
                    .attr('stroke', 'black')
                  let tmp
                  for (let i in that.graph.groups) {
                    if (event.x == that.graph.groups[i].x && event.y == that.graph.groups[i].y) {
                      tmp = i
                      console.log(i)
                      break
                    }
                  }
                  for (let i in that.choice) {
                    if (tmp == that.choice[i]) {
                      that.choice.splice(i, 1)
                    }
                  }
                }
              }
            })
          console.log(that.choice)
        }

        return d3.selectAll('rect')
          .each(function(d, i) {
            if (d['dx'] != that.settings.svgWigth || d['dy'] != that.settings.svgHeight) {
              var selection = d3.select(this)
                .attr('index', i)
                .attr('x', d['x'])
                .attr('y', d['y'])
                .attr('width', d['dx'])
                .attr('height', d['dy'])
                .on('click', func)
            }
          })
      }
    }
  }
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
  padding-bottom: 2rem;
  margin-top: 2rem;
  /* margin: auto; */
  background: #f8f8f8;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.sync {
  background: black;
  height: 60px;
  width: 60px;
  position: absolute;
  right: 0;
  bottom: 0;
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

.svg-container {
  margin: auto;
  display: table;
  border: 0px solid #f8f8f8;
  /* box-shadow: 1px 2px 4px rgba(0, 0, 0, .5); */
}

.controls>*+* {
  margin-top: 1rem;
}

label {
  display: block;
}

.links line {
  stroke: #999;
  stroke-opacity: 1;
}

.traje line {
  stroke: #EF75A5;
  stroke-width: 0.8;
}

/*.nodes circle {
  stroke: #fff;
  stroke-width: 1.0px;
}*/
</style>
