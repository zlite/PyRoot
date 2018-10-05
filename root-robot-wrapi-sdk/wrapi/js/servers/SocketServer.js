"use strict";

var net = require('net');

var _self = null;
class SocketServer {
    constructor(port, didReceiveSocketData) {
        _self = this;
        _self._connection = null;
        _self._didReceiveSocketData = didReceiveSocketData;

        _self.server = net.createServer(function(connection) {
            _self._connection = connection;
            console.log("Client connected."); //##Improve command line messages.

            _self._connection.on('end', function() {
                console.log('Client disconnected.'); //##Improve command line messages.

                //Very important: Without this assignment, the write function will crash after the client disconnects.
                _self._connection = null;
            });

            _self._connection.on('data', function(data) {
                _self._didReceiveSocketData(data)
            });
        });

        _self.server.listen(port, function() {
            console.log('Server is listening.'); //##Improve command line messages.
        });
    }

    //##Experiment:
    write(data) {
        //console.log("SocketServer.write:"); //##Debug.
        if (_self._connection !== null) {
            //console.log(data); //##Debug.
            _self._connection.write(data);
        }
    }
}

exports = module.exports = SocketServer;
