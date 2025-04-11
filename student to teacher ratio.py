# %%
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

# %% [markdown]
# ## Public School Teachers

# %%
excel_file = pd.ExcelFile("C:/Users/franj/notebooks/public school teachers/public school teachers.xlsx")

# Sheets you want to combine
sheet_names = excel_file.sheet_names

for sheet in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet)
    print(f"--- Sheet: {sheet} ---")
    print(df.head())
    print(df.head())
    print("\n")

# %%
df.shape

# %%
for sheet in sheet_names:
    df = pd.read_excel("C:/Users/franj/notebooks/public school teachers/public school teachers.xlsx", sheet_name=sheet)
    print(f"{sheet}: {df.shape[0]} rows × {df.shape[1]} columns")

# %%
df_list = []

# Loop and add "Level" column to each
for sheet in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df['Level'] = sheet  # Add sheet name as a column
    df_list.append(df)

# Combine all into one DataFrame
combined_df = pd.concat(df_list, ignore_index=True)

# Preview
print(combined_df.shape)
print(combined_df.head())

# %%
# combined_df.to_csv("C:/Users/franj/notebooks/public school teachers/combined_teachers.csv", index=False)

# %%
df_teachers = pd.melt(
    combined_df,
    id_vars=["Region", "Level"],
    var_name="School Year",
    value_name="Teachers"
)

df_teachers

# %%
sns.set_theme(style="darkgrid")

sns.lineplot(
    x="School Year",
    y="Teachers",
    hue="Level",
    data=df_teachers
)

plt.xticks(rotation=45)
plt.title("Number of Public School Teachers Over Time")
plt.tight_layout()
plt.show()

# %%
# Group by 'Level' and 'School Year' and calculate the total number of teachers
total_teachers_by_category_and_school_year = df_teachers.groupby(['Level', 'School Year'])['Teachers'].sum().reset_index() 

# Rename columns for clarity
total_teachers_by_category_and_school_year.columns = ['School Category', 'Total Teachers', 'School Year']

# Display the result
print(total_teachers_by_category_and_school_year)

# %% [markdown]
# ## Elementary Public School Students

# %%
elementary = pd.ExcelFile("C:/Users/franj/notebooks/public school teachers/elementary.xlsx")

# %%
sheet_names = elementary.sheet_names

# %%
# List to hold the processed DataFrames for each sheet
df_list = []

# Loop through each sheet, sum male and female students per grade level
for sheet in sheet_names:
    # Read data from the sheet with multi-level headers
    df = pd.read_excel(elementary, sheet_name=sheet, header=[0, 1])
    
    # Flatten the multi-level columns
    df.columns = [' '.join(col).strip() for col in df.columns]
    
    # Rename the "Region Unnamed: 0_level_1" column back to "Region"
    df.rename(columns={"Region Unnamed: 0_level_1": "Region"}, inplace=True)
    
    # Debug: Print the columns to verify
    print(f"Flattened columns for sheet '{sheet}': {df.columns}")
    
    # Ensure the 'Region' column exists
    if 'Region' not in df.columns:
        raise KeyError(f"'Region' column not found in sheet '{sheet}'")
    
    # Identify grade level columns dynamically
    grade_levels = set(col.rsplit(' ', 1)[0] for col in df.columns if "Male" in col or "Female" in col)
    
    # Debug: Print identified grade levels
    print(f"Identified grade levels for sheet '{sheet}': {grade_levels}")
    
    # Create a new DataFrame to store totals per grade level
    grade_totals = pd.DataFrame()
    grade_totals['Region'] = df['Region']  # Keep the "Region" column
    
    for grade in grade_levels:
        male_col = f"{grade} Male"
        female_col = f"{grade} Female"
        
        if male_col in df.columns and female_col in df.columns:
            # Sum "Male" and "Female" columns for the grade level
            grade_totals[grade] = df[male_col] + df[female_col]
    
    # Add a 'School Year' column to keep track of which year it came from
    grade_totals['School Year'] = sheet
    
    # Append the processed DataFrame to the list
    df_list.append(grade_totals)

