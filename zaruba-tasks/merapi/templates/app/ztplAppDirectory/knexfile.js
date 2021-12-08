"use strict";
const yaml = require("js-yaml");
const fs = require("fs");
const { Config } = require("merapi");

const yamlConfig = yaml.load(fs.readFileSync("./service.yml", "utf8"));

let config = Config.create(yamlConfig, { left: "${", right: "}" });
Object.keys(process.env).forEach(key => {
    config.set("ENV." + key, process.env[key]);
    config.set("$" + key, process.env[key]);
});
config.resolve();

module.exports = config.get("stores.knex");
