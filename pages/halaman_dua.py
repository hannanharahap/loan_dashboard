import streamlit as st
import pandas as pd
import plotly_express as px

st.set_page_config(
    page_title='Demo Dashboard',
    page_icon="🎗", # windows dan . (titik) untuk pilih emoji
    layout="wide"
)

st.title("Financial Insights Dashboard: Loan Performance & Trends")

st.markdown("---")

st.sidebar.header("Dashboard Filters and Features")

st.sidebar.subheader("Features")

st.sidebar.markdown('''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
''')


loan = pd.read_pickle('data_input/loan_clean')

condition = st.selectbox(
    "Select Loan Condition",
    ("Good Loan", "Bad Loan")
)
with st.container(border=True):
    tab4, tab5 = st.tabs(['Loan Amount Distribution','Loan Amount Distribution by Purpose'])
    loan_condition = loan[loan['loan_condition'] == condition]
    with tab4:
        hist=px.histogram(
            loan_condition,
            x='loan_amount',
            color='term',
            nbins=20,
            template='seaborn',
            labels={
                'loan_amount':'Loan Amount',
                'term':'Loan Term'
            },
            title='Loan Amount Distribution by Condition'
        )
        st.plotly_chart(hist)

    with tab5:
        box=px.box(
            loan_condition,
            x='purpose',
            y='loan_amount',
            color='term',
            template='seaborn',
            labels={
                'purpose':'Loan Purpose',
                'loan_amount':'Loan Amount',
                'term':'Loan Term'
            },
            title='Loan Amount Distribution by Purpose'
        )
        st.plotly_chart(box)