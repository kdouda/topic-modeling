# LDA on Novinky.cz data corpus

This is an attempt for a topic model based on the corpus of Novinky.cz news articles (no news article contents are provided in this repository).

Basic process diagram is as follows:
* find as many links to news articles,
* scrape the content of individual news articles,
* sentence split, tokenize, lemmatize, remove stop words,
* save lemmatized document into a database,
* after the data collection phase is finished, train an LDA model on the database, save it to a file along with its id2word dictionary,
* optimize the LDA model with available metrics (u_mass, c_v),
* classify all the training documents, try to find some labels for the topics,
* classify new documents from other sources, ideally documents that are not similar to the training documents.

An LDA-based topic model was developed which shows promise for news articles from other sources, but shows considerable bias towards health-related topics due to the time period in which the model was developed.

Nevertheless, the model provides very good results for news articles and may be developed further as a web application that allows users to conduct a document search for articles with similar content.

This repository also contains a practical example of using MorphoDiTa for lemmatization of Czech documents.

## Running the model

to be added

run import.py to scrape all articles starting with a certain ID (last id in the import file is from roughly September 2020 - adjust this!)

run train.py to create a model from the corpus of lemmatized documents (beware, this WILL overwrite the last model in models directory)

run test.py to classify new documents provided as plain text files (UTF-8 encoded) in test directory

## Code quality

As this was developed as a semestral project, no substantial amount of time was dedicated to the quality of the code after a certain period of time. This code does not follow many principles of good code. Regarding the access token to the MongoDB database - this should not be an issue, as the database is whitelisted to only allow one IP.