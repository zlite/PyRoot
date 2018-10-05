"use strict";

let packetHelper = require("../computing/PacketHelper.js");
let bleManager = require("../devices/BleManager.js");
let SocketServer = require("./SocketServer.js");

//##Move this one to a different file:
var _self = null;
class BleSocketServer {
    constructor(port) {
        _self = this;

        //Set the callbacks:
        this._socketServer = new SocketServer(port, _self.didReceiveSocketData);
        bleManager.didReceiveData = _self.didReceiveBleData;

        _self.ansCanWrite = 10; //##7.
        _self.ansData = 20; //##7.

        _self.commands = {
            "10": _self.getVersion,
            "20": _self.startScanning,
            "30": _self.stopScanning,
            "40": _self.connectDevice,
            "50": _self.disconnectDevice,
            "60": _self.startTx,
            "70": _self.stopTx,
            "80": _self.write,
            "90": _self.setClientDisconnectionCmd
        }

        _self._uuidLen = 36;
    }

    get uuidLen() {
        return _self._uuidLen;
    }

    _getPayLoadLen(data) {
        var payLoadLenArray = [0].concat(0, data[0], data[1]);
        //console.log(payLoadLenArray); //##Debug.
        return packetHelper.byteArrayToInt32(payLoadLenArray);
    }

    //Rx callbacks:
    didReceiveSocketData(data) {
        //console.log("didReceiveSocketData: " + data); //##Debug.
        //console.log(data[0].toString()); //##Debug.

        _self.commands[data[0].toString()](data.slice(1));
    }

    didReceiveBleData(data) {
        //##Implement:
        // console.log("didReceiveBleData: " + data); //##Debug.
    }

    //Commands:
    getVersion(data) {
        //##Future: Implement.
        console.log("getVersion:"); //##Debug.
    }

    startScanning(data) {
        var payLoadLen = _self._getPayLoadLen(data.slice(0, 2));
        let uuidsQuantity = payLoadLen/_self.uuidLen; //If div by 0 throws an exception.
        let firstUuidIndex = 2;

        //console.log("uuidsQuantity: " + uuidsQuantity); //##Debug.
        let uuids = []; //##
        for (let i in [...Array(uuidsQuantity).keys()]) {
            let start = i*_self.uuidLen + firstUuidIndex;
            uuids.push(data.slice(start, start + _self.uuidLen));
        }
        //console.log("uudis: " + uuids); //##Debug.

        bleManager.startScanning(uuids);
    }

    stopScanning(data) {
        bleManager.stopScanning();
    }

    _getDeviceId(data) {
        let deviceIdIndex = 2
        return data.slice(deviceIdIndex, deviceIdIndex + _self.uuidLen);
    }

    connectDevice(data) {
        bleManager.connectDevice(_self._getDeviceId(data));
    }

    disconnectDevice(data) {
        bleManager.connectDevice(_self._getDeviceId(data));
    }

    startTx(data) {
        bleManager.startTx();
    }

    stopTx(data) {
        bleManager.stopTx();
    }

    write(data) {
        let deviceIdIndex = 2;
        let serviceIdIndex = deviceIdIndex + _self.uuidLen;
        let characteristicIdIndex = serviceIdIndex + _self.uuidLen;
        let payLoadIndex = characteristicIdIndex + _self.uuidLen;
        //Not used by now:
        //var payLoadLen = _self._getPayLoadLen(data.slice(0, 2));

        let deviceId = data.slice(deviceIdIndex, serviceIdIndex).toString('utf8');
        let serviceId = data.slice(serviceIdIndex, characteristicIdIndex).toString('utf8')
        let characteristicId = data.slice(characteristicIdIndex, payLoadIndex).toString('utf8')
        let payLoad = data.slice(payLoadIndex)

        bleManager.write(deviceId, serviceId, characteristicId, payLoad);

        //##Delete ALL this stuff:
        console.log("Tx:");
        console.log(payLoad);
        if (chTx !== null) {
            chTx.write(payLoad);
        }
    }

    /* Sets a command to be sent to a given device, service and charactestic once the
    client owning that devices disconnects. This allows for example, to stop a robot
    that is connected through BLE under the command of an application via sockets. */
    setClientDisconnectionCmd(data) {
        //##Implement.
    }
}

//##Experiment: Evaluate if this goes into a different file, making the BleSocketServer
//an exported class (or singleton? If so, the constructor should be improved to allow
//deferred server creation on a port selected by the user):
var svr = new BleSocketServer(44199);

