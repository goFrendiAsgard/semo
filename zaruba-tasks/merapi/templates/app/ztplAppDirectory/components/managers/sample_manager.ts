import { Component, IConfig, ILogger, JsonObject } from 'merapi';
import { ISampleManager } from 'interfaces/managers';

export default class SampleManager extends Component implements ISampleManager {
    constructor(
        private logger: ILogger,
        private config: IConfig
    ){
        super();
    }

    public async hello(name?: string): Promise<string> {
        const greetingName = name || 'world';
        return `hello ${greetingName}`;
    }

}