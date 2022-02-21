from os import rename
import pandas as pd
from pandasql import sqldf

from settings import *

def read_file(file):
    df = pd.read_csv(file, index_col=None)
    return df

def drop_columns(df, columns_list):
    df_new = df.drop(columns_list, axis=1)
    return df_new

def rename_columns(df, columns_dict):
    df_rename = df.rename(columns=columns_dict)
    return df_rename

def union_df(df_list):
    df_union = pd.concat(df_list)
    return df_union

def new_mentee(df_mentee, df):
    df_new = df_mentee[df_mentee.name.isin(df.name) == False]
    return df_new

def new_mentor(df_mentor, df):
    df_new = df_mentor[df_mentor.mentor_name.isin(df.mentor) == False]
    return df_new 

def best_match(df_mentee, df_mentor):
    df_first = df_mentee.merge(df_mentor, how="left", left_on="first", right_on="mentor_name")

    # df_best_first = df_first.groupby("first").agg({"first":{"first_count":"count"}}).reset_index()

    # print(df_best_first)
    # print(df_best_first.loc[df_best_first["first"]["first_count"] == 1])
    # df_best_first = df_best_first.loc[df_best_first["first"]["first_count"] == 1]
    # df_best = pd.merge(df_first, df_best_first, on=["first"], how="inner")
    # print(df_best)

    df_first["first_count"] = df_first.groupby("first")["name"].transform("count")
    # print(df_first.loc[df_first["first_count"]==1])

    df_1 = df_first.loc[df_first["first_count"]==1]
    df_1 = df_1[["name", "first"]]
    df_1 = rename_columns(df_1, rename_1)
    print("df_1", df_1)
    # print(df_first.columns)

    #To fetch one of the mentee, based on mentor's first.
    df_ambiguious_first = df_first.loc[df_first["first_count"]>=1]
    df_mentor = new_mentor(df_mentor, df_1)
    print("df_mentor", df_mentor)
    df_2 = df_mentor.merge(df_ambiguious_first, how="left", left_on="mentors_first", right_on="name")
    print(df_2.columns)
    df_2["mentors_first_count"] = df_2.groupby("mentors_first_x")["mentor_name_x"].transform("count")
    print(df_2.loc[df_2["mentors_first_count"]==1])
    df_2 = df_2[["mentor_name_x", "mentors_first_x"]]
    df_2 = rename_columns(df_2, rename_2)
    print("df_2 columns", df_2.columns)
    print("df_2", df_2)
    # mysql = lambda q: sqldf(q, globals())
    # df_best = mysql("select first, count(first) from df_mentee left outer join df_mentor where first==mentor_name group by first")
    # print(df_best)

    df_union = union_df([df_1,df_2])
    print("df_union", df_union)

    df_new_mentee = new_mentee(df_mentee, df_union)
    print("df_new_mentee", df_new_mentee)

    print("df_mentor COLUMNS", df_mentor.columns)
    print("df_union COLUMNS", df_union.columns)
    df_new_mentor = new_mentor(df_mentor,df_union)
    print("df_new_mentor", df_new_mentor)

    if df_new_mentor.empty:
        df_human_intervention = df_new_mentee[["name"]].copy()
        df_human_intervention["mentor"] = "HI"
        df_final = union_df([df_1,df_2,df_human_intervention])
        print(df_final)
        exit()
    
    df_second = df_new_mentee.merge(df_new_mentor, how="left", left_on="second", right_on="mentor_name")
    df_second["second_count"] = df_second.groupby("second")["name"].transform("count")
    print(df_second.loc[df_second["second_count"]==1])

    df_3 = df_second.loc[df_second["second_count"]==1]
    df_3 = df_3[["name", "second"]]
    df_3 = rename_columns(df_3, rename_3)
    print(df_second.columns)

    #To fetch one of the mentee, based on mentor's first.
    df_ambiguious_second = df_second.loc[df_second["second_count"]>=1]
    df_new_mentor = new_mentor(df_new_mentor, union_df([df_1,df_2,df_3]))
    df_4 = df_new_mentor.merge(df_ambiguious_second, how="left", left_on="mentors_first", right_on="name")
    print(df_4.columns)
    df_4["mentors_second_count"] = df_4.groupby("mentors_first_x")["mentor_name_x"].transform("count")
    print(df_4.loc[df_4["mentors_second_count"]==1])
    df_4 = df_4[["mentor_name_x", "mentors_first_x"]]
    df_4 = rename_columns(df_4, rename_2)
    print("df_4 columns", df_4.columns)
    # mysql = lambda q: sqldf(q, globals())
    # df_best = mysql("select first, count(first) from df_mentee left outer join df_mentor where first==mentor_name group by first")
    # print(df_best)

    df_final = union_df([df_1, df_2, df_3, df_4])
    print("df_final",df_final)




def main():
    df_mentee = read_file("/Users/ruksvaithy/Projects/twm_matchmaking/datasets/sample_mentee.csv")
    print(df_mentee)
    df_mentor = read_file("/Users/ruksvaithy/Projects/twm_matchmaking/datasets/sample_mentor.csv")
    print(df_mentor)
    best_match(df_mentee, df_mentor)

if __name__ == "__main__":
    main()