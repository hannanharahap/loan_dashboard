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

with st.container(border=True):
    col1,col2 = st.columns(2)

    with col1:
        st.metric("Total Loans", f"{loan['id'].count():,.0f}", delta=None, delta_color="normal", help=None, label_visibility="visible")
        st.metric("Total Loan Amount", f"${loan['loan_amount'].sum():,.0f}", delta=None, delta_color="normal", help=None, label_visibility="visible")

    with col2:
        st.metric("Average Interest Rate", f"{loan['interest_rate'].mean():,.2f}%", delta=None, delta_color="normal", help=None, label_visibility="visible")
        st.metric("Average Loan Amount", f"${loan['loan_amount'].mean():,.0f}", delta=None, delta_color="normal", help=None, label_visibility="visible")

with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(['Loans Issued Over Time','Loan Amount Over Time','Issue Date Analysis'])

    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
        line_count=px.line(
            loan_date_count.sort_index(),
            markers=True,
            labels={
                'issue_date':'Issue Date',
                'value':'Number of Loans'
            },
            title='Number of Loans Issued Overtime',
            template='seaborn'
        ).update_layout(showlegend = False)
        st.plotly_chart(line_count)
    
    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
        line_sum=px.line(
            loan_date_sum.sort_index(),
            markers=True,
            labels={
                'issue_date':'Issue Date',
                'value':'Total Loan Amount'
            },
            title='Total Loan Amount Issued Over Time',
            template='seaborn'
        ).update_layout(showlegend = False)
        st.plotly_chart(line_sum)

    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
        line_week=px.bar(
            loan_day_count,
            category_orders={
                'issue_weekday':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            },
            labels={'issue_weekday':'Day of the Week','value':'Number of Loans'},
            title='Distribution of Loans by Day of the Week',
            template='seaborn'
        ).update_layout(showlegend = False)
        st.plotly_chart(line_week)

with st.expander("Clik Here to Expand Visualization"):
    col3,col4=st.columns(2)

    with col3:
        pie=px.pie(
            loan,
            names='loan_condition',
            hole=0.4,
            title='Distribution of Loans by Condition',
            template='seaborn'
        )
        st.plotly_chart(pie)

    with col4:
        grade = loan['grade'].value_counts().sort_index()
        bar=px.bar(
            grade,
            labels={
                'grade':'Grade',
                'value':'Number of Loans'
            },
            title='Distribution of Loans by Grade',
            template='seaborn'
        ).update_layout(showlegend = False)
        st.plotly_chart(bar)



