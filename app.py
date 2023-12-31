import streamlit as st # pip install streamlit==1.0.0
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

file1 = 'project_1_Olympics_data_analysis\dataset\\athlete_events.csv'
file2 = 'project_1_Olympics_data_analysis\dataset\\noc_regions.csv'

df = pd.read_csv(file1)
region_df = pd.read_csv(file2)

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
#st.sidebar.image()

user_menu = st.sidebar.radio(
    "Select an option",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete-wise analysis")
)

# st.dataframe(df)

if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")

    years,country = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medal_tally = helper.fetch_metal_tally(df,selected_year,selected_country)

    if selected_year == "Overall" and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != "Overall" and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    elif selected_year == "Overall" and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")
    elif selected_year != "Overall" and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
    
    st.table(medal_tally)

elif user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    
    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x = "Edition", y = "No of countries")
    st.title("Participating nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df)
    fig = px.line(events_over_time, x = "Edition", y = "No of events")
    st.title("Events over time")
    st.plotly_chart(fig)

    athletes_over_time = helper.athletes_over_time(df)
    fig = px.line(athletes_over_time, x = "Edition", y = "No of athletes")
    st.title("Athletes over time")
    st.plotly_chart(fig)

    st.title("No of Events over time (Every sport)")
    fig, ax = plt.subplots(figsize = (20,20))

    x = df.drop_duplicates(["Year","Sport","Event"])
    ax = sns.heatmap(x.pivot_table(index = "Sport", columns = "Year", values = "Event", aggfunc = 'count').fillna(0).astype('int'), annot = True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Select a sport", sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

elif user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a country", country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x = "Year", y = 'Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize = (20,20))
    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

elif user_menu == "Athlete-wise analysis":
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    fig = ff.create_displot([x1,x2,x3,x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist = False, show_rug = False)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton','Sailing','Gymnastics',
                    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery',
                    'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball',
                    'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    
    fig = ff.create_displot(x, name, show_hist = False, show_rug = False)
    fig.update_layout(autosize = False, width = 100, height = 600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Height Vs Weight")
    selected_sport = st.selectbox("Select a sport", sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'], hue = temp_df['Medal'], style = temp_df['Sex'], s = 60)
    
    st.pyplot(fig)

    st.title("Men vs Women participation")
    final = helper.men_vs_women(df)
    fig = px.line(final, x = 'Year', y = ['Male', 'Female'])
    fig.update_layout(autosize = False, width = 100, height = 600)
    st.plotly_chart(fig)