def ttest( urldb, argv, log_path ):
    return f"""dbrp "{ urldb }"."autogen"
var data = stream
    |from()
        .measurement('{ argv["measurement"] }')
    |window()
        .period(10s)
        .every(10s)

data
    @tTest()
        // specify the hotend field
        .field('{ argv["field"] }')
        // Keep a 1h rolling window
        .size(3600)
    |alert()
        .id('{ argv["field"] }')
        .crit(lambda: 0 < 100)
        .log('{ log_path }')
        |influxDBOut()
            .database('{ argv["database"] }')
            .retentionPolicy('autogen')
            .measurement('{ urldb }_alert')
    
data
    |influxDBOut()
        .create()
        .database('{ argv["database"] }')
        .retentionPolicy('autogen')
        .measurement('{ urldb }')
        .tag('hotend', 'a')
        .tag('bed', 'b')
        .tag('air', 'c')

"""