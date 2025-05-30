import pandas as pd
import streamlit as st

### functions for filtering ####
def country_filter(df,countries=['SA', 'INDIA', 'CAN', 'HKG', 'ZIM', 'NAM', 'SCOT',
                                 'Asia', 'OMAN', 'ENG', 'EAf', 'USA', 'BDESH', 'KENYA',
                                 'NL', 'PAK', 'PNG', 'SL', 'WI', 'AFG', 'IRE', 'UAE',
                                 'AUS',  'NZ', 'BMUDA', 'NEPAL']):
    return df[df["Country"].isin(countries)]

def year_filter(df,year_start,year_end):
    return df[(year_start<=df["retire"])&(year_end>=df["debut"])]

def bat_experience_filter(df,min_inns_bat=0,max_inns_bat=9999):
    return df[(df["Inns_bat"]>=min_inns_bat) & 
              (df["Inns_bat"]<=max_inns_bat)]

def bowl_experience_filter(df,min_inns_bowl=0,max_inns_bowl=9999):
    return df[(df["Inns_bowl"]>=min_inns_bowl) & 
              (df["Inns_bowl"]<=max_inns_bowl)]

def bowling_filter(df,max_avg,max_econ,max_sr,min_avg=0,min_econ=0,min_sr=0):
    if max_avg == None:
        max_avg = 9999
    if max_econ == None:
        max_econ = 9999
    if max_sr == None:
        max_sr = 9999
    return df[(df['Avg_bowl']<=max_avg) & (df['Econ_bowl']<=max_econ) & (df["SR_bowl"]<=max_sr) &
              (df['Avg_bowl']>=min_avg) & (df['Econ_bowl']>=min_econ) & (df["SR_bowl"]>=min_sr) ]

def batting_filter(df,max_sr,max_avg,min_sr=0,min_avg=0):
    if max_avg == None:
        max_avg = 9999
    if max_sr == None:
        max_sr = 9999
    return df[(df["SR_bat"]>=min_sr) & (df["Avg_bat"]>=min_avg) & 
              (df["SR_bat"]<=max_sr) & (df["Avg_bat"]<=max_avg)]

### Final Filter ###
def final_filter(df,
                countries,
                year_start,
                year_end,
                min_inns_bat,
                max_inns_bat,
                min_inns_bowl,
                max_inns_bowl,
                max_avg_bowl,
                max_econ_bowl,
                max_sr_bowl,
                min_avg_bowl,
                min_econ_bowl,
                min_sr_bowl,
                max_avg_bat,
                max_sr_bat,
                min_avg_bat,
                min_sr_bat):
                             
    return country_filter(df,countries = countries).pipe(
        year_filter, year_start = year_start, year_end = year_end
    ).pipe(
        bat_experience_filter,min_inns_bat = min_inns_bat, max_inns_bat = max_inns_bat
    ).pipe(
        bowl_experience_filter, min_inns_bowl = min_inns_bowl, max_inns_bowl = max_inns_bowl
    ).pipe(
        bowling_filter, max_avg=max_avg_bowl,max_econ=max_econ_bowl,max_sr=max_sr_bowl,
                        min_avg=min_avg_bowl,min_econ=min_econ_bowl,min_sr=min_sr_bowl
    ).pipe(
        batting_filter, min_sr = min_sr_bat, min_avg = min_avg_bat,
                        max_sr = max_sr_bat, max_avg = max_avg_bat
    )

## main logic
df = pd.read_csv(r"processed_data/player_stats.csv")
all_countries = list(df["Country"].unique())

# print(all_countries)
st.set_page_config(page_title="ODI Team Selector",page_icon="🏏")
st.title("ODI PLAYER SELECTION 🏏")
st.write("Apply required filters and get the perfect team !!")
st.divider()

st.header("Filters") 

#----Year filter----
year_start,year_end = st.select_slider("Select the year",
                                    options=list(range(min(df["debut"]),max(df["retire"]+1))),
                                    value=((min(df["debut"])),max(df["retire"])))

