import pandas as pd

network_df = pd.read_csv (r'/Users/chrisryan/PycharmProjects/NPG/Master/Missing_FT_20201207/missing_ft_conduct_add.csv')
# network_df['wsp_circui'] = network_df['wsp_circui'].astype(float)
network_df = network_df[network_df.wsp_circui.notnull()]


#data inspect
#Unique = network_df.line_situation_actual.unique()
#print(Unique)

Total_length_filter = network_df.groupby('wsp_circui')["installed_length"].sum().reset_index(name="Total_Circuit_Length")


#Calculate Cable
Cabled_filter = network_df.loc[ (network_df['line_situation_actual'] =='SURFACE')|(network_df['line_situation_actual'] =='UNDERGROUND') ]
Cabled_Sum = Cabled_filter.groupby('wsp_circui')["installed_length"].sum().reset_index(name="Cabled_Length")

out = pd.merge (Total_length_filter,Cabled_Sum, how = 'left', left_on = ['wsp_circui'], right_on = ['wsp_circui'])


out ["Cabled_Average"] = out ['Cabled_Length']/out ['Total_Circuit_Length']*100

#Calculating Cab Code

out.loc[out["Cabled_Average"] < 50, 'FT_Code'] = '14'
out.loc[out["Cabled_Average"] >= 50, 'FT_Code'] = '15'


CAB_Table = out[['wsp_circui','Cabled_Average','FT_Code']]




CAB_Table.to_excel(r'/Users/chrisryan/PycharmProjects/NPG/Master/Missing_FT_20201207/ALL_Missing_FT_NEW.xlsx')