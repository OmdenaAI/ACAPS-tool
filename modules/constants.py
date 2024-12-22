DEFAULT_CHOICE = 0

CONTRIBUTORS = [
    ["Irene Sam", "https://www.linkedin.com/in/isam007/"],
    ["Soumyadeep Bose", "https://www.linkedin.com/in/soumyadeepbose/"],
    ["Dimitra Muni", "https://www.linkedin.com/in/dimitramuni/"],
    ["Raj Shah", "https://www.linkedin.com/in/raj-shah-8522a2225/"],
    ["Ahmedullah", "https://www.linkedin.com/in/ahmedullah-ahmed-4b7920165/"],
    ["Chukwudi Emmanuel Asibe", "https://www.linkedin.com/in/emmanuel-asibe-19846117a/"],
    ["Gagana M D", "https://www.linkedin.com/in/gaganamd/"],
    ["Beatrice Kemboi", "https://www.linkedin.com/in/beatrice-kemboi-505b0a95/"],
    ["Jidhnyasaa Mahajan", "https://www.linkedin.com/in/jidhnyasaa/"],
    ["Kinsley Gitonga", "https://www.linkedin.com/in/kinsley-kaimenyi-ai-ml-engineer"],
    ["Viktor Ivanenko", "https://www.linkedin.com/in/viktor-ivanenko-b8504ba5/"],
    ["Arezoo Memarian", "https://www.linkedin.com/in/arezoo-memarian-phd/"],

]

TWEETS_COLUMNS_LIST = [
    "id",
    "url",
    "text",
    "createdAt",
    "retweetCount",
    "replyCount",
    "likeCount",
    "quoteCount",
    "bookmarkCount",
    "author_name",
    "author_followers",
    "author_isVerified",
    "author_userName",
    "author_profilePicture",
    "author_location",
    "author_createdAt",
    "author_statusesCount",
    "author_following",
    "author_favouritesCount",
    "author_isBlueVerified"
]

LANGUAGES = [
        "English",
        "Japanese",
        "Chinese",
        "German",
        "Hindi",
        "French",
        "Korean",
        "Portuguese",
        "Italian",
        "Spanish",
        "Indonesian",
        "Dutch",
        "Turkish",
        "Filipino",
        "Polish",
        "Swedish",
        "Bulgarian",
        "Romanian",
        "Arabic",
        "Czech",
        "Greek",
        "Finnish",
        "Croatian",
        "Malay",
        "Slovak",
        "Danish",
        "Tamil",
        "Ukrainian",
        "Russian",
        "Hungarian",
        "Norwegian",
        "Vietnamese"
    ]

