#!/bin/bash

page=0
while /bin/true; do
    for i in 1 2 3 4 5 6
    do
        for j in 0 1 2 3 4 5 6
        do
            key=$j;
            node ./fetch.js $page $key
            >&2 echo finished $page
            if [ $? -ne 0 ]
            then
                >&2 echo failed $page 
            fi
            page=$(($page + 10))
        done
    done
    sleep 24h
done
