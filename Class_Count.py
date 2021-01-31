import pandas as pd

customer_df = pd.read_excel (r'/Users/chrisryan/PycharmProjects/NPG/Master/Batch8.xlsx')
New_Build_df =pd.read_excel (r'/Users/chrisryan/PycharmProjects/NPG/Master/ONS_New_Build.xlsx')
CAB_CODES = pd.read_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/CAB_CODES.xlsx')

customer_df['wsp_circui'] = customer_df['wsp_circui'].astype(float)

#Joining customer postcodes to ONS, to get build date.

BD_Join = pd.merge (customer_df, New_Build_df, how = 'left', left_on = ['POSTCODE'], right_on = ['pcd2'])
NB_filter = BD_Join.loc [BD_Join ["dointr"] >= 201000]


NB_count = BD_Join.groupby('wsp_circui')["Count_y"].value_counts().reset_index(name="NB_count")

#Grouping Addressbase classifications

Total_Customer = customer_df.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Total_Customers")

Domestic_filter = customer_df.loc[customer_df['Primary_Code'] =='R']
Domestic_Count = Domestic_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Domestic_Count")

Commerical_filter = customer_df.loc[customer_df['Primary_Code'] =='C']
Commerical_Count = Commerical_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Commercial_Count")

Detached_filter = customer_df.loc [customer_df["Concatenated"]== 'RD02']
Detached_count = Detached_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Detached_count")

Semi_Detached_filter = customer_df.loc [customer_df["Concatenated"]=='RD03']
Semi_Detached_count = Semi_Detached_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Semi_Detached_count")

Terraced_filter = customer_df.loc [customer_df["Concatenated"]=='RD04']
Terraced_count = Terraced_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Terraced_count")

flats_filter = customer_df.loc [customer_df["Concatenated"]=='RD06']
flats_count = flats_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="flats_count")

farm_filter = customer_df.loc[(customer_df["Concatenated"]=='LA') | (customer_df["Concatenated"]=='LA01') | (customer_df["Concatenated"]=='LA02') | (customer_df["Concatenated"]=='LA02OC')]
farm_count = farm_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="farm_count")


#UA Code calcs

UA_Code_1_filter = customer_df.loc [customer_df["UA_Code_New"]=='Inner_City']
UA_Code_1_count = UA_Code_1_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Inner_City_count")
UA_Code_2_filter = customer_df.loc [customer_df["UA_Code_New"]=='Urban']
UA_Code_2_count = UA_Code_2_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Urban_count")
UA_Code_3_filter = customer_df.loc [customer_df["UA_Code_New"]=='Rural']
UA_Code_3_count = UA_Code_3_filter.groupby('wsp_circui')["Count"].value_counts().reset_index(name="Rural_count")

#CAB Code merge
Cab_merge = pd.merge (BD_Join, CAB_CODES, how = 'left', left_on = ['wsp_circui'], right_on = ['circuit_id'])

out1 = pd.merge (Cab_merge, Domestic_Count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])
out2 = out2 = pd.merge (out1, Total_Customer, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])
out3 = pd.merge (out2, Commerical_Count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])
out4 = pd.merge (out3, Detached_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])
out5 = pd.merge (out4, Semi_Detached_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])
out6 = pd.merge (out5, Terraced_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])
out7 = pd.merge (out6, flats_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])
out8 = pd.merge (out7, farm_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])


#Cab_merge.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch3_CAB_CHECK_20201130.xlsx')

out9 = pd.merge (out8, UA_Code_1_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])
out10 = pd.merge (out9, UA_Code_2_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])

out11 = pd.merge (out10, UA_Code_3_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])

Final_merge = pd.merge (out11,NB_count, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])

#Final_merge.head(10000).to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/FINAL_MERGE_COUNT_HEAD.xlsx')

#New Build Average Calculation


Final_merge ["New_Build_Average"] = Final_merge['NB_count']/Final_merge['Total_Customers']*100


