"""
Kritagya Sharma
Description: This program asks the user for tweets and details about them. After analyzing the tweets, it creates a simple report and saves the results in a text file chosen by the user.

"""

# Import the sentiment_analysis module
from sentiment_analysis import *

# This program prompts the user for the names of three files: one for keywords, one for tweets, and one for the report. It checks if the file types are right, then looks at the overall sentiment of  the tweets by looking for specific words, and writes a report to the chosen file.

def main():

	keyword_file_name = input("Input keyword filename (.tsv file): ")
	if not keyword_file_name.endswith(".tsv"):
		raise Exception("Must have a tsv file extension!")

	tweet_file_name = input("Input tweet filename (.csv file): ")
	if not tweet_file_name.endswith(".csv"):
		raise Exception("Must have a csv file extension!")

	report_file_name = input("Input filename to output report in (.txt file): ")
	if not report_file_name.endswith(".txt"):
		raise Exception ("Must have a txt file extension!")

	

	if len (read_tweets(tweet_file_name)) != 0 and len(read_keywords(keyword_file_name)) != 0:
		write_report(make_report(read_tweets(tweet_file_name),read_keywords(keyword_file_name)), report_file_name)
	else:
		raise Exception("Tweet list or keyword dictionary is empty!")


main()

