import pandas as pd
import os

CHUKWUDI_FEATURES = ['YYYY_MM', 'Crisis', 'Iso3', 'Ethnic Fractionalisation',
       'Size Of Excluded Ethnic Groups', 'Gender Inequality',
       'Income Gini Coefficient', 'Conflict Intensity',
       'Corruption Perception', 'Rule Of Law (Wgi)', 'Rule Of Law (Bti)',
       '# Of Different Types Of Affected Population Groups',
       '% Of People In None/Minimal Conditions - Level 1',
       '% Of People In Stressed Conditions - Level 2',
       '% Of People In Moderate Conditions - Level 3',
       '% Of People Severe Conditions - Level 4',
       '% Of People Extreme Conditions - Level 5', 'Total Population [Figure]',
       'Total Population [Reliability Score]', 'Landmass Affected [Figure]',
       'Landmass Affected [Reliability Score]', 'People Exposed [Figure]',
       'People Exposed [Reliability Score]', 'People Displaced [Figure]',
       'People Displaced [Reliability Score]', 'Injuries Reported [Figure]',
       'Injuries Reported [Reliability Score]',
       'Illness Cases Reported [Figure]',
       'Illness Cases Reported [Reliability Score]',
       'Buildings Damaged [Figure]', 'Buildings Damaged [Reliability Score]',
       'Buildings Destroyed [Figure]',
       'Buildings Destroyed [Reliability Score]', 'Economic Losses [Figure]',
       'Economic Losses [Reliability Score]',
       'Minimal Humanitarian Conditions - Level 1 [Figure]',
       'Minimal Humanitarian Conditions - Level 1 [Reliability Score]',
       'Stressed Humanitarian Conditions - Level 2 [Figure]',
       'Stressed Humanitarian Conditions - Level 2 [Reliability Score]',
       'Moderate Humanitarian Conditions - Level 3 [Figure]',
       'Moderate Humanitarian Conditions - Level 3 [Reliability Score]',
       'Severe Humanitarian Conditions - Level 4 [Figure]',
       'Severe Humanitarian Conditions - Level 4 [Reliability Score]',
       'Extreme Humanitarian Conditions - Level 5 [Figure]',
       'Extreme Humanitarian Conditions - Level 5 [Reliability Score]',
       'Fatalities In All Crises [Figure]',
       'Fatalities In All Crises [Reliability Score]',
       'Crisis Affected Groups [Figure]',
       'Crisis Affected Groups [Reliability Score]',
       'People Facing Limited Access Constraints [Figure]',
       'People Facing Limited Access Constraints [Reliability Score]',
       'People Facing Restricted Access Constraints [Figure]',
       'People Facing Restricted Access Constraints [Reliability Score]',
       'Impediments To Entry Into Country (Bureaucratic And Administrative) [Figure]',
       'Impediments To Entry Into Country (Bureaucratic And Administrative) [Reliability Score]',
       'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Figure]',
       'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Reliability Score]',
       'Interference Into Implementation Of Humanitarian Activities [Figure]',
       'Interference Into Implementation Of Humanitarian Activities [Reliability Score]',
       'Violence Against Personnel, Facilities And Assets [Figure]',
       'Violence Against Personnel, Facilities And Assets [Reliability Score]',
       'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Figure]',
       'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Reliability Score]',
       'Restriction And Obstruction Of Access To Services And Assistance [Figure]',
       'Restriction And Obstruction Of Access To Services And Assistance [Reliability Score]',
       'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Figure]',
       'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Reliability Score]',
       'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Figure]',
       'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Reliability Score]',
       'Data Reliability', 'Information Gaps (# Indicator Missing)',
       '% Of Total Area Affected',
       '% Of Total Population Living In The Affected Area',
       '% Of People Affected On The Total Population Exposed',
       '% Of Fatalities On The Total Population Affected',
       'Inform Severity Category', 'Trend (Last 3 Months)', 'Regions',
       'Updated_Score',
       'Presence Of Mines And Improvised Explosive Devices [Figure]',
       'Presence Of Mines And Improvised Explosive Devices [Reliability Score]',
       'Connected Crises', 'Geoscope', 'Adm1', 'Drivers',
       '% Of Total Population Displaced On The Total Population Affected']

file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(file_path)
directory_path = directory_path[:directory_path.find("\ACAPS")+7]
data_path = os.path.join(directory_path, 'data\\INFORM_Suite\\INFORM_Severity\\EuroCom_INFORM_Severity_Data\\Yearly_merged_data\\all_features\\combined_data_outer.csv')
data = pd.read_csv(data_path)[CHUKWUDI_FEATURES]

print(data.info())

"""import os

# Get the absolute path of the Python file
file_path = os.path.abspath(__file__)

# Get the directory of the Python file
directory_path = os.path.dirname(file_path)

print("Full path to the folder:", directory_path[:directory_path.find("\ACAPS")+7])
"""