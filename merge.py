import pandas as pd
import numpy as np
pd.set_option("display.max_columns", None)
df = pd.DataFrame(np.random.rand(10, 4), 
                  columns=('col_1', 'col_2', 'col_3', 'col_4'))

dfCovid = pd.read_csv (r'covid_19_data.csv')
dfMobilityReport = pd.read_csv(r'Global_Mobility_Report.csv')
dfVaccines = pd.read_csv(r'time_series_covid19_vaccine_global.csv')
#merged = pd.read_csv (r'merged.csv')
#dfCovid  = dfCovid.replace(to_replace =["US"], value ="United States")
dfCovid  = dfCovid.replace(to_replace =["UK"], 
                            value ="United Kingdom")
#print(dfCovid[dfCovid['Country/Region'] == "China"])
#print(dfMobilityReport[dfMobilityReport['country_region'] == "Mainland China"])

dfCovid['ObservationDate'] = dfCovid['ObservationDate'].astype('datetime64[ns]')
dfMobilityReport['date'] = dfMobilityReport['date'].astype('datetime64[ns]')
dfMobilityReport['date'] = dfMobilityReport['date'] + pd.DateOffset(days=1)
dfVaccines['Date'] = dfVaccines['Date'].astype('datetime64[ns]')
dfVaccines['Date'] = dfVaccines['Date'] + pd.DateOffset(days=1)
#print(dfMobilityReport)
meanData = dfMobilityReport.groupby(['date', 'country_region', 'sub_region_1']).mean()
#dfVaccines = dfVaccines.groupby(["Date", "Country_Region"]).mean()
#print(meanData.head())
#meanData.to_csv('mean.csv')

merged_df = pd.merge(dfCovid, meanData, left_on=["ObservationDate","Country/Region","Province/State"], right_on=["date","country_region","sub_region_1"])
#merged_df.info()
#print(merged_df)
merged_df.drop('census_fips_code', inplace=True, axis=1)
merged_df.drop('Last Update', inplace=True, axis=1)

#merged_df.to_csv('merged.csv')
merged_df.sort_values(by=['ObservationDate'], inplace=True, ascending=True)
merged_df.dropna(axis=0, how='any', inplace=True)

dfVaccines = dfVaccines.groupby(["Date", "Country_Region"]).mean()
withVaccines = pd.merge(merged_df, dfVaccines, left_on=["ObservationDate","Country/Region"], right_on=["Date","Country_Region"], how="left", indicator=True)
withVaccines['Doses_admin'] = withVaccines['Doses_admin'].fillna(0)
withVaccines['People_partially_vaccinated'] = withVaccines['People_partially_vaccinated'].fillna(0)
withVaccines['People_fully_vaccinated'] = withVaccines['People_fully_vaccinated'].fillna(0)
withVaccines.drop('_merge', inplace=True, axis=1)
withVaccines.drop('UID', inplace=True, axis=1)
withVaccines.to_csv('withVaccinesV2.csv')
#withVaccines.groupby(["Country/Region","Province/State"], as_index=False).mean()["Country/Region", "Province/State"]
#withVaccines.to_csv('withVaccinesCountriesList.csv')
#withVaccines.info()