#UA_Codes Calculation


Final_merge ["Inner_City_Average"] = Final_merge['Inner_City_count']/Final_merge['Total_Customers']*100
Final_merge ["Urban_Average"] = Final_merge['Urban_count']/Final_merge['Total_Customers']*100
Final_merge ["Rural_Average"] = Final_merge['Rural_count']/Final_merge['Total_Customers']*100

Final_merge.loc[(Final_merge["Inner_City_Average"] >= 50 ), 'UA_Code_Num'] = 1
Final_merge.loc[(Final_merge["Urban_Average"] >= 50 ), 'UA_Code_Num'] = 2
Final_merge.loc[Final_merge["Rural_Average"] > 50, 'UA_Code_Num'] = 3


#DOM Codes Calculation

Final_merge ["Domestic_Average"] = Final_merge['Domestic_Count']/Final_merge['Total_Customers']*100
Final_merge ["Commercial_Average"] = Final_merge['Commercial_Count']/Final_merge['Total_Customers']*100


Final_merge.loc[Final_merge["Domestic_Average"] >= 70, 'Dom_Code'] = 1
Final_merge.loc[Final_merge["Commercial_Average"] >= 70, 'Dom_Code'] = 2
Final_merge.loc[(Final_merge["Dom_Code"] != 1 ) & (Final_merge["Dom_Code"] != 2 ), 'Dom_Code'] = 3


#FC_Codes_Calculation

Final_merge.loc[(Final_merge["Dom_Code"] == 2 ), 'FC_Code'] = 1
Final_merge.loc[(Final_merge["Dom_Code"] == 3 ), 'FC_Code'] = 10


Final_merge ["Detached_Semi_Detached_count"] = Final_merge ['Detached_count'] + Final_merge['Semi_Detached_count']
Final_merge ["Detached_Semi_Detached_Avg"] = Final_merge['Detached_Semi_Detached_count']/Final_merge ['Total_Customers']*100
Final_merge.loc[(Final_merge["Dom_Code"] == 1 ) & (Final_merge["Detached_Semi_Detached_Avg"] >= 70 ),'FC_Code'] = 5
Final_merge["Terraced_Average"] = Final_merge ['Terraced_count']/Final_merge['Total_Customers']*100
Final_merge.loc[(Final_merge["Dom_Code"] == 1 ) & (Final_merge ["Terraced_Average"] >= 70), 'FC_Code'] = 6
Final_merge ["Flats_Average"] = Final_merge ['flats_count']/Final_merge['Total_Customers']*100
Final_merge.loc[(Final_merge["Dom_Code"] == 1) & (Final_merge["Flats_Average"] >= 70), 'FC_Code'] = 7
Final_merge ["Farms_Average"] = Final_merge ['farm_count']/Final_merge['Total_Customers']*100
Final_merge.loc[(Final_merge["Dom_Code"] != 2) & (Final_merge["Farms_Average"] >= 80), 'FC_Code'] = 9
Final_merge.loc[(Final_merge["Dom_Code"] == 1) & (Final_merge["FC_Code"] != 5) & (Final_merge["FC_Code"] != 6) & (Final_merge["FC_Code"] != 7)& (Final_merge["FC_Code"] != 9),'FC_Code'] = 8



#Final_merge.loc[(Final_merge["FC_Code"] != 5) & (Final_merge["FC_Code"] != 6) & (Final_merge["FC_Code"] != 7)& (Final_merge["FC_Code"] != 8),'FC_Code'] = 99999


