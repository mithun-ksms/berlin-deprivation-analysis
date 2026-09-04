import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Berlin Deprivation Analysis", layout="wide")

# ---- HEADER ----
st.title("🏙️ Berlin Urban Deprivation Analyser")
st.markdown("**Cross-city comparison with London | Machine Learning & SHAP Explainability**")
st.markdown("---")

# ---- LOAD DATA ----
df = pd.read_csv('berlin_deprivation_clean.csv')

# ---- KEY METRICS ROW ----
st.subheader("📊 City Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Districts", "143")
col2.metric("Avg Unemployment", f"{df['unemployment_pct'].mean():.2f}%")
col3.metric("Avg Child Poverty", f"{df['child_poverty_pct'].mean():.2f}%")
col4.metric("Most Deprived", df.loc[df['deprivation_score'].idxmax(), 'district_name'])

st.markdown("---")

# ---- TOP/BOTTOM DISTRICTS ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Most Deprived Districts")
    top5 = df[['district_name', 'deprivation_score']].sort_values('deprivation_score', ascending=False).head(5)
    fig = px.bar(top5, x='deprivation_score', y='district_name', 
                 orientation='h', color='deprivation_score',
                 color_continuous_scale='Reds')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🟢 Least Deprived Districts")
    bottom5 = df[['district_name', 'deprivation_score']].sort_values('deprivation_score', ascending=True).head(5)
    fig2 = px.bar(bottom5, x='deprivation_score', y='district_name',
                  orientation='h', color='deprivation_score',
                  color_continuous_scale='Greens_r')
    fig2.update_layout(yaxis={'categoryorder': 'total descending'}, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ---- SHAP FEATURE IMPORTANCE ----
st.subheader("🔍 What Drives Deprivation in Berlin? (SHAP Analysis)")

shap_data = pd.DataFrame({
    'Indicator': ['Child Poverty', 'Unemployment', 'Welfare Dependency', 'Single Parent Households'],
    'SHAP Importance': [0.4398, 0.2295, 0.1047, 0.0817]
})

fig3 = px.bar(shap_data, x='SHAP Importance', y='Indicator',
              orientation='h', color='SHAP Importance',
              color_continuous_scale='Blues')
fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig3, use_container_width=True)
st.caption("Random Forest model R² = 0.97 | SHAP values show average impact on deprivation score across 143 districts")

st.markdown("---")

# ---- LONDON VS BERLIN COMPARISON ----
st.subheader("🌍 Cross-City Comparison: London vs Berlin")

comparison = pd.DataFrame({
    'Metric': ['Primary Driver', 'Secondary Driver', 'Model R²', 'Most Deprived Area', 'Least Deprived Area'],
    'London': ['Employment', 'Income', '0.897', 'Hackney', 'Richmond upon Thames'],
    'Berlin': ['Child Poverty', 'Unemployment', '0.97', 'Köllnische Heide', 'Mahlsdorf']
})
st.table(comparison)

st.markdown("---")

# ---- SCATTER EXPLORER ----
st.subheader("🔎 Explore Districts")
x_axis = st.selectbox("X axis", ['unemployment_pct', 'welfare_pct', 'child_poverty_pct', 'single_parent_pct'])
y_axis = st.selectbox("Y axis", ['deprivation_score', 'child_poverty_pct', 'unemployment_pct', 'welfare_pct'])

fig4 = px.scatter(df, x=x_axis, y=y_axis, hover_name='district_name',
                  color='deprivation_score', color_continuous_scale='RdYlGn_r',
                  title=f"{x_axis} vs {y_axis}")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.caption("Data: Monitoring Soziale Stadtentwicklung (MSS) 2023, Berlin Senate | Analysis: Mithun Surriya KS")
