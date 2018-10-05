"use strict";

var noble = require('noble');

//Singleton pattern:
let bleManager = new class {
    constructor() {
    }

    //Rx callback:
    didReceiveData() {
        //This is a user's callback function, so here it does nothing.
    }

    //Commands:
    startScanning(uuids) {
        console.log("startScanning:" + uuids); //##Debug.
    }

    stopScanning() {
        //##Implement.
        console.log("stopScanning:"); //##Debug.
    }

    connectDevice(deviceId) {
        //##Implement.
        console.log("connectDevice:" + deviceId); //##Debug.
    }

    disconnectDevice(deviceId) {
        //##Implement.
        console.log("disconnectDevice:" + deviceId); //##Debug.
    }

    startTx() {
        //##Implement.
        console.log("startTx:"); //##Debug.
    }

    stopTx() {
        //##Implement.
        console.log("stopTx:"); //##Debug.
    }

    write(deviceId, serviceId, characteristicId, data) {
        //##Implement.
        /*
        console.log("write:"); //##Debug.
        console.log('DevId: ' + deviceId); //##Debug.
        console.log('SvcId: ' + serviceId); //##Debug.
        console.log('ChrId: ' + characteristicId); //##Debug.
        console.log(data); //##Debug.
        */
    }
}

exports = module.exports = bleManager;
