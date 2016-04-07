"use strict";


/*
 * Because the count stored in the server is not always updated by the next time
 * the count is requested, we keep track of the number of times we unexpectedly
 * receive a count that is too low. If the maximum number of retries is hit, we
 * accept that our count is bad, and start using the server's lower count value.
 */
var MAX_RETRIES = 3;
var localCount;
var retries;

$(function() {
    localCount = 0;
    retries = 0;

    $("#like").click(incrementCount);
    setInterval(getCount, 1000);
});

function incrementCount() {
    $.post("/count",
        {},
        function(data, status) {
            updateCount(data.count);
        });
}

function getCount() {
    $.get("/count",
        function(data, status) {
            updateCount(data.count);
        })
}

function updateCount(count) {
    if (count || count === 0) {
        if (localCount <= count) {
            localCount = count;
            retries = 0;
        }
        else if (retries >= MAX_RETRIES) {
            console.log("Local count was bad for too long. Using server's count.");
            localCount = count
            retries = 0;
        }
        else {
            ++retries;
            console.log(retries + "/" + MAX_RETRIES + " Local count is too high.");
            count = localCount;
        }
        $("#numLikes").text(count);
    }
    else {
        console.log("Recieved an invalid count from the server.");
    }
}
