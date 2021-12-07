"use strict";

// This line must come before importing any instrumented module.
const tracer = require('dd-trace').init()

tracer.init({
  analytics: true
})

let boot = require("./index.js");

try {
    boot.start();
}
catch (e) {
    console.log(e.stack);
    process.exit();
}
