"""
Kritagya Sharma
Description: This program checks tweets to figure out if they are positive, negative, or neutral. It uses keywords and scores, cleans up the text, and creates a report with simple information such as average sentiment and the number of tweets.

"""
# The purpose of this function is that it reads the keywords and their sentiment score from a file and returns it to a dictionary.
# The parameter used in the function is keyword_file_name which is a file that stores the keywords and sentiment score of each keyword.
# The return values that would be returned from this is dictionary of keywords.

def read_keywords(keyword_file_name):
    try:
        keyword_dict = {} 
        with open (keyword_file_name,'r') as file:  
            for line in file:
                keywordList = line.strip().split("\t") # Converts contents from the file into a list.
                sentiment_word = keywordList[0]
                sentiment_num = int(keywordList[1]) # the 0th value of keyword_list = word, and 1st value of keyword_list will be the sentiment score
                keyword_dict[sentiment_word] = sentiment_num 
           
        
    except IOError:
        print(f"Could not open file {keyword_file_name}" )
    finally:
         return keyword_dict



# The Purpose of this function is that it cleans all of the punctuation characters from tweet text and also make it all lowercase.
# The parameter used in this function was tweet_text and this represents the tweet that we will be cleaning the punctuation from.
# The return value in this case would be a tweet that has all of it's punctuation and numbers removed from it, and also would convert the tweet to lower case.

def clean_tweet_text(tweet_text):
    punc_chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~1234567890"
    for punc in punc_chars:
        if punc in tweet_text:
            tweet_text = tweet_text.replace(punc,"")
    return tweet_text.lower()

        
# The purpose of this function is to calculate the sentiment score of a the tweets based on the amount of keywords it contains.
# The first parameter used in this function is tweet_text, which is just the tweet that we would in this case want to calculate the sentiment score from, and it also uses another parameter called keyword_dict which is the dictionary of all the keywords and their sentiment score.
# This function would return the total sentiment for each tweet in the file attached.

def calc_sentiment(tweet_text, keyword_dict): 
    total_score = 0 
    for keyword in keyword_dict: 
        words = tweet_text.split(' ')
        if keyword in words: 
            keyword_count = tweet_text.count(keyword)
            total_score = total_score + (keyword_count * keyword_dict[keyword])  # Adding the 1st index value to Total Score. 
    return total_score


# The purpose of this function is to classify the sentiment score based on if it is positive negitave or neutral.
# The paraneter used in this function is "score" which represents the sentiment score of a tweet.
# The return values in this function would be either 'positive' , 'negitave' or 'neutral'.

def classify(score):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    elif score == 0:
        return "neutral"


# The purpose of this function is to read the tweet and put each part into a dictionary.
# The parameter used in this function is tweet_file_name and this is just the file that has all the tweet information.
# The value returned in this is a big list of dictionaries with the tweet information.

def read_tweets(tweet_file_name):
    try:
        tweets_list = []
        one_tweet_info = {}        
        with open (tweet_file_name,'r') as file:
            for line in file:
                tweet_info = line.split(",") # Splitting into a list whenever there is a comma.
                one_tweet_info = { 
                    'date': tweet_info[0],  # Ok so these [0],[1],[2] etc are bascially indexed in the "tweetList" that has all the info for the tweet and they will always be in the same format so we can use index to specify everything
                    'text': clean_tweet_text(tweet_info[1]),  # Cleaning the text as we are calling the clean_tweet function on tweet_info at index 1, which is just a bunch of text (since the 0th value is just numbers).
                    'user': tweet_info[2],
                    'retweet': int(tweet_info[3]),
                    'favorite': int(tweet_info[4]),
                    'lang': tweet_info[5],
                    'country': tweet_info[6],
                    'state': tweet_info[7],
                    'city': tweet_info[8]
                                        }

                try:
                    one_tweet_info['lat'] = float(tweet_info[9]) # The 'lat' is creating a new key; basically, this line is adding 'lat' to the dictionary.
                except ValueError:
                    one_tweet_info['lat'] = 'NULL'

                try:
                    one_tweet_info['lon'] = float(tweet_info[10])
                except ValueError:
                    one_tweet_info['lon'] = 'NULL'

                sorted_list = dict(sorted(one_tweet_info.items())) # the one_tweet_info.items will sort all the key and values by alphabetical value from the key value
            
                tweets_list.append(sorted_list)
    except IOError:
        print(f"Could not open file {tweet_file_name}")
    finally:
        return tweets_list 


# The purpose of this function is that it generates a report based on the tweet information and keyword sentiment scores.
# The first parameter in this function is tweet_list which is a list of dictionaries with the information of each tweet.
# The second parameter in this function is keyword_dict and this is just a dictionary of the keywords and their sentiment scores.
# The return value in this case would be a dictionary of the all of the varaibles we calculated.