# Concatenate all DataFrames together into one large DataFrame
combined_df = pd.concat(df_list, ignore_index=True)

# Export to CSV
# combined_df.to_csv("C:/Users/franj/notebooks/public school teachers/combined_elementary.csv", index=False)

# Preview the combined DataFrame
print(combined_df)

# %%
combined_df.columns

# %%
combined_df = combined_df[['Region', 'Kindergarten', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Non-Grade (ES)','School Year']]

print(combined_df)

# %%
melted_df = pd.melt(
    combined_df,
    id_vars=["Region", "School Year"],
    value_vars=["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Non-Grade (ES)"],
    var_name="Grade Level",
    value_name="Students"
)

melted_df

# %%
# melted_df.to_csv("C:/Users/franj/notebooks/public school teachers/combined_elementary.csv", index=False)

# %%
def number_of_students_over_time_and_region(melted_df, region=None):
    sns.set_theme(style="darkgrid")

    # Ensure 'School Year' is treated as a categorical variable for better visualization
    melted_df['School Year'] = melted_df['School Year'].astype(str)
    
    # Create a figure
    plt.figure(figsize=(12, 8))
    
    if region:
        # Filter for specific region if provided
        filtered_df = melted_df[melted_df['Region'] == region]
        title_suffix = f" for {region}"
    else:
        # Use all regions
        filtered_df = melted_df
        title_suffix = " by Region"
    
    # Create the line plot
    sns.lineplot(
        x="School Year",
        y="Students",
        hue="Region",  # Use Region as the hue
        data=filtered_df
    )
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add a title and adjust layout
    plt.title(f"Number of Elementary School Students Over Time{title_suffix}")
    
    # Move the legend outside the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    
    # Adjust layout to prevent clipping
    plt.tight_layout()
    
    # Show the plot
    plt.show()

# Call the function with all regions
number_of_students_over_time_and_region(melted_df)

# Alternatively, call it for each region
regions = melted_df['Region'].unique()
for region in regions:
    number_of_students_over_time_and_region(melted_df, region)
    print(f"--- {region} ---")

# %%
# Group by 'Level' and 'School Year' and calculate the total number of students
total_students_by_category_and_school_year = melted_df.groupby(['School Year'])['Students'].sum().reset_index()

# Rename columns for clarity
total_teachers_by_category_and_school_year.columns = ['School Category', 'Total Students', 'School Year']

# Display the result
print(total_students_by_category_and_school_year)

# %%
# Rename 'Grade Level' to 'Level' in melted_df to match df_teachers
melted_df.rename(columns={'Grade Level': 'Level'}, inplace=True)

# rename school years in df_teachers to match melted_df
df_teachers['School Year'] = df_teachers['School Year'].str.replace('SY ', '')

# %%
# Filter df_teachers to include only "Elementary" level
elementary_teachers = df_teachers[df_teachers['Level'] == 'Elementary']

# Group teachers by 'School Year' and 'Region' and calculate the total number of teachers
teachers_by_year_region = elementary_teachers.groupby(['School Year', 'Region'])['Teachers'].sum().reset_index()

# Group students by 'School Year' and 'Region' and calculate the total number of students
students_by_year_region = melted_df.groupby(['School Year', 'Region'])['Students'].sum().reset_index()

# Merge the two DataFrames on 'School Year' and 'Region'
ratio_df = pd.merge(teachers_by_year_region, students_by_year_region, on=['School Year', 'Region'], how='inner')

# Calculate the ratio of teachers to students
ratio_df['Student-to-Teacher Ratio'] = ratio_df['Students'] / ratio_df['Teachers']

# Display the resulting DataFrame
print(ratio_df)

# %%
ratio_df['Student-to-Teacher Ratio'].describe()

# %%
def filter_and_plot_ratio(ratio_df, school_year):
    # Filter the DataFrame for the given school year
    student_teacher = ratio_df[ratio_df['School Year'] == school_year]
    student_teacher = student_teacher[['Region', 'School Year', 'Student-to-Teacher Ratio']]

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 8))  # Increased figure size for better spacing
    sns.barplot(data=student_teacher, x="Region", y="Student-to-Teacher Ratio", dodge=True)

    plt.axhline(y=18, color='red', linestyle='--', label="Ideal Ratio (18:1)")

    plt.title(f"Elementary Student-to-Teacher Ratio by Region in {school_year}", fontsize=14)
    plt.xlabel("Region", fontsize=12)
    plt.ylabel("Student-to-Teacher Ratio", fontsize=12)
    plt.xticks(rotation=30, ha='right')  # Rotated labels and aligned them to the right
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()

    plt.show()

