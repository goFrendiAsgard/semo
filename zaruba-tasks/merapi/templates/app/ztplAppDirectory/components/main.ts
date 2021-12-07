import { Component, IConfig, ILogger } from "merapi";

export default class Main extends Component {
    constructor(
        private logger: ILogger,
        private config: IConfig
    ){
        super();
    }

    public async start() {
        // TODO: initiate your kafka/redis, or any other listeners here
    }
}
