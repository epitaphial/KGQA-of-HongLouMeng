function showGraph(name,ifsentence) {
    var myChart = echarts.init(document.getElementById('main'));
    var categories = [{ name: "贾家荣国府" }, { name: "贾家宁国府" }, { name: "王家" }, { name: "史家" }, { name: "薛家" }, { name: "林家" }, { name: "其他" }];
    var realUrl;
    if(ifsentence){
        realUrl = "/qa/"+name
    }else{
        if(name === null){
            realUrl = "/getallrela";
        }else{
            realUrl = "/getrela/"+name;
        }
    }
    console.log(realUrl)
    $.ajax({
        url: realUrl,
        type: "get",
        dataType: "json",
        success: function (jsondata) {
            json_edges = jsondata['edges'];
            json_nodes = jsondata['nodes'];
            /*data: [{
                name: 'node01',
                des: 'nodedes01',
                symbolSize: 70,
                category: 0,
            }*/
            //console.log(json_nodes[200]['data']['name']);
            var nodedata = [];
            for (var i in json_nodes) {
                //console.log(i+":"+json_edges[i]);
                if (json_nodes[i] === null)
                    continue;

                var theindex = 0;
                for (var index in categories) {
                    if (categories[index]['name'] === json_nodes[i]['data']['clan']) {
                        theindex = index;
                        break;
                    }
                }
                var nodeSize = 50;
                if(name === json_nodes[i]['data']['name']){
                    nodeSize = 80;
                }
                nodedata.push(
                    {
                        name: json_nodes[i]['data']['name'],
                        symbolSize: nodeSize,
                        category: parseInt(theindex),
                    }
                );
            }
            /*
            [{
                source: 'node01',
                target: 'node02',
                name: 'link01',
                des: 'link01des'
            }]
            */

            var edgedata = [];
            for (var i in json_edges) {
                edgedata.push(
                    {
                        source: json_edges[i]['data']['source'],
                        target: json_edges[i]['data']['target'],
                        name: json_edges[i]['data']['relationship'],
                    }
                );
            }

            option = {
                // 图的标题
                title: {
                    text: '红楼梦人物关系图'
                },
                // 提示框的配置
                tooltip: {
                    formatter: function (x) {
                        return x.data.des;
                    }
                },
                // 工具箱
                toolbox: {
                    // 显示工具箱
                    show: true,
                    feature: {
                        mark: {
                            show: true
                        },
                        // 还原
                        restore: {
                            show: true
                        },
                        // 保存为图片
                        saveAsImage: {
                            show: true
                        }
                    }
                },
                legend: [{
                    // selectedMode: 'single',
                    data: categories.map(function (a) {
                        return a.name;
                    })
                }],
                series: [{
                    type: 'graph', // 类型:关系图
                    layout: 'force', //图的布局，类型为力导图
                    symbolSize: 40, // 调整节点的大小
                    roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [2, 10],
                    edgeLabel: {
                        normal: {
                            textStyle: {
                                fontSize: 20
                            }
                        }
                    },
                    force: {
                        repulsion: 2500,
                        edgeLength: [10, 50]
                    },
                    draggable: true,
                    lineStyle: {
                        normal: {
                            width: 2,
                            color: '#4b565b',
                            curveness: 0.5,
                        }
                    },
                    edgeLabel: {
                        normal: {
                            show: true,
                            formatter: function (x) {
                                return x.data.name;
                            }
                        }
                    },
                    label: {
                        normal: {
                            show: true,
                            textStyle: {}
                        }
                    },

                    // 数据
                    data: nodedata,
                    links: edgedata,
                    categories: categories,
                }]
            };
            myChart.setOption(option);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            //alert(XMLHttpRequest.status);
            //alert(XMLHttpRequest.readyState);
            //alert(textStatus);
            alert("获取关系图失败！");
        },
    })
}