######## Calculating FT Codes - Final output


Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 7),'FT_Code']= 2
Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 7),'Designation']= 'Dense Urban Apartments'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 7),'Feeder Type']= 'LVFT02'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 5),'FT_Code']= 3
Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 5),'Designation']= 'Urban Detached or Semi'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 5),'Feeder Type']= 'LVFT03'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 6) ,'FT_Code']= 4
Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 6) ,'Designation']= 'Urban Terraced'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 6) ,'Feeder Type']= 'LVFT07'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 8),'FT_Code']= 5
Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 8),'Designation']= 'Urban Mixed Domestic'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 1) & (Final_merge["FC_Code"] == 8),'Feeder Type']= 'LVFT04'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 7),'FT_Code']= 7
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 7),'Designation']= 'Suburban Apartment'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 7),'Feeder Type']= 'LVFT05'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 5) & (Final_merge["New_Build_Average"] < 50),'FT_Code']= 8
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 5) & (Final_merge["New_Build_Average"] < 50),'Designation']= 'Suburban Street'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 5) & (Final_merge["New_Build_Average"] < 50),'Feeder Type']= 'LVFT06'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 5) & (Final_merge["New_Build_Average"] >= 50),'FT_Code']= 9
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 5) & (Final_merge["New_Build_Average"] >= 50),'Designation']= 'Suburban New Build'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 5) & (Final_merge["New_Build_Average"] >= 50),'Feeder Type']= 'LVFT12'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 6) ,'FT_Code']= 10
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 6) ,'Designation']= 'Suburban Terraced'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 6 ) ,'Feeder Type']= 'LVFT07'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 8) ,'FT_Code']= 11
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 8) ,'Designation']= 'Suburban Mixed Domestic'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 2) & (Final_merge["FC_Code"] == 8 ) ,'Feeder Type']= 'LVFT14'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1) & (Final_merge["New_Build_Average"] >= 50) & (Final_merge["Total_Customers"] > 3 ), 'FT_Code']= 12
Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1) & (Final_merge["New_Build_Average"] >= 50) &(Final_merge["Total_Customers"] > 3 ) ,'Designation']= 'New Build Street'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1) & (Final_merge["New_Build_Average"] >= 50) & (Final_merge["Total_Customers"] > 3 ),'Feeder Type']= 'LVFT08'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] == 6) ,'FT_Code']= 13
Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] == 6) ,'Designation']= 'Rural Terraced'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] == 6 ) ,'Feeder Type']= 'LVFT13'



#Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50)& (Final_merge["CAB_Code"] == 0), 'FT_Code']= 14
#Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50)& (Final_merge["CAB_Code"] == 0),'Designation']= 'Rural Domestic OH'
#Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50)& (Final_merge["CAB_Code"] == 0),'Feeder Type']= 'LVFT09'

#Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50)& (Final_merge["CAB_Code"] == 1), 'FT_Code']= 15
#Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50)& (Final_merge["CAB_Code"] == 1),'Designation']= 'Rural Domestic UG'
#Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50)& (Final_merge["CAB_Code"] == 1),'Feeder Type']= 'LVFT10'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50) , 'FT_Code']= 111
Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50) ,'Designation']= 'Rural Domestic Merge'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1)& (Final_merge["Total_Customers"] > 3 )& (Final_merge["New_Build_Average"] < 50) ,'Feeder Type']= 'LVFT_9_10'

Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1) & (Final_merge["Total_Customers"] <= 3 ), 'FT_Code']= 16
Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1) & (Final_merge["Total_Customers"] <= 3 ), 'Designation']= 'Rural Domestic Small Holdings'
Final_merge.loc[(Final_merge["UA_Code_Num"] == 3) & (Final_merge["FC_Code"] != 6) & (Final_merge["Dom_Code"] == 1) & (Final_merge["Total_Customers"] <= 3 ), 'Feeder Type']= 'LVFT11'


Final_merge.loc[ (Final_merge["FC_Code"] == 1),'FT_Code']= 20
Final_merge.loc[(Final_merge["FC_Code"] == 1),'Designation']= 'Retail, Commercial,Industrial, Other Non Domestic'
Final_merge.loc[(Final_merge["FC_Code"] == 1),'Feeder Type']= 'LVFT15'