LSTM_FEATURES = ['YYYY_MM', 'Crisis Id', 'Crisis', 'Country', 'Iso3', 'Empowerment', 'Bti - Democracy Status', 'Trust In Society', 'Ethnic Fractionalisation', 'Size Of Excluded Ethnic Groups', 'Gender Inequality', 'Income Gini Coefficient', 'Inequality', 'Social Cohesion', 'Conflict Intensity', 'Total Killed In All Crisis', 'Safety And Security', 'Corruption Perception', 'Rule Of Law (Wgi)', 'Rule Of Law (Bti)', 'Freedom In The World', 'Rule Of Law', 'Society And Safety', '# Of Different Types Of Affected Population Groups', 'Diversity Of Groups Affected', 'Impediments To Entry Into Country (Bureaucratic And Administrative)', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions)', 'Interference Into Implementation Of Humanitarian Activities', 'Violence Against Personnel, Facilities And Assets', 'Access Of Humanitarian Actors To Affected Populations', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance', 'Restriction And Obstruction Of Access To Services And Assistance', 'Access Of People In Need To Aid', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance', 'Presence Of Mines And Improvised Explosive Devices ', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.)', 'Physical And Security Constraints', 'Humanitarian Access', 'Operating Environment', '# Of People In None/Minimal Conditions - Level 1', '# Of People In Stressed Conditions - Level 2', '# Of People In Moderate Conditions - Level 3', '# Of People Severe Conditions - Level 4', '# Of People Extreme Conditions - Level 5', 'People In Need', '% Of People In None/Minimal Conditions - Level 1', '% Of People In Stressed Conditions - Level 2', '% Of People In Moderate Conditions - Level 3', '% Of People Severe Conditions - Level 4', '% Of People Extreme Conditions - Level 5', 'Concentration Of Conditions', 'Conditions Of People Affected', 'Total Population [Helper 0]', 'Total Population [Figure]', 'Total Population [Source]', 'Total Population [Reliability]', 'Total Population [Reliability Score]', 'Total Population [Justification]', 'Total Population [Link]', 'Total Population [Date]', 'Landmass Affected [Helper 1]', 'Landmass Affected [Figure]', 'Landmass Affected [Source]', 'Landmass Affected [Reliability]', 'Landmass Affected [Reliability Score]', 'Landmass Affected [Justification]', 'Landmass Affected [Link]', 'Landmass Affected [Date]', 'People Exposed [Helper 2]', 'People Exposed [Figure]', 'People Exposed [Source]', 'People Exposed [Reliability]', 'People Exposed [Reliability Score]', 'People Exposed [Justification]', 'People Exposed [Link]', 'People Exposed [Date]', 'People Affected [Helper 3]', 'People Affected [Figure]', 'People Affected [Source]', 'People Affected [Reliability]', 'People Affected [Reliability Score]', 'People Affected [Justification]', 'People Affected [Link]', 'People Affected [Date]', 'People Displaced [Helper 4]', 'People Displaced [Figure]', 'People Displaced [Source]', 'People Displaced [Reliability]', 'People Displaced [Reliability Score]', 'People Displaced [Justification]', 'People Displaced [Link]', 'People Displaced [Date]', 'Injuries Reported [Helper 5]', 'Injuries Reported [Figure]', 'Injuries Reported [Source]', 'Injuries Reported [Reliability]', 'Injuries Reported [Reliability Score]', 'Injuries Reported [Justification]', 'Injuries Reported [Link]', 'Injuries Reported [Date]', 'Illness Cases Reported [Helper 6]', 'Illness Cases Reported [Figure]', 'Illness Cases Reported [Source]', 'Illness Cases Reported [Reliability]', 'Illness Cases Reported [Reliability Score]', 'Illness Cases Reported [Justification]', 'Illness Cases Reported [Link]', 'Illness Cases Reported [Date]', 'Fatalities Reported [Helper 7]', 'Fatalities Reported [Figure]', 'Fatalities Reported [Source]', 'Fatalities Reported [Reliability]', 'Fatalities Reported [Reliability Score]', 'Fatalities Reported [Justification]', 'Fatalities Reported [Link]', 'Fatalities Reported [Date]', 'Buildings Damaged [Helper 8]', 'Buildings Damaged [Figure]', 'Buildings Damaged [Source]', 'Buildings Damaged [Reliability]', 'Buildings Damaged [Reliability Score]', 'Buildings Damaged [Justification]', 'Buildings Damaged [Link]', 'Buildings Damaged [Date]', 'Buildings Destroyed [Helper 9]', 'Buildings Destroyed [Figure]', 'Buildings Destroyed [Source]', 'Buildings Destroyed [Reliability]', 'Buildings Destroyed [Reliability Score]', 'Buildings Destroyed [Justification]', 'Buildings Destroyed [Link]', 'Buildings Destroyed [Date]', 'Buildings In The Affected Area [Helper 10]', 'Buildings In The Affected Area [Figure]', 'Buildings In The Affected Area [Source]', 'Buildings In The Affected Area [Reliability]', 'Buildings In The Affected Area [Reliability Score]', 'Buildings In The Affected Area [Justification]', 'Buildings In The Affected Area [Link]', 'Buildings In The Affected Area [Date]', 'Economic Losses [Helper 11]', 'Economic Losses [Figure]', 'Economic Losses [Source]', 'Economic Losses [Reliability]', 'Economic Losses [Reliability Score]', 'Economic Losses [Justification]', 'Economic Losses [Link]', 'Economic Losses [Date]', 'People In Need [Helper 12]', 'People In Need [Figure]', 'People In Need [Source]', 'People In Need [Reliability]', 'People In Need [Reliability Score]', 'People In Need [Justification]', 'People In Need [Link]', 'People In Need [Date]', 'Minimal Humanitarian Conditions - Level 1 [Helper 13]', 'Minimal Humanitarian Conditions - Level 1 [Figure]', 'Minimal Humanitarian Conditions - Level 1 [Source]', 'Minimal Humanitarian Conditions - Level 1 [Reliability]', 'Minimal Humanitarian Conditions - Level 1 [Reliability Score]', 'Minimal Humanitarian Conditions - Level 1 [Justification]', 'Minimal Humanitarian Conditions - Level 1 [Link]', 'Minimal Humanitarian Conditions - Level 1 [Date]', 'Stressed Humanitarian Conditions - Level 2 [Helper 14]', 'Stressed Humanitarian Conditions - Level 2 [Figure]', 'Stressed Humanitarian Conditions - Level 2 [Source]', 'Stressed Humanitarian Conditions - Level 2 [Reliability]', 'Stressed Humanitarian Conditions - Level 2 [Reliability Score]', 'Stressed Humanitarian Conditions - Level 2 [Justification]', 'Stressed Humanitarian Conditions - Level 2 [Link]', 'Stressed Humanitarian Conditions - Level 2 [Date]', 'Moderate Humanitarian Conditions - Level 3 [Helper 15]', 'Moderate Humanitarian Conditions - Level 3 [Figure]', 'Moderate Humanitarian Conditions - Level 3 [Source]', 'Moderate Humanitarian Conditions - Level 3 [Reliability]', 'Moderate Humanitarian Conditions - Level 3 [Reliability Score]', 'Moderate Humanitarian Conditions - Level 3 [Justification]', 'Moderate Humanitarian Conditions - Level 3 [Link]', 'Moderate Humanitarian Conditions - Level 3 [Date]', 'Severe Humanitarian Conditions - Level 4 [Helper 16]', 'Severe Humanitarian Conditions - Level 4 [Figure]', 'Severe Humanitarian Conditions - Level 4 [Source]', 'Severe Humanitarian Conditions - Level 4 [Reliability]', 'Severe Humanitarian Conditions - Level 4 [Reliability Score]', 'Severe Humanitarian Conditions - Level 4 [Justification]', 'Severe Humanitarian Conditions - Level 4 [Link]', 'Severe Humanitarian Conditions - Level 4 [Date]', 'Extreme Humanitarian Conditions - Level 5 [Helper 17]', 'Extreme Humanitarian Conditions - Level 5 [Figure]', 'Extreme Humanitarian Conditions - Level 5 [Source]', 'Extreme Humanitarian Conditions - Level 5 [Reliability]', 'Extreme Humanitarian Conditions - Level 5 [Reliability Score]', 'Extreme Humanitarian Conditions - Level 5 [Justification]', 'Extreme Humanitarian Conditions - Level 5 [Link]', 'Extreme Humanitarian Conditions - Level 5 [Date]', 'Fatalities In All Crises [Helper 18]', 'Fatalities In All Crises [Figure]', 'Fatalities In All Crises [Source]', 'Fatalities In All Crises [Reliability]', 'Fatalities In All Crises [Reliability Score]', 'Fatalities In All Crises [Justification]', 'Fatalities In All Crises [Link]', 'Fatalities In All Crises [Date]', 'Crisis Affected Groups [Helper 19]', 'Crisis Affected Groups [Figure]', 'Crisis Affected Groups [Source]', 'Crisis Affected Groups [Reliability]', 'Crisis Affected Groups [Reliability Score]', 'Crisis Affected Groups [Justification]', 'Crisis Affected Groups [Link]', 'Crisis Affected Groups [Date]', 'People Facing Limited Access Constraints [Helper 20]', 'People Facing Limited Access Constraints [Figure]', 'People Facing Limited Access Constraints [Source]', 'People Facing Limited Access Constraints [Reliability]', 'People Facing Limited Access Constraints [Reliability Score]', 'People Facing Limited Access Constraints [Justification]', 'People Facing Limited Access Constraints [Link]', 'People Facing Limited Access Constraints [Date]', 'People Facing Restricted Access Constraints [Helper 21]', 'People Facing Restricted Access Constraints [Figure]', 'People Facing Restricted Access Constraints [Source]', 'People Facing Restricted Access Constraints [Reliability]', 'People Facing Restricted Access Constraints [Reliability Score]', 'People Facing Restricted Access Constraints [Justification]', 'People Facing Restricted Access Constraints [Link]', 'People Facing Restricted Access Constraints [Date]', 'Impediments To Entry Into Country (Bureaucratic And Administrative) [Helper 22]', 'Impediments To Entry Into Country (Bureaucratic And Administrative) [Figure]', 'Impediments To Entry Into Country (Bureaucratic And Administrative) [Source]', 'Impediments To Entry Into Country (Bureaucratic And Administrative) [Reliability]', 'Impediments To Entry Into Country (Bureaucratic And Administrative) [Reliability Score]', 'Impediments To Entry Into Country (Bureaucratic And Administrative) [Justification]', 'Impediments To Entry Into Country (Bureaucratic And Administrative) [Link]', 'Impediments To Entry Into Country (Bureaucratic And Administrative) [Date]', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Helper 23]', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Figure]', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Source]', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Reliability]', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Reliability Score]', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Justification]', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Link]', 'Restriction Of Movement (Impediments To Freedom Of Movement And/Or Administrative Restrictions) [Date]', 'Interference Into Implementation Of Humanitarian Activities [Helper 24]', 'Interference Into Implementation Of Humanitarian Activities [Figure]', 'Interference Into Implementation Of Humanitarian Activities [Source]', 'Interference Into Implementation Of Humanitarian Activities [Reliability]', 'Interference Into Implementation Of Humanitarian Activities [Reliability Score]', 'Interference Into Implementation Of Humanitarian Activities [Justification]', 'Interference Into Implementation Of Humanitarian Activities [Link]', 'Interference Into Implementation Of Humanitarian Activities [Date]', 'Violence Against Personnel, Facilities And Assets [Helper 25]', 'Violence Against Personnel, Facilities And Assets [Figure]', 'Violence Against Personnel, Facilities And Assets [Source]', 'Violence Against Personnel, Facilities And Assets [Reliability]', 'Violence Against Personnel, Facilities And Assets [Reliability Score]', 'Violence Against Personnel, Facilities And Assets [Justification]', 'Violence Against Personnel, Facilities And Assets [Link]', 'Violence Against Personnel, Facilities And Assets [Date]', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Helper 26]', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Figure]', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Source]', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Reliability]', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Reliability Score]', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Justification]', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Link]', 'Denial Of Existence Of Humanitarian Needs Or Entitlements To Assistance [Date]', 'Restriction And Obstruction Of Access To Services And Assistance [Helper 27]', 'Restriction And Obstruction Of Access To Services And Assistance [Figure]', 'Restriction And Obstruction Of Access To Services And Assistance [Source]', 'Restriction And Obstruction Of Access To Services And Assistance [Reliability]', 'Restriction And Obstruction Of Access To Services And Assistance [Reliability Score]', 'Restriction And Obstruction Of Access To Services And Assistance [Justification]', 'Restriction And Obstruction Of Access To Services And Assistance [Link]', 'Restriction And Obstruction Of Access To Services And Assistance [Date]', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Helper 28]', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Figure]', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Source]', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Reliability]', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Reliability Score]', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Justification]', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Link]', 'Ongoing Insecurity/Hostilities Affecting Humanitarian Assistance [Date]', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Helper 30]', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Figure]', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Source]', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Reliability]', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Reliability Score]', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Comment]', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Link]', 'Physical Constraints In The Environment (Obstacles Related To Terrain, Climate, Lack Of Infrastructure, Etc.) [Date]', 'Ethnic Fractionalisation Index [2017] [Index]', 'Empowerment Rights Index [2011] [Index]', 'Bti - Democracy Status [2020] [Index]', 'Gender Inequality Index [2018] [Index]', 'People Killed In All Crises [2020] [Number]', 'Rule Of Law (Wgi) [2019] [Index]', 'Rule Of Law (Bti) [2020] [Index]', 'Freedom In The World Index [2020] [Index]', 'Cpi [2019] [Index]', 'Total Population [2020] [Number]', 'Land Area (Sq. Km) [Nan] [Sq. Km]', 'Landmass Affected By Disaster [Sq. Km]', 'People Living In The Affected Area [Number]', 'Total # Of People Affected By The Crisis [Number]', 'Total # Of Crisis Related Displaced People [Number]', 'Total # Of Crisis Related Injuries [Number]', 'Total # Of Illness Cases Reported', 'Total # Of Crisis Related Fatalities [Number]', 'Building Partially Damaged [Number]', 'Building Totally Damaged [Number]', 'Total Building In The Affected Area [Number]', 'Econimic Losses [Million Usd]', '# Of People Affected Facing Minimal Humanitarian Needs (Level 1) [Number]', '# Of People Affected Facing Stressed Humanitarian Needs (Level 2) [Number]', '# Of People Affected Facing Moderate Humanitarian Conditions And Needs (Level 3) [Number]', '# Of People Affected Facing Severe Humanitarian Conditions And Needs (Level 4) [Number]', '# Of People Affected Facing Extreme Humanitarian Conditions And Needs (Level 5) [Number]', '# Of Groups Affected By Crisis [Number]', 'People In Need Facing Limited Access Constraints [Number]', 'People In Need Facing Restricted Access Constraints [Number]', 'Glidenumber', 'Severityglidenumber', 'Region', 'Crisis Description', 'Website Name', 'Starting Date', 'Duration (Days)', 'Data Reliability', 'Information Gaps (# Indicator Missing)', 'Impact Of The Crisis', 'Area Affected', 'People In The Affected Area', 'Geographical', 'People Affected', 'People Displaced', 'Crisis Related Fatalities', 'People Affected By Categories', 'Human', '# Of People Facing Minimal Humanitarian Needs (Level 1)', '# Of People Facing Stressed Humanitarian Conditions And Needs (Level 2)', '# Of People Facing Moderate Humanitarian Conditions And Needs (Level 3)', '# Of People Facing Severe Humanitarian Conditions And Needs (Level 4)', '# Of People Facing Extreme Humanitarian Conditions And Needs (Level 5)', 'Complexity Of The Crisis', 'Area Affected - Absolute', '% Of Total Area Affected', 'Area Affected - Relative', 'People Living In The Affected Area - Absolute', '% Of Total Population Living In The Affected Area', 'People Living In The Affected Area - Relative', 'People Affected - Absolute', '% Of People Affected On The Total Population Exposed', 'People Affected - Relative', 'People Displaced - Absolute', 'People Displaced - Relative', 'Fatalities - Absolute', '% Of Fatalities On The Total Population Affected', 'Fatalities (Relative)', 'Inform Severity Index', 'Inform Severity Category', 'Trend (Last 3 Months)', 'Reliability', 'Regions', 'Last Updated', 'Country Level', 'Indicator', 'Type Of Entry', 'Total Sq.Km.', 'Total Population [Index]', 'Ethnic Fractionalisation Index [%]', 'Empowerment Rights Index [Index]', 'Size Of Excluded Ethnic Groups [Index]', 'Bti - Democracy Status [Index]', 'Gender Inequality Index [Index]', 'Income Gini Coefficient [Number]', 'Conflict Intensity (Hiik) [Index]', 'People Killed In All Crises [Index]', 'Rule Of Law (Wgi) [Index]', 'Rule Of Law (Bti) [Index]', 'Freedom In The World Index [Number]', 'Cpi [Sq. Km]', 'Reliability Index', 'Recentness Data', 'Information Gaps', 'Recentness Data (# Days)', 'Area Affected By Disaster', 'People Living In The Affected Area', 'Total # Of People Affected By The Crisis', 'Total # Of Crisis Related Displaced People', 'Total # Of Crisis Related Fatalities', '# Of People Affected Facing Minimal Humanitarian Needs (Level 1)', '# Of People Affected Facing Stressed Humanitarian Needs (Level 2)', '# Of People Affected Facing Moderate Humanitarian Conditions And Needs (Level 3)', '# Of People Affected Facing Severe Humanitarian Conditions And Needs (Level 4)', '# Of People Affected Facing Extreme Humanitarian Conditions And Needs (Level 5)', 'Updated_Score']

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

