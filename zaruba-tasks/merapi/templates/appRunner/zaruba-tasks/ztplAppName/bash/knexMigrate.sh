if [ -d "./migrations" ]
then
    if [ -f "node_modules/.bin/knex" ]
    then
        ./node_modules/.bin/knex migrate:latest
    else
        if [ "$(isCommandExist knex)" = 0 ]
        then
            npm install -g knex
        fi
        knex migrate:latest
    fi
fi