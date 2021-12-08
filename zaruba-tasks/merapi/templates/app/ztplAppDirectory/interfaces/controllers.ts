import * as express from "express";

export interface ISampleController {
    hello(request: express.Request, response: express.Response, next: express.NextFunction): Promise<void>;
}