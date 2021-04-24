const fs = require('fs')

let tweets = require('./index.js')

console.log(tweets[0].tweet.full_text)

tweets.forEach((item) => {
    fs.appendFile('tweets.txt', ` ${item.tweet.full_text}`, (err => {
        if(err) throw err
    }))
    fs.appendFile('tweets.txt', ' ')
})