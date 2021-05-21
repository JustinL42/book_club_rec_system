# book_club_rec_system
A recommendation system for book clubs using the book crossings data set

This repository was an exploratory effort to produce a list of recommendations for book club based on their past ratings of sci-fi / fantasy books, and also the ratings data from the public Book Crossings data set. I'm no longer adding to this repository, but am using the code as a prototype for web app collects ratings from users and will be able give recommendations to individual users and to book clubs (see rec_sys_app).

The etl.py script loads the book crossing data and the user data into a database. In order to focus the recommendations on sci-fi / fantasy, only ratings for books with ISBNs in the Internet Speculative Fiction Database are included. One of there publically released mysql databases must be installed to generate the set of valid ISBNS. 

After the data is loaded into the database, the predict.py script can be run. The parameterTuning.py script was developed to generate a model that was tuned to give good predictions for specifically for the book club users, and not for the book crossing data contributer who aren't as important.
