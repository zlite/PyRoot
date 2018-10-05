"use strict";

//##Finish this class:
//Singleton pattern:
let paramsHelper = new class {
    constructor() {
    }

    verify(value, dataType) {
        return value !== undefined && (typeof value === dataType);
    }

    //##Test this function to validate constraints, at least on numeric parameters:
    //##Think about this kind of validation for other parameter types too:
    verifyNumber(value, min, max) {
        if (verify(value, 'number') && verify(min, 'number') && verify(max, 'number')) {
            return min <= value && value <= max;
        }
        return false;
    }
}

exports = module.exports = paramsHelper;
