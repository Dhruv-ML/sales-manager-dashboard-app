import streamlit as st
import altair as alt
import pandas as pd

# Load your data
dpw = pd.read_csv('sales lead manager.csv', encoding='latin-1')
dpw['Label'] = dpw['First Name'] + ' ' + dpw['Last Name']

# Sort lists
city_sorted = sorted(dpw['City'].dropna().unique())
country_sorted = sorted(dpw['Country'].dropna().unique())

# App title
st.title("Sales Freight Forwarding Manager Talent Mapping")
st.markdown("<br>", unsafe_allow_html=True)

# Altair bindings & selections
slider_ffe = alt.binding_range(name='Freight Forwarding Exp.', min=0, max=40, step=1)
dropdown_city = alt.binding_select(name='City: ', options=city_sorted)

selection_ffe = alt.selection_point(fields=['Freight Forwarding Experience'], bind=slider_ffe)
selection_country = alt.selection_point(fields=['Country'])
selection_city = alt.selection_point(fields=['City'], bind=dropdown_city)
select_level = alt.selection_point(fields=['Level of Position'], bind='legend')

# Bar chart
chart = alt.Chart(dpw).mark_bar().encode(
    x=alt.X('count():Q', title='Count'),
    y=alt.Y('Country:N', title='Country'),
    opacity=alt.condition(selection_country, alt.value(0.8), alt.value(0.05)),
    tooltip=['Country:N', 'count():Q']
).properties(
    width=350,
    height=350,
    title=alt.TitleParams(text='Count of Lead Sales Manager', anchor='middle')
).add_params(
    selection_country
).transform_filter(
    select_level
).interactive()

# Scatter plot
mapping = alt.Chart(dpw).mark_circle(size=60).encode(
    x='Total Experience:Q',
    y='Sales Management Experience',
    color=alt.Color('Level of Position:N', title='Level', scale=alt.Scale(scheme='tableau20')),
    opacity=alt.condition(select_level, alt.value(0.8), alt.value(0.00)),
    tooltip=[
        'First Name', 'Last Name', 'Total Experience', 'Sales Management Experience', 
        'Freight Forwarding Experience', 'Current Position', 'Company Name', 'Country'
    ],
).transform_filter(
    selection_ffe & selection_city & selection_country
).properties(
    width=350,
    height=350,
    title=alt.TitleParams(text='Freight Forwarding Years of Experience', anchor='middle')
).add_params(
    selection_ffe,
    selection_city,
    select_level
).interactive()

# Combine plot 1
plot1 = alt.hconcat(chart, mapping, spacing=30)
st.altair_chart(plot1, use_container_width=True)

# 🔎 Add person selection + LinkedIn for plot1
st.markdown("### 🔗 View LinkedIn from the plot")
selected_label_1 = st.selectbox("Select a talent (plot 1):", dpw['Label'].unique())
person_1 = dpw[dpw['Label'] == selected_label_1]
if not person_1.empty:
    url_1 = person_1['LinkedIn'].values[0]
    st.markdown(f"🔗 [View {selected_label_1}'s LinkedIn Profile]({url_1})", unsafe_allow_html=True)

# --- Spacer ---
st.markdown("<br><br>", unsafe_allow_html=True)

# ========== SECOND VISUALIZATION (DP World vs Competitor Talent) ==========
dp_world_candidates = dpw[dpw['Company Name'] == 'DP World']
other_candidates = dpw[dpw['Company Name'] != 'DP World']

company_dropdown = alt.binding_select(
    name='Select Company: ',
    options=sorted(other_candidates['Company Name'].dropna().unique())
)

country_dropdown = alt.binding_select(name='Country: ', options=country_sorted)

company_selection = alt.selection_point(fields=['Company Name'], bind=company_dropdown)
country_selection = alt.selection_point(fields=['Country'], bind=country_dropdown)
selection_level = alt.selection_point(fields=['Level of Position'], bind='legend')

# DP World talent pool plot
scatter_plot = alt.Chart(dp_world_candidates).mark_circle(size=60).encode(
    x='Total Experience:Q',
    y='Freight Forwarding Experience:Q',
    color=alt.Color('Level of Position:N', legend=alt.Legend(title='Level of Position')),
    tooltip=[
        'First Name', 'Last Name', 'Total Experience', 'Freight Forwarding Experience', 
        'Current Position', 'Company Name', 'Country'
    ],
    opacity=alt.condition(selection_level, alt.value(0.9), alt.value(0.10))
).transform_filter(
    country_selection
).properties(
    width=350,
    height=350,
    title=alt.TitleParams(text='Logistic firm Talent Pool (client)', anchor='middle')
).add_params(selection_level).interactive()

# Competitor plot
scatter_plot_other = alt.Chart(other_candidates).mark_circle(size=60).encode(
    x='Total Experience:Q',
    y='Freight Forwarding Experience:Q',
    color=alt.Color('Level of Position:N', legend=alt.Legend(title='Level of Position')),
    tooltip=[
        'First Name', 'Last Name', 'Total Experience', 'Freight Forwarding Experience', 
        'Level of Position', 'Company Name', 'City'
    ],
    opacity=alt.condition(company_selection, alt.value(0.9), alt.value(0.10))
).transform_filter(
    country_selection & selection_level
).properties(
    width=350,
    height=350,
    title=alt.TitleParams(text='Competitors Talent Pool', anchor='middle')
).add_params(
    company_selection, country_selection, selection_level 
).interactive()

plot2 = alt.hconcat(scatter_plot_other, scatter_plot, spacing=30)
st.altair_chart(plot2, use_container_width=True)

# 🔎 Add person selection + LinkedIn for plot2
st.markdown("### 🔗 View LinkedIn from Talent Pool Comparison")
selected_label_2 = st.selectbox("Select a talent (plot 2):", dpw['Label'].unique())
person_2 = dpw[dpw['Label'] == selected_label_2]
if not person_2.empty:
    url_2 = person_2['LinkedIn'].values[0]
    st.markdown(f"🔗 [View {selected_label_2}'s LinkedIn Profile]({url_2})", unsafe_allow_html=True)
    
