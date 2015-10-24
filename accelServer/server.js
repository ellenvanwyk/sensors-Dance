var http = require('http'),
    map = require('through2-map'),
    port = process.argv[2];
    //ip = process.argv[3];

console.log("--------------------");
console.log("listening on", port);
console.log("--------------------");

//instantiate server to SensorLog post requests
var server = http.createServer(function(req,res){
    //accept post requests
    if(req.method === 'POST'){
        req.pipe(map(function(chunk){
            sensorLogParse(chunk.toString());
            return(chunk.toString());
            })).pipe(res);
    }else{
        console.log("The request ", req, " is not a POST request.")
        res.end();
    }
});

//clean sensorLog data
var sensorLogParse = function(rawData){
    var cleanUp = {}; //empty JSON

    var firstPass = rawData.split('&');

    var secondPass = firstPass.map(n => n.split('='));

    var cleanUpPush = secondPass.map(n => cleanUp[n[0]] = n[1]); //push data to cleanUp JSON

    console.log(cleanUp);
    //cleanUp.map(n => console.log(n));
};

server.listen(port);