#Final_merge.loc[ (Final_merge["FC_Code"] == 2),'FT_Code']= 21
#Final_merge.loc[(Final_merge["FC_Code"] == 2),'Designation']= 'Commercial'
#Final_merge.loc[(Final_merge["FC_Code"] == 2),'Feeder Type']= 'LVFT16'

# Final_merge.loc[ (Final_merge["FC_Code"] == 3),'FT_Code']= 22
#  Final_merge.loc[(Final_merge["FC_Code"] == 3),'Designation']= 'Industrial'
# Final_merge.loc[(Final_merge["FC_Code"] == 3),'Feeder Type']= 'LVFT17'

# Final_merge.loc[ (Final_merge["FC_Code"] == 4),'FT_Code']= 23
# Final_merge.loc[(Final_merge["FC_Code"] == 4),'Designation']= 'Other non domestic'
# Final_merge.loc[(Final_merge["FC_Code"] == 4),'Feeder Type']= 'LVFT18'

Final_merge.loc[ (Final_merge["FC_Code"] == 10),'FT_Code']= 30
Final_merge.loc[(Final_merge["FC_Code"] == 10),'Designation']= 'Mixed Domestic or non domestic'
Final_merge.loc[(Final_merge["FC_Code"] == 10),'Feeder Type']= 'LVFT16'






#Batch1

#Final_merge.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch1/Batch1_codes.xlsx')

# LA_1_filter_query = Final_merge['LA'] =='Bn'
# LA_1_filter = Final_merge[LA_1_filter_query]
# LA_1_filter_out = LA_1_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA1 = LA_1_filter_out[LA_1_filter_out.FT_Code.notnull()]
# LA1.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch1/Barnsley_Summary.xlsx')
#
# #
# LA_2_filter_query = Final_merge['LA'] =='Bs'
# LA_2_filter = Final_merge[LA_2_filter_query]
# LA_2_filter_out = LA_2_filter[['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA2 = LA_2_filter_out[LA_2_filter_out.FT_Code.notnull()]
# LA2.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch1/Bassetlaw_Summary.xlsx')
#
# LA_3_filter_query = Final_merge['LA'] =='Bf'
# LA_3_filter = Final_merge[LA_3_filter_query]
# LA_3_filter_out = LA_3_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA3 = LA_3_filter_out[LA_3_filter_out.FT_Code.notnull()]
# LA3.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch1/Bradford_Summary.xlsx')
#
# #
# LA_4_filter_query = Final_merge['LA'] =='Cl'
# LA_4_filter = Final_merge[LA_4_filter_query]
# LA_4_filter_out = LA_4_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA4 = LA_4_filter_out[LA_4_filter_out.FT_Code.notnull()]
# LA4.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch1/Calderdale_Summary.xlsx')
# #
# LA_5_filter_query = Final_merge['LA'] =='CD'
# LA_5_filter = Final_merge[LA_5_filter_query]
# LA_5_filter_out = LA_5_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA5 = LA_5_filter_out[LA_5_filter_out.FT_Code.notnull()]
# LA5.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch1/Country_Durham_Summary.xlsx')
#
# LA_6_filter_query = Final_merge['LA'] =='Cr'
# LA_6_filter = Final_merge[LA_6_filter_query]
# LA_6_filter_out = LA_6_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA6 = LA_6_filter_out[LA_6_filter_out.FT_Code.notnull()]
# LA6.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch1/Craven_Summary.xlsx')
#
# LA_7_filter_query = Final_merge['LA'] =='DI'
# LA_7_filter = Final_merge[LA_7_filter_query]
# LA_7_filter_out = LA_7_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA7 = LA_7_filter_out[LA_7_filter_out.FT_Code.notnull()]
# LA7.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch1/Darlington_Summary.xlsx')


#Batch2