#---Country filter---
country_select_box, country_checkbox = st.columns([2,1])

# Checkbox inside the right column
with country_checkbox:
    select_all_country = st.checkbox("Select / Deselect all Countries",value=True)

# Multiselect inside the left column
with country_select_box:
    if select_all_country:
        countries = st.multiselect("Select Country", sorted(all_countries),
                                default=sorted(all_countries),
                                key="all_country_selected",placeholder="Select Country/Countries")
    else:
        countries = st.multiselect("Select Country",
                                sorted(all_countries),
                                key="country_select",placeholder="Select Country/Countries")


#---batiing and bowling experience filter---
bat_col,bowl_col = st.columns(2)

#batting experience filter
with bat_col:
    st.subheader(":gray[Batting Filters]")
    with st.expander('Filters'):
        bat_filter_checkbox = st.checkbox("Apply Filters",key="batiing_filters",
                                          help="Filters are :red[NOT] applied until this box is checked !!")
        min_inns_bat,max_inns_bat = st.select_slider("MINIMUM & MAXIMUM innings played (batting)",
                                options=list(range(0,int(max(df["Inns_bat"]))+1)),
                                value=(0,int(max(df["Inns_bat"]))),
                                key="min_max_inns_bat")
        
        col_bat_left, col_bat_right = st.columns(2)
        with col_bat_left:
            min_avg_bat = st.number_input("MINIMUM batting average",min_value=0,max_value=9999,key="min_avg_bat")
           
            min_sr_bat = st.number_input("MINIMUM batting strike rate",min_value=0,max_value=9999,key="min_sr_bat")
        with col_bat_right:
            max_avg_bat = st.number_input("MAXIMUM batting average",min_value=0,max_value=9999, value=None,
                                          key="max_avg_bat")
            max_sr_bat = st.number_input("MAXIMUM batting strike rate",min_value=0,max_value=9999, value=None,
                                         key="max_sr_bat")


        if not bat_filter_checkbox:
            min_inns_bat = 0
            max_inns_bat = 9999
            min_avg_bat = 0
            max_avg_bat = 9999
            min_sr_bat = 0
            max_sr_bat = 9999
    if bat_filter_checkbox:
        st.write(":red[Batting filters applied]")

#bowling experience filter
with bowl_col:
    st.subheader(":gray[Bowling Filters]")
    with st.expander("Filters"):
        bowl_filter_checkbox = st.checkbox("Apply Filters",key="bowling_filters",
                                           help="Filters are :red[NOT] applied until this box is checked !!")
        
        min_inns_bowl,max_inns_bowl = st.select_slider("MINIMUM & MAXIMUM innings played (bowling)",
                                options=list(range(0,int(max(df["Inns_bowl"]))+1)),
                                value=(0,int(max(df["Inns_bowl"]))),
                                key="min_max_inns_bowl")

        col_bowl_left,col_bowl_right  = st.columns(2)
        with col_bowl_left:
            # min_inns_bowl = st.slider("MINIMUM innings played (bowling)",
            #                     min_value=1, max_value=int(max(df["Inns_bowl"])))
            
            min_avg_bowl = st.number_input("MINIMUM bowling average", min_value=0,max_value=9999)

            min_sr_bowl = st.number_input("MINIMUM bowling strike rate", min_value=0,max_value=9999)

            min_econ_bowl = st.number_input("MINIMUM bowling economy", min_value=0,max_value=9999)
        with col_bowl_right:
            max_avg_bowl = st.number_input("MAXIMUM bowling average", min_value=0,max_value=9999,value=None,
                                           key="max_avg_bowl")
            max_sr_bowl = st.number_input("MAXIMUM bowling strike rate", min_value=0,max_value=9999,value=None, 
                                          key="max_sr_bowl")
            max_econ_bowl = st.number_input("MAXIMUM bowling economy", min_value=0,max_value=9999,value=None,
                                            key="max_econ_bowl")

        if not bowl_filter_checkbox:
            min_inns_bowl = 0
            max_inns_bowl = 9999
            min_avg_bowl = 0
            max_avg_bowl = 9999
            min_sr_bowl = 0
            max_sr_bowl = 9999
            min_econ_bowl = 0
            max_econ_bowl = 9999
    if bowl_filter_checkbox:
        st.write(":red[Bowling filters applied]")