# Loop through the school years and call the function
for year in ['2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', 
             '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021']:
    filter_and_plot_ratio(ratio_df, year)
    print(f"--- {year} ---")

# %% [markdown]
# ## Junior High Public School Students

# %%
junior_high = pd.ExcelFile("C:/Users/franj/notebooks/public school teachers/junior high school.xlsx")

# %%
sheet_names = junior_high.sheet_names

# %%
df_list = []

# Loop through each sheet, sum male and female students per grade level
for sheet in sheet_names:
    # Read data from the sheet with multi-level headers
    df = pd.read_excel(junior_high, sheet_name=sheet, header=[0, 1])
    
    # Flatten the multi-level columns
    df.columns = [' '.join(col).strip() for col in df.columns]
    
    # Rename the "Region Unnamed: 0_level_1" column back to "Region"
    df.rename(columns={"Region Unnamed: 0_level_1": "Region"}, inplace=True)
    
    # Debug: Print the columns to verify
    print(f"Flattened columns for sheet '{sheet}': {df.columns}")
    
    # Ensure the 'Region' column exists
    if 'Region' not in df.columns:
        raise KeyError(f"'Region' column not found in sheet '{sheet}'")
    
    # Identify grade level columns dynamically
    grade_levels = set(col.rsplit(' ', 1)[0] for col in df.columns if "Male" in col or "Female" in col)
    
    # Debug: Print identified grade levels
    print(f"Identified grade levels for sheet '{sheet}': {grade_levels}")
    
    # Create a new DataFrame to store totals per grade level
    grade_totals = pd.DataFrame()
    grade_totals['Region'] = df['Region']  # Keep the "Region" column
    
    for grade in grade_levels:
        male_col = f"{grade} Male"
        female_col = f"{grade} Female"
        
        if male_col in df.columns and female_col in df.columns:
            # Sum "Male" and "Female" columns for the grade level
            grade_totals[grade] = df[male_col] + df[female_col]
    
    # Add a 'School Year' column to keep track of which year it came from
    grade_totals['School Year'] = sheet
    
    # Append the processed DataFrame to the list
    df_list.append(grade_totals)

# Concatenate all DataFrames together into one large DataFrame
combined_df = pd.concat(df_list, ignore_index=True)

# Export to CSV
# combined_df.to_csv("C:/Users/franj/notebooks/public school teachers/combined_junior_high.csv", index=False)

# Preview the combined DataFrame
print(combined_df)

# %%
combined_df.columns