def make_report(tweet_list, keyword_dict):

    num_tweets = len(tweet_list) # Counts the num of tweets from the list of tweets
    num_favorite = 0
    num_retweet = 0
    total_sentiment = 0 # Total sentiment of all the tweets
    num_negative = 0
    num_neutral = 0
    num_positive = 0
    total_fav_sentiment = 0
    total_retweet_sentiment = 0
    country_sentiment = {} # Dictionary of total sentiment for each country
    country_count = {}

    for tweet in tweet_list:
        tweet_sentiment = calc_sentiment(tweet['text'], keyword_dict) # This is just calculating sentiment value of the tweet
        total_sentiment = total_sentiment + tweet_sentiment 


        # Determine which tweets sentiments are Posivite Negitave or Neutral
        if classify(tweet_sentiment) == 'positive':
            num_positive = num_positive + 1
        elif classify(tweet_sentiment) == "negative":
            num_negative = num_negative + 1
        elif classify(tweet_sentiment) == "neutral":
            num_neutral = num_neutral + 1


        # Count favorites and retweets
        if tweet['favorite'] > 0:
            num_favorite = num_favorite + 1
        if tweet['retweet'] > 0:
            num_retweet = num_retweet + 1


        # The total sentiment for each country
        tweet_country = tweet['country'] 
        if tweet_country in country_sentiment and tweet_country != 'NULL': 
            country_sentiment[tweet_country] = country_sentiment[tweet_country] + tweet_sentiment
            country_count[tweet_country] += 1
        elif tweet_country not in country_sentiment and tweet_country != 'NULL': 
            country_sentiment[tweet_country] = tweet_sentiment # So if the country is not in list, we add that new country in the dictionary so a key value pair to dictionary.
            country_count[tweet_country] = 1

        # Calculating the total sentiment score of Favourited and Retweeted Tweets
        if tweet['favorite'] > 0:
            total_fav_sentiment = total_fav_sentiment + tweet_sentiment
        if tweet['retweet'] > 0:
            total_retweet_sentiment = total_retweet_sentiment + tweet_sentiment



    # This segment calculates all of the averages
    if num_tweets > 0: 
        avg_sentiment = total_sentiment / num_tweets
    else:
        avg_sentiment = "NAN"

    
    if num_favorite > 0:
        avg_favorite = total_fav_sentiment / num_favorite
    else:
        avg_favorite = "NAN"

    
    if num_retweet > 0:
        avg_retweet = total_retweet_sentiment / num_retweet
    else:
        avg_retweet = "NAN"

        

    # Calculating Average Sentiment For Each Country
    for country in country_sentiment:
        country_sentiment[country] = country_sentiment[country]/country_count[country]
    count = 1
    string_top_five_list = ''
    top_five_list = sorted(country_sentiment.items(), key=lambda item: item[1], reverse=True)
    for country in top_five_list:
        if count != 5 and len(top_five_list) != (top_five_list.index(country) + 1):
            string_top_five_list += country[0] + ', '
            count += 1
        else:
            string_top_five_list += country[0]
            break

    
    report = {
        'avg_favorite': round(avg_favorite, 2),
        'avg_retweet': round(avg_retweet, 2),
        'avg_sentiment': round(avg_sentiment,2),
        'num_favorite': num_favorite,
        'num_negative': num_negative,
        'num_neutral': num_neutral,
        'num_positive': num_positive,
        'num_retweet': num_retweet,
        'num_tweets': num_tweets,
        'top_five': string_top_five_list
    } 
    return report


# The purpose of this function is to take all of the calculated values in the make report function, and write it to a file called output file.
# The first parameter in this function is "report" which comes from the return of "make_report"
# The second parameter in this function is "output_file" which is the file that we will be placing out report in.
# There will be no values returned in this function, since we are just writing to a file.

def write_report(report, output_file):

    try:
        with open(output_file,'w') as file:
            file.write(f"Average sentiment of all tweets: {report['avg_sentiment']}\n")
            file.write(f"Total number of tweets: {report['num_tweets']}\n")
            file.write(f"Number of positive tweets: {report['num_positive']}\n")
            file.write(f"Number of negative tweets: {report['num_negative']}\n")
            file.write(f"Number of neutral tweets: {report['num_neutral']}\n")
            file.write(f"Number of favorited tweets: {report['num_favorite']}\n")
            file.write(f"Average sentiment of favorited tweets: {report['avg_favorite']}\n")
            file.write(f"Number of retweeted tweets: {report['num_retweet']}\n")
            file.write(f"Average sentiment of retweeted tweets: {report['avg_retweet']}\n")
            file.write(f"Top five countries by average sentiment: {report['top_five']}\n")
        print(f"Wrote report to {output_file}")
    except IOError:
        print(f"Could not open file {output_file}")



            
 
 




   
    





