# Twitter Parody Bot Using Python and AWS Lambda

I made a twitter bot based on my twitter-active comedian girlfriend. You can checkout and follow the bot (lovingly known as "anabot") [here](https://twitter.com/ana40624883).

Most of this code was written with the help of @DylanJCastillo and his tutorial [How to Make a Twitter Bot Using Python and AWS Lambda](https://dylancastillo.co/how-to-make-a-twitter-bot-for-free/). I'll walk through how I incorporated markov chains and personal twitter data to make my bot sound just like Ana.

# Get the tweets!

Before we get started making the bot, you'll need to download whoever you're trying to replicate's entire twitter history. You can only download your own entire twitter history, so it helps to be personally very close to the person you're trying to clone. Thankfully, my girlfriend and I are pretty close.

Twitter will send you your entire tweet history in an absolutely enormous JSON file. You'll need to grab the text from each tweet and put them into a text file. You can do this with simple Javascript:

    const fs = require('fs')

    //the tweets JSON is in index.js
    let tweets = require('./index.js')

    tweets.forEach((item) => {
        fs.appendFile('tweets.txt', ` ${item.tweet.full_text}`, (err => {
            if(err) throw err
        }))
        fs.appendFile('tweets.txt', ' ')
    })

Now you'll have a file called "tweets.txt" that you can use as a corpus for a markov chain and produce pretty lifelike tweets. 

# Markovify

Ok, we're done with that little bit of Javascript. On to Python - you'll need a really neat Python library called [Markovify](https://github.com/jsvine/markovify)

In src/anabot you'll find simple code that takes "markovify's" the tweets.txt corpus we just created, and produces a sentence of max 280 characters:

    dirname = os.path.dirname(os.path.abspath(__file__))
    tweets = os.path.join(dirname, 'tweets.txt')

    with open(tweets) as f:
    text = f.read()

    class POSifiedText(markovify.Text):
        def word_split(self, sentence):
            words = re.split(self.word_split_pattern, sentence)
            words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
            return words

        def word_join(self, words):
            sentence = " ".join(word.split("::")[0] for word in words)
            return sentence

    text_model = markovify.Text(text)

    print(text_model.make_short_sentence(280))

This file doesn't actually do anything other than print a tweet,  but it was helpful to have for testing purposes and to understand what Markovify was capable of doing. Its helpful to also import the NLTK library (natural language toolkit) to help the markovify function produce more "realistic" sounding sentences.

# Now we make the Lambda function!

This is where @dylanjcastillo 's [incredible tutorial](https://dylancastillo.co/how-to-make-a-twitter-bot-for-free/) comes in handy. You're pretty much going to want to follow it from beginning to end - just make sure to have a basic understanding of Docker, AWS, and have a Twitter development account set up and ready to go.

What you'll want to change is the lambda_function.py file. This is the file that will be "triggered" and run while it's hosted on AWS Lambda - i.e., this is what will produce the tweet every 10 hours or whatever time you set it for. What I did was copy in my anabot.py code and adjust the get_tweet function to produce a tweet from the tweets.txt corpus. Just also make sure to import whatever necessary libraries (in my case, markovify and nltk), and add those libraries to the requirements.txt file as well.

# Deploy on AWS

Now you're going to run those handy scripts Dylan so kindly put together to create zip files of the lambda function, and a layer file for AWS. Upload your lamda_function.zip, layer.zip, add your Twitter developer account credentials, set up a trigger, and you're ready to go! 


