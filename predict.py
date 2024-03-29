#!/usr/bin/python3
import pandas as pd
from sqlalchemy import create_engine
from surprise import Dataset, Reader, SVD, KNNBasic, dump
from numpy import isnan

print("Connecting to db and loading data into memory...")
alchemyEngine = create_engine(
    'postgresql+psycopg2://postgres:@127.0.0.1/rec_system')
conn = alchemyEngine.connect()
ratings_df = pd.read_sql("""
    SELECT id, isbn, rating 
    FROM "ratings"
    """, conn)
books_df = pd.read_sql("""
    SELECT isbn, title, author, year 
    FROM "books"
    """, conn)
conn.close()

reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(ratings_df, reader)
train_set = data.build_full_trainset()

print("""   
    Number of ratings: {}\n
    Number of books: {}\n
    Number of users: {}\n""".format(
        len(ratings_df), 
        len(ratings_df['isbn'].unique()), 
        len(ratings_df['id'].unique())))

_, algo = dump.load("bestAlgo.pickle")
# algo = KNNBasic(verbose=True)
print("algo: {}".format(algo.__class__.__name__))
print("Fitting train_set")
algo.fit(train_set)


print("Getting test predictions")
selected_user = 500016
# selected_user = 500000
# selected_user = 600001
predictions = [(isbn, algo.predict(selected_user, isbn, clip=False).est) \
                for isbn in ratings_df['isbn'].unique()]
predictions_df = pd.DataFrame(predictions, 
    columns=['isbn', 'rating']).sort_values(by="rating", 
    ascending=False).merge(books_df, on='isbn', how='left')


def print_row(i, row):
    print("{}: {}".format(i + 1, row.title), end="")
    if ~isnan(row.year):
        print(" ({})".format(int(row.year)), end="")
    print("\nby {}   {}   {}\n".format(row.author, 
        row.isbn, round(row.rating, 2)))

top_x = 20
print("\nTop {}:".format(top_x))
for i, row in predictions_df.head(top_x).iterrows():
    print_row(i, row)

bottom_x = 5
print("\nBottom {}:".format(bottom_x))
for i, row in predictions_df.tail(bottom_x).iterrows():
    print_row(i, row)