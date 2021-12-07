import { Component, IConfig, ILogger, JsonObject } from "merapi";

export default class SampleController extends Component {
    constructor(
        private logger: ILogger,
        private config: IConfig,
        private sampleManager: Component,
    ){
        super();
    }

    public async hello(name?: string): Promise<string> {
        return Promise.resolve(`hello ${name}`);
    }

}