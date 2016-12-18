# Book Rat
Find similar books based on content.
The python application uses postgresql and prolog custom prolog stemmer.
We've downloaded the Chitanka's database and analysed the stemmed words with tf-idf algorithm. 
After that we determine the top 300 words for every book.
Then we can recommend books as an answer to a query - the more common words they have in their top words with ours, 
the higher the score.