# Final_merge.head(1000).to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch2/Batch2_codes.xlsx')
#
# LA_1_filter_query = Final_merge['LA'] =='Dc'
# LA_1_filter = Final_merge[LA_1_filter_query]
# LA_1_filter_out = LA_1_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA1 = LA_1_filter_out[LA_1_filter_out.FT_Code.notnull()]
# LA1.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch2/Doncaster_Summary.xlsx')
#
# LA_2_filter_query = Final_merge['LA'] =='EL'
# LA_2_filter = Final_merge[LA_2_filter_query]
# LA_2_filter_out = LA_2_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA2 = LA_2_filter_out[LA_2_filter_out.FT_Code.notnull()]
# LA2.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch2/East_Lindsey_Summary.xlsx')
#
#
# LA_3_filter_query = Final_merge['LA'] =='ER'
# LA_3_filter = Final_merge[LA_3_filter_query]
# LA_3_filter_out = LA_3_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA3 = LA_3_filter_out[LA_3_filter_out.FT_Code.notnull()]
# LA3.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch2/East_Ride_Yorkshire_Summary.xlsx')
#
#
# LA_4_filter_query = Final_merge['LA'] =='Gt'
# LA_4_filter = Final_merge[LA_4_filter_query]
# LA_4_filter_out = LA_4_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA4 = LA_4_filter_out[LA_4_filter_out.FT_Code.notnull()]
# LA4.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch2/Gateshead_Summary.xlsx')
#
#
# LA_5_filter_query = Final_merge['LA'] =='Hb'
# LA_5_filter = Final_merge[LA_5_filter_query]
# LA_5_filter_out = LA_5_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA5 = LA_5_filter_out[LA_5_filter_out.FT_Code.notnull()]
# LA5.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch2/Hambleton_Summary.xlsx')

#Batch 3


# Final_merge.head(1000).to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch3/Batch3_codes.xlsx')
#
# LA_1_filter_query = Final_merge['LA'] =='Hg'
# LA_1_filter = Final_merge[LA_1_filter_query]
# LA_1_filter_out = LA_1_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA1 = LA_1_filter_out[LA_1_filter_out.FT_Code.notnull()]
# LA1.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch3/Harrowgate_Summary.xlsx')
#
# LA_2_filter_query = Final_merge['LA'] =='Ht'
# LA_2_filter = Final_merge[LA_2_filter_query]
# LA_2_filter_out = LA_2_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA2 = LA_2_filter_out[LA_2_filter_out.FT_Code.notnull()]
# LA2.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch3/Hartlepool_Summary.xlsx')
#
#
# LA_3_filter_query = Final_merge['LA'] =='HP'
# LA_3_filter = Final_merge[LA_3_filter_query]
# LA_3_filter_out = LA_3_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA3 = LA_3_filter_out[LA_3_filter_out.FT_Code.notnull()]
# LA3.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch3/High_Peak_Summary.xlsx')
# #
# LA_4_filter_query = Final_merge['LA'] =='KH'
# LA_4_filter = Final_merge[LA_4_filter_query]
# LA_4_filter_out = LA_4_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA4 = LA_4_filter_out[LA_4_filter_out.FT_Code.notnull()]
# LA4.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch3/Kingston_Upon_Hull_Summary.xlsx')
# #
# LA_5_filter_query = Final_merge['LA'] =='Kk'
# LA_5_filter = Final_merge[LA_5_filter_query]
# LA_5_filter_out = LA_5_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA5 = LA_5_filter_out[LA_5_filter_out.FT_Code.notnull()]
# LA5.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch3/Kirkless_Summary.xlsx')

#Batch 4

