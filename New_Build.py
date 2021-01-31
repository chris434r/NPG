import pandas as pd
postcodes_df =pd.read_csv (r'/Volumes/CR SSD/GIS/WSP Projects/_2020/NPG/ONS Data/ONSPD_MAY_2019_UK/Data/multi_csv/USE/Dates.csv')


ONS_New_Build_filter = postcodes_df.loc[postcodes_df["dointr"] >= 201000]

print(ONS_New_Build_filter)

#ONS_New_Build_filter.to_excel(r'/Volumes/CR SSD/GIS/WSP Projects/_2020/NPG/ONS Data/ONSPD_MAY_2019_UK/Data/multi_csv/USE/ONS_New_Build.xlsx')