st.info("Apply both Batting and Bowling filters for 'All Rounders'")


filtered_df = final_filter(df,
                            countries,
                            year_start,
                            year_end,
                            min_inns_bat,
                            max_inns_bat,
                            min_inns_bowl,
                            max_inns_bowl,
                            max_avg_bowl,
                            max_econ_bowl,
                            max_sr_bowl,
                            min_avg_bowl,
                            min_econ_bowl,
                            min_sr_bowl,
                            max_avg_bat,
                            max_sr_bat,
                            min_avg_bat,
                            min_sr_bat)

filtered_df = filtered_df.rename(columns={
    "player_name":"Player",
    "Country":"Country",
    "Mat":"Matches",
    "Inns_bat":"Innings Batted",
    "SR_bat":"Batting SR",
    "Avg_bat":"Batting Avg",
    "Inns_bowl":"Innings Bowled",
    "Econ_bowl":"Economy",
    "Avg_bowl":"Bowling Avg",
    "SR_bowl":"Bowling SR",
    "bat_rating":"Batter Rating",
    "bowl_rating":"Bowler Rating",
    "role":"Role"
})

df_columns = ["Player",
            "Country",
            "Role",
            "Matches",
            "Innings Batted",
            "Batting SR",
            "Batting Avg",
            "Innings Bowled",
            "Economy",
            "Bowling Avg",
            "Bowling SR",
            "Batter Rating",
            "Bowler Rating",
            "Batter_rank",
            "Bowler_rank"]

st.write(f":orange[{filtered_df.shape[0]} filtered players available]")
with st.expander("See all Filtered Players"):
    st.dataframe(filtered_df[df_columns])
st.divider()

#----Team Filters----
team,table = st.columns([2,3])
with team:
    st.header("Team Combination")
    st.write("Select required number players in each role")
    bat,bowl,allrnd = st.columns(3)
    with bat:
        batters = st.number_input("Batters",min_value=0,max_value=11)
    with bowl:
        bowlers = st.number_input("Bowlers",min_value=0,max_value=11)
    with allrnd:
        allrounders = st.number_input("All Rounders",min_value=0,max_value=11)
    selected_players = batters + bowlers + allrounders
    if selected_players==11:
        st.write(":green[11 Players selected]")
    elif selected_players < 11:
        st.write(f":orange[Please select {11-selected_players} more player(s)]")
        st.warning(f"11 players required. Only {selected_players} Players selected")
    else:
        st.write(f":red[Please remove {selected_players - 11} players]")
        st.error(f"Only 11 players are allowed. {selected_players} Players selected")

st.divider()

batter_df = filtered_df[filtered_df["Role"]=="Batter"].copy()
bowler_df = filtered_df[filtered_df["Role"]=="Bowler"].copy()
allrnd_df = filtered_df[filtered_df["Role"]=="All-Rounder"].copy()

batter_df = batter_df.sort_values("Batter_rank").head(batters)
bowler_df = bowler_df.sort_values("Bowler_rank").head(bowlers)
allrnd_df = allrnd_df.sort_values("allrnd_rating",ascending=False).head(allrounders)
finalXIdf = pd.concat([batter_df,allrnd_df,bowler_df],ignore_index=True)


with table:
    if finalXIdf.shape[0]>0:
        st.subheader("Final XI")
        st.dataframe(finalXIdf[df_columns].sort_values("Batter_rank",ignore_index=True))
        if finalXIdf.shape[0]<11 and selected_players==11:
            st.warning(f"Only {finalXIdf.shape[0]} players available with required conditions/roles")
        elif finalXIdf.shape[0]==11:
            st.success("11 top players selected")
        st.write(f"Team Batting Average : {finalXIdf["Batting Avg"].mean():.2f}")
    