# %%
combined_df = combined_df[['Region', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Non-Grade (SS)', 'Non-Grade (JHS)', 'School Year' ]]

print(combined_df)

# %%
melted_df = pd.melt(
    combined_df,
    id_vars=["Region", "School Year"],
    value_vars=['Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Non-Grade (SS)', 'Non-Grade (JHS)'],
    var_name="Grade Level",
    value_name="Students"
)

melted_df

# %%
# melted_df.to_csv("C:/Users/franj/notebooks/public school teachers/combined_junior_high.csv", index=False)

# %%
def number_of_students_over_time_and_region(melted_df, region=None):
    sns.set_theme(style="darkgrid")

    # Ensure 'School Year' is treated as a categorical variable for better visualization
    melted_df['School Year'] = melted_df['School Year'].astype(str)
    
    # Create a figure
    plt.figure(figsize=(12, 8))
    
    if region:
        # Filter for specific region if provided
        filtered_df = melted_df[melted_df['Region'] == region]
        title_suffix = f" for {region}"
    else:
        # Use all regions
        filtered_df = melted_df
        title_suffix = " by Region"
    
    # Create the line plot
    sns.lineplot(
        x="School Year",
        y="Students",
        hue="Region",  # Use Region as the hue
        data=filtered_df
    )
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add a title and adjust layout
    plt.title(f"Number of Junior High Public School Students Over Time{title_suffix}")
    
    # Move the legend outside the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    
    # Adjust layout to prevent clipping
    plt.tight_layout()
    
    # Show the plot
    plt.show()

# Call the function with all regions
number_of_students_over_time_and_region(melted_df)

# Alternatively, call it for each region
regions = melted_df['Region'].unique()
for region in regions:
    number_of_students_over_time_and_region(melted_df, region)
    print(f"--- {region} ---")

# %%
# Group by 'Level' and 'School Year' and calculate the total number of students
total_students_by_category_and_school_year = melted_df.groupby(['School Year'])['Students'].sum().reset_index()

# Rename columns for clarity
total_teachers_by_category_and_school_year.columns = ['School Category', 'Total Students', 'School Year']

# Display the result
print(total_students_by_category_and_school_year)

# %%
# Rename 'Grade Level' to 'Level' in melted_df to match df_teachers
melted_df.rename(columns={'Grade Level': 'Level'}, inplace=True)

# %%
# Filter df_teachers to include only "Junior High" level
junior_high_teachers = df_teachers[df_teachers['Level'] == 'Junior High School']

# Group teachers by 'School Year' and 'Region' and calculate the total number of teachers
teachers_by_year_region = junior_high_teachers.groupby(['School Year', 'Region'])['Teachers'].sum().reset_index()

# Group students by 'School Year' and 'Region' and calculate the total number of students
students_by_year_region = melted_df.groupby(['School Year', 'Region'])['Students'].sum().reset_index()

# Merge the two DataFrames on 'School Year' and 'Region'
ratio_df = pd.merge(teachers_by_year_region, students_by_year_region, on=['School Year', 'Region'], how='inner')

# Calculate the ratio of teachers to students
ratio_df['Student-to-Teacher Ratio'] = ratio_df['Students'] / ratio_df['Teachers']

# Display the resulting DataFrame
print(ratio_df)

# %%
ratio_df['Student-to-Teacher Ratio'].describe()

# %%
def filter_and_plot_ratio(ratio_df, school_year):
    # Filter the DataFrame for the given school year
    student_teacher = ratio_df[ratio_df['School Year'] == school_year]
    student_teacher = student_teacher[['Region', 'School Year', 'Student-to-Teacher Ratio']]

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 8))  # Increased figure size for better spacing
    sns.barplot(data=student_teacher, x="Region", y="Student-to-Teacher Ratio", dodge=True)

    plt.axhline(y=18, color='red', linestyle='--', label="Ideal Ratio (18:1)")

    plt.title(f"Junior High Student-to-Teacher Ratio by Region in {school_year}", fontsize=14)
    plt.xlabel("Region", fontsize=12)
    plt.ylabel("Student-to-Teacher Ratio", fontsize=12)
    plt.xticks(rotation=30, ha='right')  # Rotated labels and aligned them to the right
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()

    plt.show()

# Loop through the school years and call the function
for year in ['2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', 
             '2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021']:
    filter_and_plot_ratio(ratio_df, year)
    print(f"--- {year} ---")

