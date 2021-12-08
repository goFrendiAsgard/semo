
import * as express from "express";
import { ISampleController } from "interfaces/controllers";
import { ISampleManager } from "interfaces/managers";
import { Component, IConfig, ILogger, JsonObject } from "merapi";

export default class SampleController extends Component implements ISampleController {
    constructor(
        private logger: ILogger,
        private config: IConfig,
        private sampleManager: ISampleManager,
    ){
        super();
    }

    public async hello(request: express.Request, response: express.Response, next: express.NextFunction): Promise<void>{
        try {
            const { name } = request.params;
            const helloResponse = await this.sampleManager.hello(name);
            response.status(200).json({
                status: 'ok',
                response: helloResponse
            });
        } catch(error) {
            this.logger.error(error);
            response.status(500).json({
                status: 'error',
                message: error.message
            });
        }
    }

}