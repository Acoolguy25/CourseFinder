import download_csv
import download_electives
import util
import pandas as pd
import logging, itertools
import re
import math
settings_root = util.get_settings("core")
settings_download = settings_root["download"]
settings_electives = settings_root["electives"]
settings_merge = settings_root["merge"]
settings_sort = settings_root["sort"]

# Grade percentage columns
grade_cols = ["A+", "A", "A-", "B+", "B", "B-", 
                  "C+", "C", "C-", "D+", "D", "D-", "F"]

def merge_courses(group):
    total_students = group["num_students"].sum()

    # Weighted average GPA
    weighted_gpa = (group["avg_gpa"] * group["num_students"]).sum() / total_students

    

    # Convert percentages → counts, merge, then back to percentage
    grade_counts = {}
    for col in grade_cols:
        # some rows might have NaN
        counts = (group[col].fillna(0)) * group["num_students"]
        grade_counts[col] = counts.sum() / total_students

    return pd.Series({
        "num_students": total_students,
        "avg_gpa": weighted_gpa,
        **grade_counts
    })

def main():
    # if settings_download["use_saved"]:
    df: pd.DataFrame = download_csv.import_url()
    electives: list = download_electives.download_electives()
    for val in settings_electives["exclude_courses"]:
        if val in electives:
            electives.remove(val)
        else:
            logging.warning(f"Exclude Course {val} does not exist!")
    if settings_download["hide_unavailable_courses"]:
        df = df[df["teaching_next_semester"] != True]
    merged: pd.DataFrame = df.groupby("course").apply(merge_courses, include_groups=False).reset_index()
    merged.sort_values("course")
    merged["num_students"] = merged["num_students"].astype(int)
    merged["avg_gpa"] = merged["avg_gpa"].round(2)
    merged[grade_cols] = (merged[grade_cols] * 100).round(1)
    if settings_merge["save_all"]:
        download_csv.save_csv(merged, "all_courses")
    # download_csv.save_csv(merged, "temp")

    # Keep only rows where the prefix matches one in electives
    merged = merged[merged["course"].apply(
        lambda c: c.split(":")[0] in electives
    )]
    by_list = settings_sort["sort_columns"] # ["num_students", "avg_gpa"]
    if by_list:
        merged = merged.sort_values(
            by=by_list,  # columns to sort by
            ascending=list(itertools.repeat(False, len(by_list)))         # descending for all
        ).reset_index(drop=True)            # optional: reset index
    if settings_merge["save_merging_tech_electives"]:
        download_csv.save_csv(merged, "merged_tech_electives")


if __name__ == "__main__":
    main()