COUNTRIES = [
    {
        "country": "Grenada",
        "capital": "St. George's",
        "latitude": 32.38,
        "longitude": -64.68,
        "iso_alpha": "GRD"
    },
    {
        "country": "Switzerland",
        "capital": "Bern",
        "latitude": 46.92,
        "longitude": 7.47,
        "iso_alpha": "CHE"
    },
    {
        "country": "Sierra Leone",
        "capital": "Freetown",
        "latitude": 8.48,
        "longitude": -13.23,
        "iso_alpha": "SLE"
    },
    {
        "country": "Hungary",
        "capital": "Budapest",
        "latitude": 47.5,
        "longitude": 19.08,
        "iso_alpha": "HUN"
    },
    {
        "country": "Taiwan",
        "capital": "Taipei",
        "latitude": 25.03,
        "longitude": 121.52,
        "iso_alpha": "TWN"
    },
    {
        "country": "Barbados",
        "capital": "Bridgetown",
        "latitude": 13.1,
        "longitude": -59.62,
        "iso_alpha": "BRB"
    },
    {
        "country": "Tunisia",
        "capital": "Tunis",
        "latitude": 36.8,
        "longitude": 10.18,
        "iso_alpha": "TUN"
    },
    {
        "country": "Italy",
        "capital": "Rome",
        "latitude": 41.9,
        "longitude": 12.48,
        "iso_alpha": "ITA"
    },
    {
        "country": "Benin",
        "capital": "Porto-Novo",
        "latitude": 6.48,
        "longitude": 2.62,
        "iso_alpha": "BEN"
    },
    {
        "country": "Indonesia",
        "capital": "Jakarta",
        "latitude": -6.17,
        "longitude": 106.82,
        "iso_alpha": "IDN"
    },
    {
        "country": "Saint Kitts and Nevis",
        "capital": "Basseterre",
        "latitude": 17.3,
        "longitude": -62.72,
        "iso_alpha": "KNA"
    },
    {
        "country": "Laos",
        "capital": "Vientiane",
        "latitude": 17.97,
        "longitude": 102.6,
        "iso_alpha": "LAO"
    },
    {
        "country": "Uganda",
        "capital": "Kampala",
        "latitude": 0.32,
        "longitude": 32.55,
        "iso_alpha": "UGA"
    },
    {
        "country": "Andorra",
        "capital": "Andorra la Vella",
        "latitude": 42.5,
        "longitude": 1.52,
        "iso_alpha": "AND"
    },
    {
        "country": "Burundi",
        "capital": "Gitega",
        "latitude": -3.43,
        "longitude": 29.93,
        "iso_alpha": "BDI"
    },
    {
        "country": "South Africa",
        "capital": "Pretoria",
        "latitude": -25.7,
        "longitude": 28.22,
        "iso_alpha": "ZAF"
    },
    {
        "country": "France",
        "capital": "Paris",
        "latitude": 48.87,
        "longitude": 2.33,
        "iso_alpha": "FRA"
    },
    {
        "country": "Libya",
        "capital": "Tripoli",
        "latitude": 32.88,
        "longitude": 13.17,
        "iso_alpha": "LBY"
    },
    {
        "country": "Mexico",
        "capital": "Mexico City",
        "latitude": 19.43,
        "longitude": -99.13,
        "iso_alpha": "MEX"
    },
    {
        "country": "Gabon",
        "capital": "Libreville",
        "latitude": 0.38,
        "longitude": 9.45,
        "iso_alpha": "GAB"
    },
    {
        "country": "North Macedonia",
        "capital": "Skopje",
        "latitude": 42.0,
        "longitude": 21.43,
        "iso_alpha": "MKD"
    },
    {
        "country": "China",
        "capital": "Beijing",
        "latitude": 39.92,
        "longitude": 116.38,
        "iso_alpha": "CHN"
    },
    {
        "country": "Yemen",
        "capital": "Sana'a",
        "latitude": 15.37,
        "longitude": 44.19,
        "iso_alpha": "YEM"
    },
    {
        "country": "Solomon Islands",
        "capital": "Honiara",
        "latitude": -9.43,
        "longitude": 159.95,
        "iso_alpha": "SLB"
    },
    {
        "country": "Uzbekistan",
        "capital": "Tashkent",
        "latitude": 41.32,
        "longitude": 69.25,
        "iso_alpha": "UZB"
    },
    {
        "country": "Egypt",
        "capital": "Cairo",
        "latitude": 30.05,
        "longitude": 31.25,
        "iso_alpha": "EGY"
    },
    {
        "country": "Senegal",
        "capital": "Dakar",
        "latitude": 14.73,
        "longitude": -17.63,
        "iso_alpha": "SEN"
    },
    {
        "country": "Sri Lanka",
        "capital": "Sri Jayawardenepura Kotte",
        "latitude": 6.89,
        "longitude": 79.9,
        "iso_alpha": "LKA"
    },
    {
        "country": "Bangladesh",
        "capital": "Dhaka",
        "latitude": 23.72,
        "longitude": 90.4,
        "iso_alpha": "BGD"
    },
    {
        "country": "Peru",
        "capital": "Lima",
        "latitude": -12.05,
        "longitude": -77.05,
        "iso_alpha": "PER"
    },
    {
        "country": "Singapore",
        "capital": "Singapore",
        "latitude": 1.28,
        "longitude": 103.85,
        "iso_alpha": "SGP"
    },
    {
        "country": "Turkey",
        "capital": "Ankara",
        "latitude": 39.93,
        "longitude": 32.87,
        "iso_alpha": "TUR"
    },
    {
        "country": "Afghanistan",
        "capital": "Kabul",
        "latitude": 34.52,
        "longitude": 69.18,
        "iso_alpha": "AFG"
    },
    {
        "country": "United Kingdom",
        "capital": "London",
        "latitude": 51.5,
        "longitude": -0.08,
        "iso_alpha": "GBR"
    },
    {
        "country": "Zambia",
        "capital": "Lusaka",
        "latitude": -15.42,
        "longitude": 28.28,
        "iso_alpha": "ZMB"
    },
    {
        "country": "Finland",
        "capital": "Helsinki",
        "latitude": 60.17,
        "longitude": 24.93,
        "iso_alpha": "FIN"
    },
    {
        "country": "Niger",
        "capital": "Niamey",
        "latitude": 13.52,
        "longitude": 2.12,
        "iso_alpha": "NER"
    },
    {
        "country": "Guinea-Bissau",
        "capital": "Bissau",
        "latitude": 11.85,
        "longitude": -15.58,
        "iso_alpha": "GNB"
    },
    {
        "country": "Azerbaijan",
        "capital": "Baku",
        "latitude": 40.38,
        "longitude": 49.87,
        "iso_alpha": "AZE"
    },
    {
        "country": "Djibouti",
        "capital": "Djibouti",
        "latitude": 11.58,
        "longitude": 43.15,
        "iso_alpha": "DJI"
    },
    {
        "country": "Mauritius",
        "capital": "Port Louis",
        "latitude": -20.15,
        "longitude": 57.48,
        "iso_alpha": "MUS"
    },
    {
        "country": "Colombia",
        "capital": "Bogot\u00e1",
        "latitude": 4.71,
        "longitude": -74.07,
        "iso_alpha": "COL"
    },
    {
        "country": "Greece",
        "capital": "Athens",
        "latitude": 37.98,
        "longitude": 23.73,
        "iso_alpha": "GRC"
    },
    {
        "country": "Croatia",
        "capital": "Zagreb",
        "latitude": 45.8,
        "longitude": 16.0,
        "iso_alpha": "HRV"
    },
    {
        "country": "Morocco",
        "capital": "Rabat",
        "latitude": 34.02,
        "longitude": -6.82,
        "iso_alpha": "MAR"
    },
    {
        "country": "Algeria",
        "capital": "Algiers",
        "latitude": 36.75,
        "longitude": 3.05,
        "iso_alpha": "DZA"
    },
    {
        "country": "Netherlands",
        "capital": "Amsterdam",
        "latitude": 52.35,
        "longitude": 4.92,
        "iso_alpha": "NLD"
    },
    {
        "country": "Sudan",
        "capital": "Khartoum",
        "latitude": 15.6,
        "longitude": 32.53,
        "iso_alpha": "SDN"
    },
    {
        "country": "Fiji",
        "capital": "Suva",
        "latitude": -18.13,
        "longitude": 178.42,
        "iso_alpha": "FJI"
    },
    {
        "country": "Liechtenstein",
        "capital": "Vaduz",
        "latitude": 47.13,
        "longitude": 9.52,
        "iso_alpha": "LIE"
    },
    {
        "country": "Nepal",
        "capital": "Kathmandu",
        "latitude": 27.72,
        "longitude": 85.32,
        "iso_alpha": "NPL"
    },
    {
        "country": "Georgia",
        "capital": "Tbilisi",
        "latitude": 41.68,
        "longitude": 44.83,
        "iso_alpha": "GEO"
    },
    {
        "country": "Pakistan",
        "capital": "Islamabad",
        "latitude": 33.68,
        "longitude": 73.05,
        "iso_alpha": "PAK"
    },
    {
        "country": "Monaco",
        "capital": "Monaco",
        "latitude": 43.73,
        "longitude": 7.42,
        "iso_alpha": "MCO"
    },
    {
        "country": "Botswana",
        "capital": "Gaborone",
        "latitude": -24.63,
        "longitude": 25.9,
        "iso_alpha": "BWA"
    },
    {
        "country": "Lebanon",
        "capital": "Beirut",
        "latitude": 33.87,
        "longitude": 35.5,
        "iso_alpha": "LBN"
    },
    {
        "country": "Papua New Guinea",
        "capital": "Port Moresby",
        "latitude": -9.45,
        "longitude": 147.18,
        "iso_alpha": "PNG"
    },
    {
        "country": "Dominican Republic",
        "capital": "Santo Domingo",
        "latitude": 18.47,
        "longitude": -69.9,
        "iso_alpha": "DOM"
    },
    {
        "country": "Qatar",
        "capital": "Doha",
        "latitude": 25.28,
        "longitude": 51.53,
        "iso_alpha": "QAT"
    },
    {
        "country": "Madagascar",
        "capital": "Antananarivo",
        "latitude": -18.92,
        "longitude": 47.52,
        "iso_alpha": "MDG"
    },
    {
        "country": "India",
        "capital": "New Delhi",
        "latitude": 28.6,
        "longitude": 77.2,
        "iso_alpha": "IND"
    },
    {
        "country": "Syria",
        "capital": "Damascus",
        "latitude": 33.5,
        "longitude": 36.3,
        "iso_alpha": "SYR"
    },
    {
        "country": "Montenegro",
        "capital": "Podgorica",
        "latitude": 42.43,
        "longitude": 19.27,
        "iso_alpha": "MNE"
    },
    {
        "country": "Eswatini",
        "capital": "Mbabane",
        "latitude": -26.32,
        "longitude": 31.13,
        "iso_alpha": "SWZ"
    },
    {
        "country": "Paraguay",
        "capital": "Asunci\u00f3n",
        "latitude": -25.28,
        "longitude": -57.57,
        "iso_alpha": "PRY"
    },
    {
        "country": "El Salvador",
        "capital": "San Salvador",
        "latitude": 13.7,
        "longitude": -89.2,
        "iso_alpha": "SLV"
    },
    {
        "country": "Ukraine",
        "capital": "Kyiv",
        "latitude": 50.43,
        "longitude": 30.52,
        "iso_alpha": "UKR"
    },
    {
        "country": "Namibia",
        "capital": "Windhoek",
        "latitude": -22.57,
        "longitude": 17.08,
        "iso_alpha": "NAM"
    },
    {
        "country": "United Arab Emirates",
        "capital": "Abu Dhabi",
        "latitude": 24.47,
        "longitude": 54.37,
        "iso_alpha": "ARE"
    },
    {
        "country": "Bulgaria",
        "capital": "Sofia",
        "latitude": 42.68,
        "longitude": 23.32,
        "iso_alpha": "BGR"
    },
    {
        "country": "Germany",
        "capital": "Berlin",
        "latitude": 52.52,
        "longitude": 13.4,
        "iso_alpha": "DEU"
    },
    {
        "country": "Cambodia",
        "capital": "Phnom Penh",
        "latitude": 11.55,
        "longitude": 104.92,
        "iso_alpha": "KHM"
    },
    {
        "country": "Iraq",
        "capital": "Baghdad",
        "latitude": 33.33,
        "longitude": 44.4,
        "iso_alpha": "IRQ"
    },
    {
        "country": "Sweden",
        "capital": "Stockholm",
        "latitude": 59.33,
        "longitude": 18.05,
        "iso_alpha": "SWE"
    },
    {
        "country": "Cuba",
        "capital": "Havana",
        "latitude": 23.12,
        "longitude": -82.35,
        "iso_alpha": "CUB"
    },
    {
        "country": "Kyrgyzstan",
        "capital": "Bishkek",
        "latitude": 42.87,
        "longitude": 74.6,
        "iso_alpha": "KGZ"
    },
    {
        "country": "Russia",
        "capital": "Moscow",
        "latitude": 55.75,
        "longitude": 37.6,
        "iso_alpha": "RUS"
    },
    {
        "country": "Malaysia",
        "capital": "Kuala Lumpur",
        "latitude": 3.17,
        "longitude": 101.7,
        "iso_alpha": "MYS"
    },
    {
        "country": "Cyprus",
        "capital": "Nicosia",
        "latitude": 35.17,
        "longitude": 33.37,
        "iso_alpha": "CYP"
    },
    {
        "country": "Canada",
        "capital": "Ottawa",
        "latitude": 45.42,
        "longitude": -75.7,
        "iso_alpha": "CAN"
    },
    {
        "country": "Malawi",
        "capital": "Lilongwe",
        "latitude": -13.97,
        "longitude": 33.78,
        "iso_alpha": "MWI"
    },
    {
        "country": "Saudi Arabia",
        "capital": "Riyadh",
        "latitude": 24.65,
        "longitude": 46.7,
        "iso_alpha": "SAU"
    },
    {
        "country": "Bosnia and Herzegovina",
        "capital": "Sarajevo",
        "latitude": 43.87,
        "longitude": 18.42,
        "iso_alpha": "BIH"
    },
    {
        "country": "Ethiopia",
        "capital": "Addis Ababa",
        "latitude": 9.03,
        "longitude": 38.7,
        "iso_alpha": "ETH"
    },
    {
        "country": "Spain",
        "capital": "Madrid",
        "latitude": 40.4,
        "longitude": -3.68,
        "iso_alpha": "ESP"
    },
    {
        "country": "Slovenia",
        "capital": "Ljubljana",
        "latitude": 46.05,
        "longitude": 14.52,
        "iso_alpha": "SVN"
    },
    {
        "country": "Oman",
        "capital": "Muscat",
        "latitude": 23.62,
        "longitude": 58.58,
        "iso_alpha": "OMN"
    },
    {
        "country": "San Marino",
        "capital": "City of San Marino",
        "latitude": 43.94,
        "longitude": 12.45,
        "iso_alpha": "SMR"
    },
    {
        "country": "Lesotho",
        "capital": "Maseru",
        "latitude": -29.32,
        "longitude": 27.48,
        "iso_alpha": "LSO"
    },
    {
        "country": "Marshall Islands",
        "capital": "Majuro",
        "latitude": 7.1,
        "longitude": 171.38,
        "iso_alpha": "MHL"
    },
    {
        "country": "Iceland",
        "capital": "Reykjavik",
        "latitude": 64.15,
        "longitude": -21.95,
        "iso_alpha": "ISL"
    },
    {
        "country": "Luxembourg",
        "capital": "Luxembourg",
        "latitude": 49.6,
        "longitude": 6.12,
        "iso_alpha": "LUX"
    },
    {
        "country": "Argentina",
        "capital": "Buenos Aires",
        "latitude": -34.58,
        "longitude": -58.67,
        "iso_alpha": "ARG"
    },
    {
        "country": "Nauru",
        "capital": "Yaren",
        "latitude": -0.55,
        "longitude": 166.92,
        "iso_alpha": "NRU"
    },
    {
        "country": "Dominica",
        "capital": "Roseau",
        "latitude": 15.3,
        "longitude": -61.4,
        "iso_alpha": "DMA"
    },
    {
        "country": "Costa Rica",
        "capital": "San Jos\u00e9",
        "latitude": 9.93,
        "longitude": -84.09,
        "iso_alpha": "CRI"
    },
    {
        "country": "Australia",
        "capital": "Canberra",
        "latitude": -35.27,
        "longitude": 149.13,
        "iso_alpha": "AUS"
    },
    {
        "country": "Thailand",
        "capital": "Bangkok",
        "latitude": 13.75,
        "longitude": 100.52,
        "iso_alpha": "THA"
    },
    {
        "country": "Haiti",
        "capital": "Port-au-Prince",
        "latitude": 18.53,
        "longitude": -72.33,
        "iso_alpha": "HTI"
    },
    {
        "country": "Tuvalu",
        "capital": "Funafuti",
        "latitude": -8.52,
        "longitude": 179.22,
        "iso_alpha": "TUV"
    },
    {
        "country": "Honduras",
        "capital": "Tegucigalpa",
        "latitude": 14.1,
        "longitude": -87.22,
        "iso_alpha": "HND"
    },
    {
        "country": "Equatorial Guinea",
        "capital": "Malabo",
        "latitude": 3.75,
        "longitude": 8.78,
        "iso_alpha": "GNQ"
    },
    {
        "country": "Saint Lucia",
        "capital": "Castries",
        "latitude": 14.0,
        "longitude": -61.0,
        "iso_alpha": "LCA"
    },
    {
        "country": "Belarus",
        "capital": "Minsk",
        "latitude": 53.9,
        "longitude": 27.57,
        "iso_alpha": "BLR"
    },
    {
        "country": "Latvia",
        "capital": "Riga",
        "latitude": 56.95,
        "longitude": 24.1,
        "iso_alpha": "LVA"
    },
    {
        "country": "Palau",
        "capital": "Ngerulmud",
        "latitude": 7.5,
        "longitude": 134.62,
        "iso_alpha": "PLW"
    },
    {
        "country": "Philippines",
        "capital": "Manila",
        "latitude": 14.6,
        "longitude": 120.97,
        "iso_alpha": "PHL"
    },
    {
        "country": "Denmark",
        "capital": "Copenhagen",
        "latitude": 55.67,
        "longitude": 12.58,
        "iso_alpha": "DNK"
    },
    {
        "country": "Cameroon",
        "capital": "Yaound\u00e9",
        "latitude": 3.85,
        "longitude": 11.5,
        "iso_alpha": "CMR"
    },
    {
        "country": "Guinea",
        "capital": "Conakry",
        "latitude": 9.5,
        "longitude": -13.7,
        "iso_alpha": "GIN"
    },
    {
        "country": "Bahrain",
        "capital": "Manama",
        "latitude": 26.23,
        "longitude": 50.57,
        "iso_alpha": "BHR"
    },
    {
        "country": "Suriname",
        "capital": "Paramaribo",
        "latitude": 5.83,
        "longitude": -55.17,
        "iso_alpha": "SUR"
    },
    {
        "country": "Somalia",
        "capital": "Mogadishu",
        "latitude": 2.07,
        "longitude": 45.33,
        "iso_alpha": "SOM"
    },
    {
        "country": "Vanuatu",
        "capital": "Port Vila",
        "latitude": -17.73,
        "longitude": 168.32,
        "iso_alpha": "VUT"
    },
    {
        "country": "Togo",
        "capital": "Lom\u00e9",
        "latitude": 6.14,
        "longitude": 1.21,
        "iso_alpha": "TGO"
    },
    {
        "country": "Kenya",
        "capital": "Nairobi",
        "latitude": -1.28,
        "longitude": 36.82,
        "iso_alpha": "KEN"
    },
    {
        "country": "Rwanda",
        "capital": "Kigali",
        "latitude": -1.95,
        "longitude": 30.05,
        "iso_alpha": "RWA"
    },
    {
        "country": "Estonia",
        "capital": "Tallinn",
        "latitude": 59.43,
        "longitude": 24.72,
        "iso_alpha": "EST"
    },
    {
        "country": "Romania",
        "capital": "Bucharest",
        "latitude": 44.43,
        "longitude": 26.1,
        "iso_alpha": "ROU"
    },
    {
        "country": "Trinidad and Tobago",
        "capital": "Port of Spain",
        "latitude": 10.65,
        "longitude": -61.52,
        "iso_alpha": "TTO"
    },
    {
        "country": "Guyana",
        "capital": "Georgetown",
        "latitude": 6.8,
        "longitude": -58.15,
        "iso_alpha": "GUY"
    },
    {
        "country": "Timor-Leste",
        "capital": "Dili",
        "latitude": -8.58,
        "longitude": 125.6,
        "iso_alpha": "TLS"
    },
    {
        "country": "Vietnam",
        "capital": "Hanoi",
        "latitude": 21.03,
        "longitude": 105.85,
        "iso_alpha": "VNM"
    },
    {
        "country": "Uruguay",
        "capital": "Montevideo",
        "latitude": -34.85,
        "longitude": -56.17,
        "iso_alpha": "URY"
    },
    {
        "country": "Vatican City",
        "capital": "Vatican City",
        "latitude": 41.9,
        "longitude": 12.45,
        "iso_alpha": "VAT"
    },
    {
        "country": "Austria",
        "capital": "Vienna",
        "latitude": 48.2,
        "longitude": 16.37,
        "iso_alpha": "AUT"
    },
    {
        "country": "Turkmenistan",
        "capital": "Ashgabat",
        "latitude": 37.95,
        "longitude": 58.38,
        "iso_alpha": "TKM"
    },
    {
        "country": "Mozambique",
        "capital": "Maputo",
        "latitude": -25.95,
        "longitude": 32.58,
        "iso_alpha": "MOZ"
    },
    {
        "country": "Panama",
        "capital": "Panama City",
        "latitude": 8.97,
        "longitude": -79.53,
        "iso_alpha": "PAN"
    },
    {
        "country": "Micronesia",
        "capital": "Palikir",
        "latitude": 6.92,
        "longitude": 158.15,
        "iso_alpha": "FSM"
    },
    {
        "country": "Ireland",
        "capital": "Dublin",
        "latitude": 53.32,
        "longitude": -6.23,
        "iso_alpha": "IRL"
    },
    {
        "country": "Norway",
        "capital": "Oslo",
        "latitude": 59.92,
        "longitude": 10.75,
        "iso_alpha": "NOR"
    },
    {
        "country": "Central African Republic",
        "capital": "Bangui",
        "latitude": 4.37,
        "longitude": 18.58,
        "iso_alpha": "CAF"
    },
    {
        "country": "Burkina Faso",
        "capital": "Ouagadougou",
        "latitude": 12.37,
        "longitude": -1.52,
        "iso_alpha": "BFA"
    },
    {
        "country": "Eritrea",
        "capital": "Asmara",
        "latitude": 15.33,
        "longitude": 38.93,
        "iso_alpha": "ERI"
    },
    {
        "country": "Tanzania",
        "capital": "Dodoma",
        "latitude": -6.16,
        "longitude": 35.75,
        "iso_alpha": "TZA"
    },
    {
        "country": "Jordan",
        "capital": "Amman",
        "latitude": 31.95,
        "longitude": 35.93,
        "iso_alpha": "JOR"
    },
    {
        "country": "Mauritania",
        "capital": "Nouakchott",
        "latitude": 18.07,
        "longitude": -15.97,
        "iso_alpha": "MRT"
    },
    {
        "country": "Lithuania",
        "capital": "Vilnius",
        "latitude": 54.68,
        "longitude": 25.32,
        "iso_alpha": "LTU"
    },
    {
        "country": "Slovakia",
        "capital": "Bratislava",
        "latitude": 48.15,
        "longitude": 17.12,
        "iso_alpha": "SVK"
    },
    {
        "country": "Angola",
        "capital": "Luanda",
        "latitude": -8.83,
        "longitude": 13.22,
        "iso_alpha": "AGO"
    },
    {
        "country": "Kazakhstan",
        "capital": "Nur-Sultan",
        "latitude": 51.16,
        "longitude": 71.45,
        "iso_alpha": "KAZ"
    },
    {
        "country": "Moldova",
        "capital": "Chi\u0219in\u0103u",
        "latitude": 47.01,
        "longitude": 28.9,
        "iso_alpha": "MDA"
    },
    {
        "country": "Mali",
        "capital": "Bamako",
        "latitude": 12.65,
        "longitude": -8.0,
        "iso_alpha": "MLI"
    },
    {
        "country": "Armenia",
        "capital": "Yerevan",
        "latitude": 40.17,
        "longitude": 44.5,
        "iso_alpha": "ARM"
    },
    {
        "country": "Samoa",
        "capital": "Apia",
        "latitude": -13.82,
        "longitude": -171.77,
        "iso_alpha": "WSM"
    },
    {
        "country": "Japan",
        "capital": "Tokyo",
        "latitude": 35.68,
        "longitude": 139.75,
        "iso_alpha": "JPN"
    },
    {
        "country": "Bolivia",
        "capital": "Sucre",
        "latitude": -19.02,
        "longitude": -65.26,
        "iso_alpha": "BOL"
    },
    {
        "country": "Chile",
        "capital": "Santiago",
        "latitude": -33.45,
        "longitude": -70.67,
        "iso_alpha": "CHL"
    },
    {
        "country": "United States",
        "capital": "Washington, D.C.",
        "latitude": 38.89,
        "longitude": -77.05,
        "iso_alpha": "USA"
    },
    {
        "country": "Saint Vincent and the Grenadines",
        "capital": "Kingstown",
        "latitude": 13.13,
        "longitude": -61.22,
        "iso_alpha": "VCT"
    },
    {
        "country": "Seychelles",
        "capital": "Victoria",
        "latitude": -4.62,
        "longitude": 55.45,
        "iso_alpha": "SYC"
    },
    {
        "country": "Guatemala",
        "capital": "Guatemala City",
        "latitude": 14.62,
        "longitude": -90.52,
        "iso_alpha": "GTM"
    },
    {
        "country": "Ecuador",
        "capital": "Quito",
        "latitude": -0.22,
        "longitude": -78.5,
        "iso_alpha": "ECU"
    },
    {
        "country": "Tajikistan",
        "capital": "Dushanbe",
        "latitude": 38.55,
        "longitude": 68.77,
        "iso_alpha": "TJK"
    },
    {
        "country": "Malta",
        "capital": "Valletta",
        "latitude": 35.88,
        "longitude": 14.5,
        "iso_alpha": "MLT"
    },
    {
        "country": "Gambia",
        "capital": "Banjul",
        "latitude": 13.45,
        "longitude": -16.57,
        "iso_alpha": "GMB"
    },
    {
        "country": "Nigeria",
        "capital": "Abuja",
        "latitude": 9.08,
        "longitude": 7.53,
        "iso_alpha": "NGA"
    },
    {
        "country": "Bahamas",
        "capital": "Nassau",
        "latitude": 25.08,
        "longitude": -77.35,
        "iso_alpha": "BHS"
    },
    {
        "country": "Kuwait",
        "capital": "Kuwait City",
        "latitude": 29.37,
        "longitude": 47.97,
        "iso_alpha": "KWT"
    },
    {
        "country": "Maldives",
        "capital": "Mal\u00e9",
        "latitude": 4.17,
        "longitude": 73.51,
        "iso_alpha": "MDV"
    },
    {
        "country": "South Sudan",
        "capital": "Juba",
        "latitude": 4.85,
        "longitude": 31.62,
        "iso_alpha": "SSD"
    },
    {
        "country": "Iran",
        "capital": "Tehran",
        "latitude": 35.7,
        "longitude": 51.42,
        "iso_alpha": "IRN"
    },
    {
        "country": "Albania",
        "capital": "Tirana",
        "latitude": 41.32,
        "longitude": 19.82,
        "iso_alpha": "ALB"
    },
    {
        "country": "Brazil",
        "capital": "Bras\u00edlia",
        "latitude": -15.79,
        "longitude": -47.88,
        "iso_alpha": "BRA"
    },
    {
        "country": "Serbia",
        "capital": "Belgrade",
        "latitude": 44.83,
        "longitude": 20.5,
        "iso_alpha": "SRB"
    },
    {
        "country": "Belize",
        "capital": "Belmopan",
        "latitude": 17.25,
        "longitude": -88.77,
        "iso_alpha": "BLZ"
    },
    {
        "country": "Myanmar",
        "capital": "Naypyidaw",
        "latitude": 19.76,
        "longitude": 96.07,
        "iso_alpha": "MMR"
    },
    {
        "country": "Bhutan",
        "capital": "Thimphu",
        "latitude": 27.47,
        "longitude": 89.63,
        "iso_alpha": "BTN"
    },
    {
        "country": "Venezuela",
        "capital": "Caracas",
        "latitude": 10.48,
        "longitude": -66.87,
        "iso_alpha": "VEN"
    },
    {
        "country": "Liberia",
        "capital": "Monrovia",
        "latitude": 6.3,
        "longitude": -10.8,
        "iso_alpha": "LBR"
    },
    {
        "country": "Jamaica",
        "capital": "Kingston",
        "latitude": 17.99702,
        "longitude": -76.79358,
        "iso_alpha": "JAM"
    },
    {
        "country": "Poland",
        "capital": "Warsaw",
        "latitude": 52.25,
        "longitude": 21.0,
        "iso_alpha": "POL"
    },
    {
        "country": "Brunei",
        "capital": "Bandar Seri Begawan",
        "latitude": 4.88,
        "longitude": 114.93,
        "iso_alpha": "BRN"
    },
    {
        "country": "Comoros",
        "capital": "Moroni",
        "latitude": -11.7,
        "longitude": 43.23,
        "iso_alpha": "COM"
    },
    {
        "country": "Tonga",
        "capital": "Nuku'alofa",
        "latitude": -21.13,
        "longitude": -175.2,
        "iso_alpha": "TON"
    },
    {
        "country": "Kiribati",
        "capital": "South Tarawa",
        "latitude": 1.33,
        "longitude": 172.98,
        "iso_alpha": "KIR"
    },
    {
        "country": "Ghana",
        "capital": "Accra",
        "latitude": 5.55,
        "longitude": -0.22,
        "iso_alpha": "GHA"
    },
    {
        "country": "Chad",
        "capital": "N'Djamena",
        "latitude": 12.1,
        "longitude": 15.03,
        "iso_alpha": "TCD"
    },
    {
        "country": "Zimbabwe",
        "capital": "Harare",
        "latitude": -17.82,
        "longitude": 31.03,
        "iso_alpha": "ZWE"
    },
    {
        "country": "Mongolia",
        "capital": "Ulan Bator",
        "latitude": 47.92,
        "longitude": 106.91,
        "iso_alpha": "MNG"
    },
    {
        "country": "Portugal",
        "capital": "Lisbon",
        "latitude": 38.72,
        "longitude": -9.13,
        "iso_alpha": "PRT"
    },
    {
        "country": "Belgium",
        "capital": "Brussels",
        "latitude": 50.83,
        "longitude": 4.33,
        "iso_alpha": "BEL"
    },
    {
        "country": "Israel",
        "capital": "Jerusalem",
        "latitude": 31.77,
        "longitude": 35.23,
        "iso_alpha": "ISR"
    },
    {
        "country": "New Zealand",
        "capital": "Wellington",
        "latitude": -41.3,
        "longitude": 174.78,
        "iso_alpha": "NZL"
    },
    {
        "country": "Nicaragua",
        "capital": "Managua",
        "latitude": 12.13,
        "longitude": -86.25,
        "iso_alpha": "NIC"
    }
]