# Final_merge.head(1000).to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch4/Batch4_codes.xlsx')
#
#
# LA_1_filter_query = Final_merge['LA'] == 'Ld'
# LA_1_filter = Final_merge[LA_1_filter_query]
# LA_1_filter_out = LA_1_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA1 = LA_1_filter_out[LA_1_filter_out.FT_Code.notnull()]
# LA1.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch4/Leeds_Summary.xlsx')
#
# LA_2_filter_query = Final_merge['LA'] == 'Md'
# LA_2_filter = Final_merge[LA_2_filter_query]
# LA_2_filter_out = LA_2_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA2 = LA_2_filter_out[LA_2_filter_out.FT_Code.notnull()]
# LA2.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch4/Middlesbrough_Summary.xlsx')
#
# LA_3_filter_query = Final_merge['LA'] == 'Nu'
# LA_3_filter = Final_merge[LA_3_filter_query]
# LA_3_filter_out = LA_3_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA3 = LA_3_filter_out[LA_3_filter_out.FT_Code.notnull()]
# LA3.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch4/Newcastle_Summary.xlsx')
#
# LA_4_filter_query = Final_merge['LA'] == 'Nr'
# LA_4_filter = Final_merge[LA_4_filter_query]
# LA_4_filter_out = LA_4_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA4 = LA_4_filter_out[LA_4_filter_out.FT_Code.notnull()]
# LA4.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch4/North_East_Derbyshire_Summary.xlsx')
#
# LA_5_filter_query = Final_merge['LA'] == 'No'
# LA_5_filter = Final_merge[LA_5_filter_query]
# LA_5_filter_out = LA_5_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA5 = LA_5_filter_out[LA_5_filter_out.FT_Code.notnull()]
# LA5.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch4/North_East_Lincolnshire_Summary.xlsx')

#Batch5
#
# Final_merge.head(1000).to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch5/Batch5_codes.xlsx')
#
# LA_1_filter_query = Final_merge['LA'] == 'NL'
# LA_1_filter = Final_merge[LA_1_filter_query]
# LA_1_filter_out = LA_1_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA1 = LA_1_filter_out[LA_1_filter_out.FT_Code.notnull()]
# LA1.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch5/North_Lincolnshire_Summary.xlsx')
#
# LA_2_filter_query = Final_merge['LA'] == 'NT'
# LA_2_filter = Final_merge[LA_2_filter_query]
# LA_2_filter_out = LA_2_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA2 = LA_2_filter_out[LA_2_filter_out.FT_Code.notnull()]
# LA2.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch5/North_Tyeneside_Summary.xlsx')
#
# LA_3_filter_query = Final_merge['LA'] == 'Nb'
# LA_3_filter = Final_merge[LA_3_filter_query]
# LA_3_filter_out = LA_3_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA3 = LA_3_filter_out[LA_3_filter_out.FT_Code.notnull()]
# LA3.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch5/Northumberland_Summary.xlsx')
#
# LA_4_filter_query = Final_merge['LA'] == 'Pd'
# LA_4_filter = Final_merge[LA_4_filter_query]
# LA_4_filter_out = LA_4_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA4 = LA_4_filter_out[LA_4_filter_out.FT_Code.notnull()]
# LA4.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch5/Pendle_Summary.xlsx')
#
# LA_5_filter_query = Final_merge['LA'] == 'RC'
# LA_5_filter = Final_merge[LA_5_filter_query]
# LA_5_filter_out = LA_5_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA5 = LA_5_filter_out[LA_5_filter_out.FT_Code.notnull()]
# LA5.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch5/Redcar_Cleveland_Summary.xlsx')

#Batch 6

