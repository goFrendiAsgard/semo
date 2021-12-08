import {knex} from "knex";
import { IConfigReader } from "merapi";

export default async function(config: IConfigReader) {
    const client = knex(config.default("stores.knex", {}));
    // await client.migrate.latest();
    return client;
}
