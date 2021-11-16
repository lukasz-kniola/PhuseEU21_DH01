import streamlit as st
import requests, io
import pandas as pd
import altair as alt

# Send and retrieve HTTP (REST) request
url = 'https://clinicaltrials.gov/api/query/study_fields?expr=multiple sclerosis&fields=NCTId%2CCondition%2Cphase%2CStartDate%2CEnrollmentCount&min_rnk=1&max_rnk=1000&fmt=csv'
res = requests.get(url).content

# Extract contents of request, skip CSV header (first 10 lines), to Pandas dataframe
data = pd.read_csv(io.StringIO(res.decode("utf-8")), skiprows=10).fillna(0)
data = data[data['StartDate'] != 0]

# Get year from StartDate
data["StartYear"] = data["StartDate"].map(lambda dt: str(dt).split()[-1])

# Find all Phase values in dataframe
studyPhases = data["Phase"].unique().tolist()
studyPhases = [str(x) for x in studyPhases if x not in [0, "Not Applicable"]]
studyPhases.sort()

# List all Phase values as checkboxes in sidebar
st.sidebar.subheader("Phases:")
phases = {}
for phase in studyPhases:
    phases[phase] = st.sidebar.checkbox(phase,True)
    
# Subset dataframe to only phases selected in sidebar
subdata = data[data["Phase"].isin([k for k,v in phases.items() if v])]

# Sum up enrollment count by year and phase
studyCount = subdata.groupby(['StartYear','Phase'])['EnrollmentCount'].count().reset_index()
enrolmentCount = subdata.groupby(['StartYear','Phase'])['EnrollmentCount'].sum().reset_index()

# Altair study count chart
sc = alt.Chart(studyCount).mark_bar().encode(x='StartYear:O', y='sum(EnrollmentCount):Q', color='Phase:N')

# Altair enrollment chart
ec = alt.Chart(enrolmentCount).mark_bar().encode(x='StartYear:O', y='sum(EnrollmentCount):Q', color='Phase:N')

st.header('CT.gov API - "Multiple Sclerosis" studies')
st.subheader('Study count')
st.altair_chart(sc)
st.subheader('Enrollment')
st.altair_chart(ec)