# Final_merge.head(1000).to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch6/Batch6_codes_head.xlsx')
#
LA_1_filter_query = Final_merge['LA'] == 'Rh'
LA_1_filter = Final_merge[LA_1_filter_query]
LA_1_filter_out = LA_1_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui']]
LA1 = LA_1_filter_out[LA_1_filter_out.FT_Code.notnull()]
LA1.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch6/Richmondshire_Summary.xlsx','LA')
#
# LA_2_filter_query = Final_merge['LA'] == 'Rt'
# LA_2_filter = Final_merge[LA_2_filter_query]
# LA_2_filter_out = LA_2_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA2 = LA_2_filter_out[LA_2_filter_out.FT_Code.notnull()]
# LA2.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch6/Rotherham_Summary.xlsx','LA')
#
# LA_3_filter_query = Final_merge['LA'] == 'Ry'
# LA_3_filter = Final_merge[LA_3_filter_query]
# LA_3_filter_out = LA_3_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA3 = LA_3_filter_out[LA_3_filter_out.FT_Code.notnull()]
# LA3.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch6/Ryedale_Summary.xlsx','LA')
#
# LA_4_filter_query = Final_merge['LA'] == 'Sb'
# LA_4_filter = Final_merge[LA_4_filter_query]
# LA_4_filter_out = LA_4_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA4 = LA_4_filter_out[LA_4_filter_out.FT_Code.notnull()]
# LA4.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch6/Scarborough_Summary.xlsx','LA')
#
# LA_5_filter_query = Final_merge['LA'] == 'Sl'
# LA_5_filter = Final_merge[LA_5_filter_query]
# LA_5_filter_out = LA_5_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA5 = LA_5_filter_out[LA_5_filter_out.FT_Code.notnull()]
# LA5.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch6/Selby_Summary.xlsx')

#Batch7

# Final_merge.head(1000).to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch7/Batch7_codes_head.xlsx')
# #
# LA_1_filter_query = Final_merge['LA'] == 'Sf'
# LA_1_filter = Final_merge[LA_1_filter_query]
# LA_1_filter_out = LA_1_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA1 = LA_1_filter_out[LA_1_filter_out.FT_Code.notnull()]
# LA1.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch7/Sheffield_Summary.xlsx')
#
# LA_2_filter_query = Final_merge['LA'] == 'ST'
# LA_2_filter = Final_merge[LA_2_filter_query]
# LA_2_filter_out = LA_2_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA2 = LA_2_filter_out[LA_2_filter_out.FT_Code.notnull()]
# LA2.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch7/South_Tyneside_Summary.xlsx')
#
# LA_3_filter_query = Final_merge['LA'] == 'So'
# LA_3_filter = Final_merge[LA_3_filter_query]
# LA_3_filter_out = LA_3_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA3 = LA_3_filter_out[LA_3_filter_out.FT_Code.notnull()]
# LA3.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch7/Stockton_Summary.xlsx')

#Batch8

Final_merge.head(1000).to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch8/Batch8_codes_head.xlsx')
#
# LA_1_filter_query = Final_merge['LA'] == 'Sd'
# LA_1_filter = Final_merge[LA_1_filter_query]
# LA_1_filter_out = LA_1_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA1 = LA_1_filter_out[LA_1_filter_out.FT_Code.notnull()]
# LA1.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch8/Sunderland_Summary.xlsx')
#
# LA_2_filter_query = Final_merge['LA'] == 'Wk'
# LA_2_filter = Final_merge[LA_2_filter_query]
# LA_2_filter_out = LA_2_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA2 = LA_2_filter_out[LA_2_filter_out.FT_Code.notnull()]
# LA2.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch8/Wakefield_Summary.xlsx')
#
LA_3_filter_query = Final_merge['LA'] == 'WL'
LA_3_filter = Final_merge[LA_3_filter_query]
LA_3_filter_out = LA_3_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
LA3 = LA_3_filter_out[LA_3_filter_out.FT_Code.notnull()]
LA3.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch8/West_Lindsey_Summary.xlsx')
# #
# LA_4_filter_query = Final_merge['LA'] == 'Yr'
# LA_4_filter = Final_merge[LA_4_filter_query]
# LA_4_filter_out = LA_4_filter [['FT_Code', 'Designation', 'Feeder Type','wsp_circui','LA']]
# LA4 = LA_4_filter_out[LA_4_filter_out.FT_Code.notnull()]
# LA4.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Out/Batch8/York_Summary.xlsx')
