"use strict";

const _ = require("lodash");

const path = require("path");
const merapi = require("merapi");
const yaml = require("js-yaml");
const fs = require("fs");

const config = yaml.load(fs.readFileSync("./service.yml", "utf8"));
config.package = require("./package");

const plugins = yaml.load(fs.readFileSync("./plugin.yml", "utf8"));
const env = process.env.PLUGIN_ENV || "platform";

const pluginConf = plugins && plugins[env];
if (pluginConf) {
    if (pluginConf.include)
        config.plugins = _.union(config.plugins, pluginConf.include);
    if (pluginConf.exclude)
        config.plugins = _.without(config.plugins, ...pluginConf.exclude);
}

module.exports = merapi({
    basepath: path.resolve(__dirname, "lib"),
    config: config,
    delimiters: { left: "${", right: "}" }
});