# %% [markdown]
# ## Senior High Public School Students

# %%
senior_high = pd.ExcelFile("C:/Users/franj/notebooks/public school teachers/senior high school.xlsx")

# %%
sheet_names = senior_high.sheet_names

# %%
df_list = []

# Loop through each sheet, sum male and female students per grade level
for sheet in sheet_names:
    # Read data from the sheet with multi-level headers
    df = pd.read_excel(senior_high, sheet_name=sheet, header=[0, 1])
    
    # Flatten the multi-level columns
    df.columns = [' '.join(col).strip() for col in df.columns]
    
    # Rename the "Region Unnamed: 0_level_1" column back to "Region"
    df.rename(columns={"Region Unnamed: 0_level_1": "Region"}, inplace=True)
    
    # Debug: Print the columns to verify
    print(f"Flattened columns for sheet '{sheet}': {df.columns}")
    
    # Ensure the 'Region' column exists
    if 'Region' not in df.columns:
        raise KeyError(f"'Region' column not found in sheet '{sheet}'")
    
    # Identify grade level columns dynamically
    grade_levels = set(col.rsplit(' ', 1)[0] for col in df.columns if "Male" in col or "Female" in col)
    
    # Debug: Print identified grade levels
    print(f"Identified grade levels for sheet '{sheet}': {grade_levels}")
    
    # Create a new DataFrame to store totals per grade level
    grade_totals = pd.DataFrame()
    grade_totals['Region'] = df['Region']  # Keep the "Region" column
    
    for grade in grade_levels:
        male_col = f"{grade} Male"
        female_col = f"{grade} Female"
        
        if male_col in df.columns and female_col in df.columns:
            # Sum "Male" and "Female" columns for the grade level
            grade_totals[grade] = df[male_col] + df[female_col]
    
    # Add a 'School Year' column to keep track of which year it came from
    grade_totals['School Year'] = sheet
    
    # Append the processed DataFrame to the list
    df_list.append(grade_totals)

# Concatenate all DataFrames together into one large DataFrame
combined_df = pd.concat(df_list, ignore_index=True)

# Export to CSV
# combined_df.to_csv("C:/Users/franj/notebooks/public school teachers/combined_senior_high.csv", index=False)

# Preview the combined DataFrame
print(combined_df)

# %%
combined_df.columns

# %%
combined_df = combined_df[['Region', "Grade 11 (TVL)", "Grade 11 (GAS)", "Grade 11 (STEM)", "Grade 11 (MARITIME)", "Grade 11 (ARTs & DESIGN)", "Grade 11 (SPORTs)", "Grade 11 (HUMSS)",	"Grade 11 (ABM)", "Grade 12 (SPORTs)", "Grade 12 (GAS)", "Grade 12 (STEM)", "Grade 12 (TVL)", "Grade 12 (HUMSS)", "Grade 12 (MARITIME)", "Grade 12 (ABM)", "Grade 12 (ARTs & DESIGN)", "School Year"]]

print(combined_df)

# %%
melted_df = pd.melt(
    combined_df,
    id_vars=["Region", "School Year"],
    value_vars=["Grade 11 (TVL)", "Grade 11 (GAS)", "Grade 11 (STEM)", "Grade 11 (MARITIME)", "Grade 11 (ARTs & DESIGN)", "Grade 11 (SPORTs)", "Grade 11 (HUMSS)",	"Grade 11 (ABM)", "Grade 12 (SPORTs)", "Grade 12 (GAS)", "Grade 12 (STEM)", "Grade 12 (TVL)", "Grade 12 (HUMSS)", "Grade 12 (MARITIME)", "Grade 12 (ABM)", "Grade 12 (ARTs & DESIGN)"],
    var_name="Grade Level",
    value_name="Students"
)

melted_df

# %%
melted_df.dropna(inplace=True)

# %%
# melted_df.to_csv("C:/Users/franj/notebooks/public school teachers/combined_senior_high.csv", index=False)

