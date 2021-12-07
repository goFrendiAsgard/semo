export interface ISampleManager {
    hello(name?: string): Promise<string>;
}