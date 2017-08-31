/*
   Script search a list of keywords/phrases on the guardian website.
   Add all search strings to the query variable then run.
*/

usage = `usage:

    node fetch.js <current page> <key number>`

if (process.argv.length < 4) {
    console.log(usage);
    process.exit();
}
var page = process.argv[2];

var asyncs = require('async');
var fs = require('fs'); //filesystem support
var HtT = require('html-to-text');
var guardian = require('guardian-js'); //the guardian

keys = ['4fb7747f-c5a3-4786-a011-dda7371d2dda',
        '2b707819-62fd-49f2-b5d9-1cde76849d68',
        '8d020f80-9140-41b0-a45f-9c7ceb9e5ddf',
        '7cca4eb8-e3fa-493e-a920-73eec0641f6c',
        '0697243b-3870-4ccb-b46e-d730d1b077d8',
        '3609df25-f74b-4afb-97eb-22034920d337',
        '4cdf3199-38dc-40ce-b893-4f154e0bc4d6'];

let api = new guardian(keys[process.argv[3]], false); //API Key

var mysql = require('mysql'); //mysql
var connection = mysql.createConnection({
        host : '152.46.19.233',
        user : 'privacy',
        password : 'pr1vacyB0x',
        database : 'privacy'
});

//a place for storing all individual articles to query later
results_list = [];

query = ["cookie","data","information","privacy","advertising","google","web","internet","users","browser","website","technology"]; //put real queries here

//Start here
search_list(query);

//search a list
function search_list(queries) {
    num_pages = 0; //default
    page_size = 50; //max page size
    //for (var i = 0; i < queries.length; i++) {
        //first call to check how many pages are in each query
        api.special.search({'pageSize': page_size, 'from-date': '2015-3-20'})
            .then(function(response) {
                try {
                    body = JSON.parse(response.body);
                } catch (err) {
                    console.log("\nERROR \n" + response.body);
                    return;
                }
                if (body.message && body.message == "API rate limit exceeded") {
                    console.log("rate limit exceeded");
                    process.exit(-1);
                }
                num_pages = body.response.pages;
                search(page_size, num_pages/*, queries[i]*/);
            })
            .catch(function(error) {
                console.log(error);
                return;
            });
    //}
}

//search a key word
function search(page_size, num_pages, /*keyword,*/ options = {}) {
    //one request per page
    page_nums = [];
    for (var i = 0; i <= 9; i++){
        if (+page+i+1 > num_pages) break;
        page_nums[i] = +page + i + 1;
    }
    connection.connect();
    asyncs.each(page_nums,
        function(page_num, callback) {
            opctions = {};
            options['page-size'] = page_size;
            options['page'] = page_num;
            api.special.search(options) 
                .then(function(response) {
                try {
                    body = JSON.parse(response.body);
                } catch (err) {
                    console.log("\nERROR\n" + response.body);
                    return;
                }
                if (body.message && body.message == "API rate limit exceeded") {
                        console.log("rate limit reached");
                        process.exit();
                    }
                    results = parseResults(response);
                    if (results != undefined){
                        results_list = results_list.concat(results);
                    }
                    callback();
                })
                .catch(function(error) {
                    console.log(error);
                    callback(error);
                    return;
                });
        },
        function(err) {
            if (err){
                console.log("error");
            }
            check_ID(results_list);
        }
    );
}

//parse response for returned articles
//results is a list of articles
function parseResults(response) {
    try {
        body = JSON.parse(response.body);
    } catch (err) {
        console.log("\nERROR\n" + response.body);
    }
    resp = body.response;
    if (resp == undefined) return undefined; //if somethings invalid leave
    results = resp.results;
    if (results == undefined) return undefined; //if somethings invalid leave
    return results;
}

//get body text of ids from each item in results
function check_ID(results) {
    asyncs.each(results,
         function(result, cb){ //used to fix javascript scoping issues
         
            //Have we seen the id?
            //There is no reason to query twice. Given the async nature of js the checks will fail farely often anyway.
            //Rely on mySQL to catch it
            connection.query("INSERT INTO privacy.articles (ID) VALUES (?);", [result.id], function(error, response, fields) {
                if (error) {
                    console.log("duplicate");
                } else{
                    try {
                        make_individual_query(result, cb);
                        return;
                    } catch (error) {
                        console.log(error);
                        cb();
                        return;
                    }
                }
                cb();
                return;
            });
        },
        function(err) {
            process.exit();
        }
    );
}

async function make_individual_query(article_to_query, cb) {
    //Make query for specific article
    var response = await api.item.search(article_to_query.id, {'show-fields': 'body'});
    body = JSON.parse(response.body);
    if (body.message && body.message == "API rate limit exceeded") {
        console.log("rate limit reached");
        process.exit();
    }
    body_text = body.response.content
    body_text = body_text.fields.body;
    body_text = HtT.fromString(body_text); //remove HTML tags and unreadable elements
    id = body.response.content.id;
    section = body.response.content.sectionName;
    pubDate = body.response.content.webPublicationDate;
    title = body.response.content.webTitle;
    url = body.response.content.webUrl;
    //add article to database
    connection.query("UPDATE privacy.articles SET section=?, body=?, url=?, title=?, pub_date=? WHERE ID = ?", [section, body_text, url, title, pubDate, id], function(error, response, fields){
        if (error) console.log(error);
        cb();
    });
    return;
}

//adapted from http://stackoverflow.com/questions/14031763/doing-a-cleanup-action-just-before-node-js-exits
//Last thing before exit should be to sync the files
function exitHandler(options, err) {
        if (options.cleanup) {
        }
        connection.query("delete from privacy.articles where body is null", function(error, response, fields){
            if (error) console.log(error);
        });
        connection.end(); //kill mysql connection
}

//do something when program exits
process.on('exit', exitHandler.bind(null,{cleanup:true}));

//catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {cleanup:true}));
