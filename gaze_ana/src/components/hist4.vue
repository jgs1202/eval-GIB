<template>
<div>
  <div id="app" class="app">
    <el-container>
      <el-aside width='20%'>
        <div class='text'>
          Which box is with the most inter links?<br><br>
          最も多くのグループ間リンクを持つBOXを選んでください。
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
      </el-aside>
      <el-main>
        <div class="svg-container" :style="{width: settings.width + '%'}">
          <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
      <g id="nodes">{{nodes}}</g>
      <g id="links">{{links}}</g>
      <g id='boxes'>{{boxes}}</g>
      <g id='traje'>{{traje}}</g>
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
      accuracy: null,
      meanTime: null,
    }
  },
  mounted: function() {
    window.addEventListener('keyup', this.onClick)
    var that = this;
    console.log("mounted");
    that.dataNum = that.$parent.num4
    if (that.$parent.num4 >= that.dataMax){
      that.dataArray = that.$parent.set4
    } else {
      for (let i=0; i < 120; i++) {
        that.dataArray.push(i)
      }
      that.$parent.set4 = that.dataArray
    }
    d3.json("./src/data/task4/" + '' + that.dataArray[that.dataNum] + ".json").then(function(graph) {
      // if (err) throw err;
      that.graph = graph
      that.graph.groups.pop()
      console.log("json")
      that.$set(that.nodes, that.reNodes())
      that.$set(that.links, that.reLinks())
      that.$set(that.boxes, that.reBoxes())
      that.reHist()
      that.abstinfo()
    })
    // that.trajes = that.$parent.traje
    // that.traje = that.reTrajes()
  },
  methods: {
    restart: function() {
      var that = this;
      that.dataNum += 1
      console.log(that.dataNum)
      if (that.dataNum % that.dataMax == 0){
        that.$parent.num4 = that.dataNum
        this.$parent.already = 1
        this.$parent.currentPage = 'Menu'
      }
      d3.json("./src/data/task4/" + '' + that.dataArray[that.dataNum] + ".json").then(function(graph) {
        that.graph = graph
        that.graph.groups.pop()
        that.$set(that.nodes, that.reNodes())
        that.$set(that.links, that.reLinks())
        that.$set(that.boxes, that.reBoxes())
        that.reHist()
        that.abstinfo()
      })
      var sync = document.getElementsByClassName('sync')
      console.log(sync[0].style.background)
      for(let i=0; i<sync.length; i++){
        if ( that.dataNum % 2 == 0 ){
          sync[i].style.background = 'black'
        } else {
          sync[i].style.background = 'white'
        }
      }
      // that.traje = that.reTrajes()
    },
    abstinfo: function() {
      var that = this
      let tmp = that.$parent.abstData[3][that.dataArray[that.dataNum]]
      that.accuracy = Math.round(parseInt(tmp['correct']) / parseInt(tmp['people']) * 1000) / 10
      that.meanTime = Math.round(parseInt(tmp['meanTime']))
    },
    reHist: function(dataNum) {
      console.log('hist calculation')
      var that = this
      let hist = {}
      hist.data = that.$parent.timeSeriese[3][that.dataArray[that.dataNum]]
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
    reTrajes: function() {
      var that = this;
      if (that.trajes) {
        d3.select("svg").append("g")
          .attr("class", "traje")
          .selectAll("line")
          .data(that.trajes[3][that.dataNum])
          .enter().append("line")
          .attr("stroke-width", function(d) {
            return 1;
          })
        console.log(d3.selectAll('.traje')._groups[0][0])
        d3.selectAll("line")
          .each(function(d, i) {
            if (d.source.x) {
              var selection = d3.select(this)
              selection.attr('x1', function(d) {
                  return (d.source.x - 433)/1.477
                })
                .attr('y1', function(d) {
                  return (d.source.y - 124) / 1.477
                })
                .attr('x2', function(d) {
                  return (d.target.x - 433)/1.477
                })
                .attr('y2', function(d) {
                  return (d.target.y - 124) / 1.477
                })
              }
          })
        }
      var obj = {}
      obj._groups = d3.selectAll('.traje')._groups[0][0].childNodes
      return obj
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
        // console.log(that.graph)
          d3.selectAll('rect').attr('stroke-width', 0.6).attr('stroke', 'black')
          d3.selectAll('circle').remove()
          d3.selectAll('line').remove()
          d3.selectAll('rect').remove()
          that.restart()
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
                  // selection.remove()
                  // console.log(this.attributes.index)
                  // d3.select("svg").append("rect")
                  //   .attr("stroke", d3.rgb(102, 200, 255))
                  //   .attr("stroke-width", 3)
                  //   .attr("fill", 'transparent')
                  //   .attr('index', this.attributes.index)
                  //   .attr('x', this.x.animVal.value)
                  //   .attr('y', this.y.animVal.value)
                  //   .attr('width', this.width.animVal.value)
                  //   .attr('height', this.height.animVal.value)
                  //   .on('click', func)
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
  },
  computed: {
    // nodes: function() {
    //   var that = this;
    //   if (that.graph) {
    //     console.log('this is')
    //     console.log(this)
    //     return d3.select("svg").append("g")
    //       .attr("class", "nodes")
    //       .selectAll("circle")
    //       .data(that.graph.nodes)
    //       .enter().append("circle")
    //       .attr('cx', 0)
    //       .attr('cy', 0)
    //       .attr("r", 20)
    //       .attr("fill", function(d, i) {
    //         return that.color(i);
    //       })
    // .call(d3.drag()
    //   .on("start", function dragstarted(d) {
    //     if (!d3.event.active) that.simulation.alphaTarget(0.3).restart();
    //     d.fx = d.x;
    //     d.fy = d.y;
    //   })
    //   .on("drag", function dragged(d) {
    //     d.fx = d3.event.x;
    //     d.fy = d3.event.y;
    //   })
    //   .on("end", function dragended(d) {
    //     if (!d3.event.active) that.simulation.alphaTarget(0);
    //     d.fx = null;
    //     d.fy = null;
    //   }));
    //   }
    // },
    // nodes: function(){
    //   console.log('nodes')
    //   return this.reNodes()
    // },
    exnodes: function() {
      var that = this;
      if (that.graph) {
        d3.select("svg").append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(that.graph.nodes)
          .enter().append("circle")
          .attr('cx', 0)
          .attr('cy', 0)
          .attr("r", 3)
        return d3.selectAll("circle")
          .each(function(d, i) {
            // console.log(d)
            // console.log(this)
            // console.log(that.graph.nodes[i].cx)
            var selection = d3.select(this)
            selection.transition()
              .attr('cx', that.graph.nodes[i].cx)
              .attr("cy", that.graph.nodes[i].cy)
              .attr("fill", function(d, i) {
                return that.color(d.group);
              })
          })
      }
    },
    exlinks: function() {
      var that = this;
      if (that.graph) {
        d3.select("svg").append("g")
          .attr("class", "links")
          .selectAll("line")
          .data(that.graph.links)
          .enter().append("line")
          .attr("stroke-width", function(d) {
            // return Math.sqrt(d.value);
            return Math.sqrt(1);
          })
        d3.selectAll("line")
          .each(function(d, i) {
            // console.log('d is ')
            // console.log(d)
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
          })
        d3.selection.prototype.moveToFront = function() {
          return this.each(function() {
            this.parentNode.parentNode.appendChild(this.parentNode);
          })
        }
        d3.select('circle').moveToFront()
        return d3.selectAll("line")
      }
    },
    exboxes: function() {
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
          console.log(event)
          d3.selectAll('rect')
            .each(function(d, i) {
              if (event.x == d.x && event.y == d.y) {
                var selection = d3.select(this)
                if (selection.attr('stroke') == 'black') {
                  // selection.remove()
                  // console.log(this.attributes.index)
                  // d3.select("svg").append("rect")
                  //   .attr("stroke", d3.rgb(102, 200, 255))
                  //   .attr("stroke-width", 3)
                  //   .attr("fill", 'transparent')
                  //   .attr('index', this.attributes.index)
                  //   .attr('x', this.x.animVal.value)
                  //   .attr('y', this.y.animVal.value)
                  //   .attr('width', this.width.animVal.value)
                  //   .attr('height', this.height.animVal.value)
                  //   .on('click', func)
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
                      // console.log(i)
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
            // console.log(d['x'])
            // console.log(d)
            // console.log(this)
            // console.log(that.graph.nodes[i].cx)
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
    // updated: function() {
    //   var that = this;
    //   that.simulation.nodes(that.graph.nodes).on('tick', function ticked() {
    //     that.links
    //       .attr("x1", function(d) {
    //         return d.source.x;
    //       })
    //       .attr("y1", function(d) {
    //         return d.source.y;
    //       })
    //       .attr("x2", function(d) {
    //         return d.target.x;
    //       })
    //       .attr("y2", function(d) {
    //         return d.target.y;
    //       });
    //
    //     that.nodes
    //       .attr("cx", function(d) {
    //         return d.x;
    //       })
    //       .attr("cy", function(d) {
    //         return d.y;
    //       });
    //   });
    // }
  },
  // updated: function() {
  //   // console.log(this.graph.nodes[0]['cx'], this.nodes[0], this.Choice)
  // }
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

.text {
  width : 80%;
  margin: auto;
  text-align: center;
  margin-top: 20%;
  font-size: 1.3rem;
}

.el-aside{
  /* border: 1px solid #67C23A; */
  box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
}

.el-main{
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

.sync {
  background: black;
  height: 60px;
  width: 60px;
  position: absolute;
  right: 0;
  bottom: 0;
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