SENTIMENT_TAGS = {
    'positive': 1,   # Positive sentiment
    'neutral': 0,    # Neutral sentiment
    'negative': -1   # Negative sentiment
}


TEXT_COLOR = {"positive": "green", "neutral": "gray", "negative": "red"}

SPANISH_STOP_WORDS = set([
    'a', 'acá', 'ahí', 'al', 'algo', 'algunas', 'algunos', 'allá', 'allí', 'ambos', 'ante', 'antes', 'aquel', 'aquellas', 
    'aquellos', 'aquí', 'arriba', 'así', 'atras', 'aun', 'aunque', 'bajo', 'bastante', 'bien', 'cada', 'casi', 'cerca', 
    'cierto', 'ciertos', 'como', 'con', 'conmigo', 'contigo', 'contra', 'cual', 'cuales', 'cuando', 'cuanta', 'cuantas', 
    'cuanto', 'cuantos', 'de', 'dejar', 'del', 'demás', 'dentro', 'desde', 'donde', 'dos', 'el', 'él', 'ella', 'ellas', 
    'ellos', 'en', 'encima', 'entonces', 'entre', 'era', 'erais', 'eran', 'eras', 'eres', 'es', 'esa', 'esas', 'ese', 
    'eso', 'esos', 'esta', 'estaba', 'estabais', 'estaban', 'estabas', 'estad', 'estada', 'estadas', 'estado', 'estados', 
    'estamos', 'estando', 'estar', 'estaremos', 'estará', 'estarán', 'estarás', 'estaré', 'estaréis', 'estaría', 'estaríais', 
    'estaríamos', 'estarían', 'estarías', 'estas', 'este', 'estemos', 'esto', 'estos', 'estoy', 'estuve', 'estuviera', 
    'estuvierais', 'estuvieran', 'estuvieras', 'estuvieron', 'estuviese', 'estuvieseis', 'estuviesen', 'estuvieses', 'estuvimos', 
    'estuviste', 'estuvisteis', 'estuviéramos', 'estuviésemos', 'estuvo', 'ex', 'excepto', 'fue', 'fuera', 'fuerais', 'fueran', 
    'fueras', 'fueron', 'fuese', 'fueseis', 'fuesen', 'fueses', 'fui', 'fuimos', 'fuiste', 'fuisteis', 'gran', 'grandes', 'ha', 
    'habéis', 'había', 'habíais', 'habíamos', 'habían', 'habías', 'habida', 'habidas', 'habido', 'habidos', 'habiendo', 'habrá', 
    'habrán', 'habrás', 'habré', 'habréis', 'habría', 'habríais', 'habríamos', 'habrían', 'habrías', 'hace', 'haceis', 'hacemos', 
    'hacen', 'hacer', 'hacerlo', 'hacerme', 'hacernos', 'haceros', 'hacerse', 'haces', 'hacia', 'hago', 'han', 'hasta', 'incluso', 
    'intenta', 'intentais', 'intentamos', 'intentan', 'intentar', 'intentas', 'intento', 'ir', 'jamás', 'junto', 'juntos', 'la', 
    'largo', 'las', 'le', 'les', 'lo', 'los', 'mas', 'me', 'menos', 'mi', 'mía', 'mías', 'mientras', 'mío', 'míos', 'mis', 'misma', 
    'mismas', 'mismo', 'mismos', 'modo', 'mucha', 'muchas', 'muchísima', 'muchísimas', 'muchísimo', 'muchísimos', 'mucho', 'muchos', 
    'muy', 'nada', 'ni', 'ninguna', 'ningunas', 'ninguno', 'ningunos', 'no', 'nos', 'nosotras', 'nosotros', 'nuestra', 'nuestras', 
    'nuestro', 'nuestros', 'nunca', 'os', 'otra', 'otras', 'otro', 'otros', 'para', 'parecer', 'pero', 'poca', 'pocas', 'poco', 
    'pocos', 'podéis', 'podemos', 'poder', 'podría', 'podríais', 'podríamos', 'podrían', 'podrías', 'poner', 'por', 'por qué', 'porque', 
    'primero', 'puede', 'pueden', 'puedo', 'pues', 'que', 'qué', 'querer', 'quien', 'quién', 'quienes', 'quiénes', 'quiere', 'se', 
    'según', 'ser', 'si', 'sí', 'siempre', 'siendo', 'sin', 'sino', 'sobre', 'sois', 'solamente', 'solo', 'somos', 'soy', 'su', 'sus', 
    'también', 'tampoco', 'tan', 'tanto', 'te', 'teneis', 'tenemos', 'tener', 'tengo', 'ti', 'tiempo', 'tiene', 'tienen', 'toda', 
    'todas', 'todavía', 'todo', 'todos', 'tu', 'tú', 'tus', 'un', 'una', 'unas', 'uno', 'unos', 'usa', 'usas', 'usáis', 'usamos', 
    'usan', 'usar', 'usas', 'uso', 'usted', 'ustedes', 'va', 'vais', 'valor', 'vamos', 'van', 'varias', 'varios', 'vaya', 'verdad', 
    'verdadera', 'vosotras', 'vosotros', 'voy', 'vuestra', 'vuestras', 'vuestro', 'vuestros', 'y', 'ya', 'yo'
])

CUSTOM_STOP_WORDS = set([
    'ser', 'haber', 'hacer', 'tener', 'poder', 'ir', 'q', 'si', 'solo', 'saber', 'decir',
    'dar', 'querer', 'ver', 'así', 'sos', 'maje', 'dejar', 'si', 'solo', 'si', 'op', 'vos',
    'cada', 'mismo', 'usted', 'mas', 'pues', 'andar', 'ahora', 'claro', 'nunca', 'quedar', 'pasar',
    'venir', 'poner', 'dio', 'señora', 'señor', 'ahí', 'asi', 'vez', 'jajaja'
])