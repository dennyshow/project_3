queue()
    .defer(d3.json, "diy_cookery/cuisines.json")
    .await(makeGraph);