//////////////////////////////////////////////////////////////////////////////////////////////
//##This is just a quick test, so from here, everything MUST BE CONVERTED TO WRAPI CLASSES:
//////////////////////////////////////////////////////////////////////////////////////////////

//##:
// From Daniel's file:
const uuidRoot = '48c5d828ac2a442d97a30c9822b04979';
const uuidSerial = '6e400001b5a3f393e0a9e50e24dcca9e';
const uuidTx = '6e400002b5a3f393e0a9e50e24dcca9e';
const uuidRx = '6e400003b5a3f393e0a9e50e24dcca9e';


//////////////////////////////////////////////////////////////////
var chTx = null;

var TxChannel = function(channel, server) {
    this.chTx = channel;

    //##Important: This is just the response indicating that the characteristic was written, NOT that the command has been completed:
    //chTx.once('write', function() { //Don't delete: useful for the future.
    this.chTx.on('write', function() {
        //##console.log('written!');

        //##7:
        let strToSend =  Buffer([server.ansCanWrite]).toString('hex')
        //server._socketServer.write(new Buffer([server.ansCanWrite]).toString('hex'));
        server._socketServer.write(strToSend);
        // console.log('Socket data: ' + strToSend); //##Debug.
    });
    console.log("txChannel initialized.");
}

TxChannel.prototype.write = function(buffer) {
    this.chTx.write(buffer, false);
}

//////////////////////////////////////////////////////////////////
var noble = require('noble'); //##Delete.

noble.on('stateChange', function(state) {
    if (state === 'poweredOn') {
        noble.startScanning([uuidRoot], false);
        console.log('Scanning for robots...');
    } else {
        noble.stopScanning();
        console.log('stop scanning');
    }
});

noble.on('discover', function(peripheral) {
    console.log('------------------------------------------------------------');
    console.log('peripheral discovered (' + peripheral.id +
                ' with address <' + peripheral.address +  ', ' + peripheral.addressType + '>,' +
                ' connectable ' + peripheral.connectable + ',' +
                ' RSSI ' + peripheral.rssi + ':');
    console.log('Local name: ' + + peripheral.advertisement.localName);
    console.log('Advertised services:');
    console.log('\t' + JSON.stringify(peripheral.advertisement.serviceUuids));
    console.log('');

    peripheral.connect(function(err) {
        //console.log(err);
        noble.stopScanning() //##Once it connects to a robot, it stops scanning.
        peripheral.discoverServices([uuidSerial], function(error, services) {
            //console.log(services);
            for (var i in services) {
                //console.log('service: ' + services[0]); //##Debug.
                var service = services[i];
                if (service.hasOwnProperty('uuid')) {
                    if (service.uuid === uuidSerial) {
                        //console.log('serialId = ' + service.uuid); //##Debug.
                        console.log('Serial found.');
                        //console.log(service);
                        service.discoverCharacteristics([uuidTx, uuidRx], function(error, characteristics) {
                            //##Save Tx characteristic.

                            for (var j in characteristics) {
                                //console.log('j = ' + j); //##Debug.
                                if (characteristics[j].uuid === uuidTx) {
                                    console.log('Tx found.');
                                    chTx = new TxChannel(characteristics[j], svr);
                                }
                                else if (characteristics[j].uuid === uuidRx) {
                                    console.log('Rx found.');
                                    //##Register Rx event and associate it with the Rx characteristic:
                                    var chRx = characteristics[j];
                                    chRx.notify(true, function(error) { //Don't forget this!
                                        //##console.log(error);
                                    });
                                    chRx.on('data', function(data, isNotification) {
                                        // ##This will be part of the debug mode in the future:
                                        //console.log('Rx: ' + data.toString('hex')); //##Debug.
                                        let strToSend = svr.ansData.toString(16) + data.toString('hex')
                                        //console.log('Socket: ' + strToSend); //##Debug.

                                        //console.log(data); //##Debug.
                                        //##Try to send more commands here:
                                        if (chTx !== null) {
                                            if (svr !== null) {
                                                //##7:svr._socketServer.write(data.toString('hex'));
                                                //svr._socketServer.write(data.toString('hex'));
                                                //console.log([svr.ansData].concat(data)).toString('hex'));
                                                svr._socketServer.write(strToSend);
                                            }
                                        }
                                    });
                                }
                            }
                        });
                    }
                }
            }
        });
    });
});
