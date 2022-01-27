import pandas as pd
from pandasql import sqldf

def read_file(file):
    df = pd.read_csv(file, index_col=None)
    return df

def best_match(df_mentee, df_mentor):
    df_first = df_mentee.merge(df_mentor, how="left", left_on="first", right_on="mentor_name")
    # df_best_first = df_first.groupby("first").agg({"first":{"first_count":"count"}}).reset_index()

    # print(df_best_first)
    # print(df_best_first.loc[df_best_first["first"]["first_count"] == 1])
    # df_best_first = df_best_first.loc[df_best_first["first"]["first_count"] == 1]
    # df_best = pd.merge(df_first, df_best_first, on=["first"], how="inner")
    # print(df_best)
    df_first["first_count"] = df_first.groupby("first")["name"].transform("count")
    print(df_first.loc[df_first["first_count"]==1])
    
    #To fetch one of the mentee, based on mentor's first.
    df_ambiguious_first = df_first.loc[df_first["first_count"]>=1]
    df_2 = df_mentor.merge(df_ambiguious_first, how="left", left_on="mentors_first", right_on="name")
    print(df_2.columns)
    df_2["mentors_first_count"] = df_2.groupby("mentors_first_x")["mentor_name_x"].transform("count")
    print(df_2.loc[df_2["mentors_first_count"]==1])
    # mysql = lambda q: sqldf(q, globals())
    # df_best = mysql("select first, count(first) from df_mentee left outer join df_mentor where first==mentor_name group by first")
    # print(df_best)

def main():
    df_mentee = read_file("/Users/ruksvaithy/Projects/twm_matchmaking/datasets/sample_mentee.csv")
    print(df_mentee)
    df_mentor = read_file("/Users/ruksvaithy/Projects/twm_matchmaking/datasets/sample_mentor.csv")
    print(df_mentor)
    best_match(df_mentee, df_mentor)

if __name__ == "__main__":
    main()