# %%
def number_of_students_over_time_and_region(melted_df, region=None):
    sns.set_theme(style="darkgrid")

    # Ensure 'School Year' is treated as a categorical variable for better visualization
    melted_df['School Year'] = melted_df['School Year'].astype(str)
    
    # Create a figure
    plt.figure(figsize=(12, 8))
    
    if region:
        # Filter for specific region if provided
        filtered_df = melted_df[melted_df['Region'] == region]
        title_suffix = f" for {region}"
    else:
        # Use all regions
        filtered_df = melted_df
        title_suffix = " by Region"
    
    # Create the line plot
    sns.lineplot(
        x="School Year",
        y="Students",
        hue="Region",  # Use Region as the hue
        data=filtered_df
    )
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add a title and adjust layout
    plt.title(f"Number of Senior High Public School Students Over Time{title_suffix}")
    
    # Move the legend outside the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    
    # Adjust layout to prevent clipping
    plt.tight_layout()
    
    # Show the plot
    plt.show()

# Call the function with all regions
number_of_students_over_time_and_region(melted_df)

# Alternatively, call it for each region
regions = melted_df['Region'].unique()
for region in regions:
    number_of_students_over_time_and_region(melted_df, region)
    print(f"--- {region} ---")

# %%
# Group by 'Level' and 'School Year' and calculate the total number of students
total_students_by_category_and_school_year = melted_df.groupby(['School Year'])['Students'].sum().reset_index()

# Rename columns for clarity
total_teachers_by_category_and_school_year.columns = ['School Category', 'Total Students', 'School Year']

# Display the result
print(total_students_by_category_and_school_year)

# %%
# Rename 'Grade Level' to 'Level' in melted_df to match df_teachers
melted_df.rename(columns={'Grade Level': 'Level'}, inplace=True)

# %%
# Filter df_teachers to include only "Senior High" level
senior_high_teachers = df_teachers[df_teachers['Level'] == 'Senior High School']

# Group teachers by 'School Year' and 'Region' and calculate the total number of teachers
teachers_by_year_region = senior_high_teachers.groupby(['School Year', 'Region'])['Teachers'].sum().reset_index()

# Group students by 'School Year' and 'Region' and calculate the total number of students
students_by_year_region = melted_df.groupby(['School Year', 'Region'])['Students'].sum().reset_index()

# Merge the two DataFrames on 'School Year' and 'Region'
ratio_df = pd.merge(teachers_by_year_region, students_by_year_region, on=['School Year', 'Region'], how='inner')

# Calculate the ratio of teachers to students
ratio_df['Student-to-Teacher Ratio'] = ratio_df['Students'] / ratio_df['Teachers']

# Display the resulting DataFrame
print(ratio_df)

# %%
ratio_df['Student-to-Teacher Ratio'].describe()

# %%
def filter_and_plot_ratio(ratio_df, school_year):
    # Filter the DataFrame for the given school year
    student_teacher = ratio_df[ratio_df['School Year'] == school_year]
    student_teacher = student_teacher[['Region', 'School Year', 'Student-to-Teacher Ratio']]

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 8))  # Increased figure size for better spacing
    sns.barplot(data=student_teacher, x="Region", y="Student-to-Teacher Ratio", dodge=True)

    plt.axhline(y=18, color='red', linestyle='--', label="Ideal Ratio (18:1)")

    plt.title(f"Senior High Student-to-Teacher Ratio by Region in {school_year}", fontsize=14)
    plt.xlabel("Region", fontsize=12)
    plt.ylabel("Student-to-Teacher Ratio", fontsize=12)
    plt.xticks(rotation=30, ha='right')  # Rotated labels and aligned them to the right
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()

    plt.show()

# Loop through the school years and call the function
for year in ['2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021']:
    filter_and_plot_ratio(ratio_df, year)
    print(f"--- {year} ---")


