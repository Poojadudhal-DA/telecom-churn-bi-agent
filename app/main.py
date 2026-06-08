import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Telecom Churn BI Agent",
    page_icon="📊",
    layout="wide"
)

# --- Title ---
st.title("📊 Telecom Customer Churn Dashboard & BI Agent")
st.markdown("Business intelligence insights on telecom customer churn.")

st.divider()

# --- Load Data ---
data_path = os.path.join("data", "Telco-Customer-Churn-Cleaned.csv")

@st.cache_data
def load_data():
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        return df
    else:
        st.error(f"Data file not found at {data_path}.")
        return None

df = load_data()

if df is not None:

    # --- KPIs ---
    total_customers = len(df)
    churned_customers = len(df[df['Churn'] == 'Yes'])
    churn_rate = (churned_customers / total_customers) * 100
    avg_monthly_charges = df['MonthlyCharges'].mean()

    # --- Display KPIs ---
    st.subheader("📌 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Churn Rate", f"{churn_rate:.2f}%")
    col2.metric("Avg Monthly Charges", f"${avg_monthly_charges:.2f}")
    col3.metric("Total Customers", f"{total_customers:,}")
    col4.metric("Churned Customers", f"{churned_customers:,}")

    st.divider()

    # --- Charts Row ---
    st.subheader("📊 Churn Insights")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(3, 2.5))
        sns.countplot(
            data=df, x='Contract',
            hue='Churn', palette='Set2', ax=ax1)
        ax1.set_title("Contract Type", fontsize=8)
        ax1.set_xlabel("", fontsize=7)
        ax1.set_ylabel("Customers", fontsize=7)
        ax1.tick_params(labelsize=6)
        ax1.legend(fontsize=6)
        plt.tight_layout()
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(3, 2.5))
        sns.countplot(
            data=df, x='InternetService',
            hue='Churn', palette='Set1', ax=ax2)
        ax2.set_title("Internet Service", fontsize=8)
        ax2.set_xlabel("", fontsize=7)
        ax2.set_ylabel("Customers", fontsize=7)
        ax2.tick_params(labelsize=6)
        ax2.legend(fontsize=6)
        plt.tight_layout()
        st.pyplot(fig2)

    with col3:
        fig3, ax3 = plt.subplots(figsize=(3, 2.5))
        df[df['Churn'] == 'Yes']['tenure'].hist(
            bins=30, ax=ax3, color='red', alpha=0.7)
        ax3.set_title("Tenure (Churned)", fontsize=8)
        ax3.set_xlabel("Months", fontsize=7)
        ax3.set_ylabel("Customers", fontsize=7)
        ax3.tick_params(labelsize=6)
        plt.tight_layout()
        st.pyplot(fig3)

    with col4:
        fig4, ax4 = plt.subplots(figsize=(3, 2.5))
        sns.countplot(
            data=df, x='PaymentMethod',
            hue='Churn', palette='coolwarm', ax=ax4)
        ax4.set_title("Payment Method", fontsize=8)
        ax4.set_xlabel("", fontsize=7)
        ax4.set_ylabel("Customers", fontsize=7)
        ax4.tick_params(labelsize=5)
        plt.xticks(rotation=15)
        ax4.legend(fontsize=6)
        plt.tight_layout()
        st.pyplot(fig4)

    st.divider()

    # --- Key Insights ---
    st.subheader("🔍 Key Insights")
    st.markdown("""
    - 🔴 **Month-to-month** customers churn the most **(1,655 customers)**
    - 🔴 **Fiber optic** users represent **69.4%** of all churned customers
    - 🔴 **New customers (1-5 months)** are at highest churn risk
    - 🔴 **Electronic check** users churn the most **(1,071 customers)**
    - 🔴 Customers **without Online Security** churn significantly more
    """)

    st.divider()

    # --- AI Agent ---
    st.subheader("🤖 Ask BI Agent")
    st.markdown("Ask me anything about the telecom churn data!")

    # --- Rule Based Agent Function ---
    def bi_agent(question, df):
        question = question.lower().strip()

        # Churn Rate
        if "churn rate" in question:
            return f"📊 The churn rate is **{churn_rate:.2f}%** — meaning {churned_customers:,} out of {total_customers:,} customers have churned."

        # Total Customers
        elif "total customers" in question or "how many customers" in question:
            return f"👥 Total customers in the dataset: **{total_customers:,}**"

        # Churned Customers
        elif "churned customers" in question or "how many churned" in question:
            return f"📉 Total churned customers: **{churned_customers:,}**"

        # Average Monthly Charges
        elif "monthly charges" in question or "average charges" in question:
            return f"💰 Average monthly charges: **${avg_monthly_charges:.2f}**"

        # Contract Type
        elif "contract" in question:
            contract_churn = df[df['Churn']=='Yes']['Contract'].value_counts()
            return f"📋 Churn by Contract Type:\n- Month-to-month: **{contract_churn.get('Month-to-month', 0):,}**\n- One year: **{contract_churn.get('One year', 0):,}**\n- Two year: **{contract_churn.get('Two year', 0):,}**"

        # Internet Service
        elif "internet" in question or "fiber" in question:
            internet_churn = df[df['Churn']=='Yes']['InternetService'].value_counts()
            return f"🌐 Churn by Internet Service:\n- Fiber optic: **{internet_churn.get('Fiber optic', 0):,}**\n- DSL: **{internet_churn.get('DSL', 0):,}**\n- No internet: **{internet_churn.get('No', 0):,}**"

        # Payment Method
        elif "payment" in question:
            payment_churn = df[df['Churn']=='Yes']['PaymentMethod'].value_counts()
            top_payment = payment_churn.index[0]
            return f"💳 Highest churn payment method: **{top_payment}** with **{payment_churn.iloc[0]:,}** customers!"

        # Tenure
        elif "tenure" in question or "new customers" in question:
            avg_tenure = df[df['Churn']=='Yes']['tenure'].mean()
            return f"📅 Average tenure of churned customers: **{avg_tenure:.1f} months** — Most churn happens in first 1-5 months!"

        # Senior Citizen
        elif "senior" in question:
            senior_churn = df[(df['Churn']=='Yes') & (df['SeniorCitizen']=='Yes')].shape[0]
            return f"👴 Senior citizens who churned: **{senior_churn:,}**"

        # Online Security
        elif "security" in question or "online security" in question:
            no_security_churn = df[(df['Churn']=='Yes') & (df['OnlineSecurity']=='No')].shape[0]
            return f"🔒 Customers without Online Security who churned: **{no_security_churn:,}** — significantly higher than those with security!"

        # Help
        elif "help" in question or "what can you" in question:
            return """🤖 I can answer questions about:
- Churn rate
- Total customers
- Churned customers
- Monthly charges
- Contract type churn
- Internet service churn
- Payment method churn
- Tenure analysis
- Senior citizen churn
- Online security impact"""

        else:
            return "🤔 I didn't understand that. Try asking about: churn rate, contract type, internet service, payment method, tenure, or monthly charges!"

    # --- Agent Input ---
    user_question = st.text_input(
        "💬 Type your question:",
        placeholder="e.g. What is the churn rate?"
    )

    if st.button("🔍 Ask Agent"):
        if user_question:
            answer = bi_agent(user_question, df)
            st.success(answer)
        else:
            st.warning("Please type a question first!")

    st.divider()

    # --- Raw Data ---
    with st.expander("📂 View Raw Data (First 10 Rows)"):
        st.dataframe(df.head(10))