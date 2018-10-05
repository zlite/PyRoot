"use strict";

//Singleton pattern:
let packetHelper = new class {
    constructor() {
    }

    boolToByte(value) {
        return value === true ? 1 : 0;
    }

    nibbleToByte(value, nibbleIndex) {
        if (nibbleIndex === 0) {
            return value & 0xf;
        }
        else { //nibbleIndex === 1, but any value != 0 will work here.
            return (value >> 4) & 0xf;
        }
    }

    //Notes:
    //  -- Does not check if the integer is bigger than a 16 bits integer (given the fact that a JS number is a 64 bits float).
    //  -- result[0] is the MSB.
    int16ToByteArray(value) {
        return [(value >> 8) & 0xff, value & 0xff];
    }

    //Notes:
    //  -- All the notes for int16ToByteArray apply to this function.
    //  -- If the number is signed, this just discards ths sign by calling Math.abs.
    uint16ToByteArray(value) {
        return int16ToByteArray(Math.abs(value));
    }

    //Notes:
    //  -- Works for 32 bits but obviously loses decimals on floats.
    //  -- Does not check if the integer is bigger than a 32 bits integer (given the fact that a JS number is a 64 bits float).
    //  -- In the case of dealing with floats, it rounds.
    //  -- result[0] is the MSB.
    int32ToByteArray(value) {
        let intValue = Math.round(value);
        let result = [0, 0, 0, 0]
        result[0] = (intValue >> 24) & 0xff;
        result[1] = (intValue >> 16) & 0xff;
        result[2] = (intValue >> 8) & 0xff;
        result[3] = intValue & 0xff;

        return result;
    }

    //Notes:
    //  -- All the notes for int32ToByteArray apply to this function.
    //  -- If the number is signed, this just discards ths sign by calling Math.abs.
    uint32ToByteArray(value) {
        return int32ToByteArray(Math.abs(value));
    }

    //Notes:
    //  -- Works for 32 bits but obviously loses decimals on floats.
    //  -- Does not check if the integer is bigger than a 32 bits integer (given the fact that a JS number is a 64 bits float).
    //  -- In the case of dealing with floats, it rounds.
    //  -- result[0] is the MSB.
    byteArrayToInt32(value) {
        let result = (value[0] & 0xff) << 24;
        result |= (value[1] & 0xff) << 16;
        result |= (value[2] & 0xff)<< 8;
        result |= value[3] & 0xff;

        return result;
    }

    getArrayFilledWithZeroes(size) {
        return new Array(size).fill(0);
    }

    fillMessageDataWithZeroes(message, payloadSize) {
        return message.concat(this.getArrayFilledWithZeroes(payloadSize - message.length + 1));
    }

    //##Not implemented yet:
    modularSum(value) {
        return 0;
    }

    //This is just an alias function, so in the future the checksum algorithm can be easily changed just by passing another
    //block as an argument (or even editing the default value here, WHICH IS NOT RECOMENDED):
    computeChecksum(data, checksumFunction = this.modularSum ) {
        return checksumFunction(data);
    }
}

exports = module.exports = packetHelper;

//Examples:
/*
console.log(packetHelper.boolToByte(true));
console.log(packetHelper.boolToByte(false));
//console.log(packetHelper.boolToByte(0));

console.log(packetHelper.nibbleToByte(0xab, 0));
console.log(packetHelper.nibbleToByte(0xab, 1));
console.log(packetHelper.nibbleToByte(0xf2, 0));
console.log(packetHelper.nibbleToByte(0xf2, 1));

console.log(packetHelper.int32ToByteArray(100));
console.log(packetHelper.int32ToByteArray(2100));
console.log(packetHelper.int32ToByteArray(2100)[0]);
console.log(packetHelper.int32ToByteArray(2100)[3]);
console.log(packetHelper.int32ToByteArray(-2100));

console.log(packetHelper.int32ToByteArray(-999.49));
console.log(packetHelper.int32ToByteArray(-999.5)); //Slightly different in Python version of the API.
console.log(packetHelper.int32ToByteArray(-999.5001));

console.log(packetHelper.byteArrayToInt32(packetHelper.int32ToByteArray(999.5)));
//console.log(packetHelper.byteArrayToInt32(packetHelper.int16ToByteArray(999.5))); //Must fail.

console.log(packetHelper.int16ToByteArray(30123));
console.log(packetHelper.int16ToByteArray(-30123));


let message = [1, 2, 3];
console.log(packetHelper.fillMessageDataWithZeroes(message, 10));

//##Not implemented yet:
//console.log(packetHelper.computeChecksum(packetHelper.int32ToByteArray(0)));
//console.log(packetHelper.computeChecksum(packetHelper.int32ToByteArray(-999)));
//console.log(packetHelper.computeChecksum(packetHelper.int32ToByteArray(-1)));
//console.log(packetHelper.computeChecksum(packetHelper.int32ToByteArray(100)));
*/
