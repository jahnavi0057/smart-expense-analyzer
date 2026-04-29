"""
Smart Expense Analyzer Web App
A Streamlit application for analyzing and predicting expenses
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.preprocessing import load_and_validate_csv, clean_data, get_monthly_data, calculate_basic_stats
from utils.categorization import categorize_expenses, get_spending_by_category, get_category_statistics, get_category_distribution
from utils.prediction import predict_next_month, get_spending_trend, detect_anomalies


# Page configuration
st.set_page_config(
    page_title="Smart Expense Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .warning-box {
        background-color: #ffe6e6;
        border: 1px solid #ff6b6b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Smart Expense Analyzer")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Choose a view:",
    ["📤 Upload & Process", "📋 Data Overview", "💼 Category Analysis", "🔮 Predictions & Insights"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**How to use:**\n"
    "1. Upload a CSV with Date, Description, Amount columns\n"
    "2. Review cleaned data\n"
    "3. Analyze spending by category\n"
    "4. View predictions and insights"
)

# Initialize session state
if 'df_original' not in st.session_state:
    st.session_state.df_original = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'df_categorized' not in st.session_state:
    st.session_state.df_categorized = None
if 'cleaning_summary' not in st.session_state:
    st.session_state.cleaning_summary = None


# ==================== UPLOAD & PROCESS PAGE ====================
if app_mode == "📤 Upload & Process":
    st.markdown("# 📤 Upload & Process Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Your Expense Data")
        st.markdown("""
        Upload a CSV file with the following columns:
        - **Date**: Transaction date (e.g., 2024-01-15)
        - **Description**: Transaction description
        - **Amount**: Transaction amount (numeric)
        """)
    
    with col2:
        # Sample data download button
        sample_df = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'Description': ['Grocery Shopping', 'Gas Station', 'Restaurant Dinner'],
            'Amount': [45.50, 35.00, 28.75]
        })
        st.download_button(
            label="📥 Download Sample CSV",
            data=sample_df.to_csv(index=False),
            file_name="sample_expenses.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Load and validate
        df, error = load_and_validate_csv(uploaded_file)
        
        if error:
            st.error(f"❌ {error}")
        else:
            st.session_state.df_original = df
            st.success("✅ File loaded successfully!")
            
            # Show raw data preview
            with st.expander("👀 Preview Raw Data"):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Data cleaning
            st.subheader("🧹 Data Cleaning")
            if st.button("Clean & Preprocess Data", type="primary"):
                try:
                    df_cleaned, cleaning_summary = clean_data(df)
                    st.session_state.df_cleaned = df_cleaned
                    st.session_state.cleaning_summary = cleaning_summary
                    
                    # Show cleaning summary
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Duplicates Removed", cleaning_summary['duplicates_removed'])
                    with col2:
                        st.metric("Missing Values Removed", cleaning_summary['rows_with_missing_values'])
                    with col3:
                        st.metric("Invalid Amounts Removed", cleaning_summary['invalid_amounts_removed'])
                    with col4:
                        st.metric("Final Rows", cleaning_summary['final_rows'])
                    
                    st.success(f"✅ Data cleaned! Final rows: {cleaning_summary['final_rows']}")
                    
                    # Categorize expenses
                    df_categorized = categorize_expenses(df_cleaned)
                    st.session_state.df_categorized = df_categorized
                    
                    with st.expander("👀 Preview Cleaned Data"):
                        st.dataframe(df_categorized.head(10), use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ Error during cleaning: {str(e)}")


# ==================== DATA OVERVIEW PAGE ====================
elif app_mode == "📋 Data Overview":
    st.markdown("# 📋 Data Overview")
    
    if st.session_state.df_categorized is None:
        st.warning("⚠️ Please upload and process data first!")
    else:
        df = st.session_state.df_categorized
        
        # Basic statistics
        st.subheader("📊 Basic Statistics")
        stats = calculate_basic_stats(df)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Expenses", f"${stats['total_expenses']:.2f}")
        with col2:
            st.metric("Avg Expense", f"${stats['average_expense']:.2f}")
        with col3:
            st.metric("Min Expense", f"${stats['min_expense']:.2f}")
        with col4:
            st.metric("Max Expense", f"${stats['max_expense']:.2f}")
        with col5:
            st.metric("Transactions", stats['transaction_count'])
        
        st.markdown(f"**Date Range:** {stats['date_range']}")
        
        # Data table
        st.subheader("📋 Transaction Details")
        st.dataframe(df, use_container_width=True)
        
        # Data export
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Cleaned Data",
            data=csv,
            file_name="cleaned_expenses.csv",
            mime="text/csv"
        )


# ==================== CATEGORY ANALYSIS PAGE ====================
elif app_mode == "💼 Category Analysis":
    st.markdown("# 💼 Category Analysis")
    
    if st.session_state.df_categorized is None:
        st.warning("⚠️ Please upload and process data first!")
    else:
        df = st.session_state.df_categorized
        
        # Spending by category
        spending_by_category = get_spending_by_category(df)
        
        st.subheader("💰 Total Spending by Category")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            bars = ax.bar(spending_by_category.index, spending_by_category.values, color=colors[:len(spending_by_category)])
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'${height:.2f}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            ax.set_xlabel('Category', fontsize=12, fontweight='bold')
            ax.set_ylabel('Amount ($)', fontsize=12, fontweight='bold')
            ax.set_title('Spending Distribution by Category', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            # Summary stats
            st.subheader("Summary")
            total = spending_by_category.sum()
            for category, amount in spending_by_category.items():
                percentage = (amount / total * 100)
                st.metric(category, f"${amount:.2f}", f"{percentage:.1f}%")
        
        # Detailed category statistics
        st.subheader("📈 Detailed Category Statistics")
        category_stats = get_category_statistics(df)
        st.dataframe(category_stats, use_container_width=True)
        
        # Pie chart for proportion
        st.subheader("🥧 Spending Proportion")
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        wedges, texts, autotexts = ax.pie(
            spending_by_category.values,
            labels=spending_by_category.index,
            autopct='%1.1f%%',
            colors=colors[:len(spending_by_category)],
            startangle=90
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Spending Distribution (%)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Category distribution (count)
        st.subheader("📊 Transaction Count by Category")
        category_distribution = get_category_distribution(df)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(category_distribution.index, category_distribution.values, color=colors[:len(category_distribution)])
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Category', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Number of Transactions by Category', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)


# ==================== PREDICTIONS & INSIGHTS PAGE ====================
elif app_mode == "🔮 Predictions & Insights":
    st.markdown("# 🔮 Predictions & Insights")
    
    if st.session_state.df_categorized is None:
        st.warning("⚠️ Please upload and process data first!")
    else:
        df = st.session_state.df_categorized
        
        # Tabs for different insights
        tab1, tab2, tab3, tab4 = st.tabs(["💡 Predictions", "📊 Trends", "⚠️ Anomalies", "💼 Category Insights"])
        
        # TAB 1: Predictions
        with tab1:
            st.subheader("Next Month Expense Prediction")
            
            months_to_predict = st.slider("Months to predict", 1, 12, 1)
            
            if st.button("🔮 Generate Predictions", type="primary"):
                predictions, model_info = predict_next_month(df, months_ahead=months_to_predict)
                
                if predictions is None:
                    st.error(f"❌ {model_info.get('error', 'Prediction failed')}")
                else:
                    # Model quality indicator
                    r2_score = model_info['r2_score']
                    
                    if r2_score > 0.7:
                        quality_indicator = "🟢 Good"
                    elif r2_score > 0.4:
                        quality_indicator = "🟡 Fair"
                    else:
                        quality_indicator = "🔴 Poor"
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Model Quality", quality_indicator)
                    with col2:
                        st.metric("R² Score", f"{r2_score:.3f}")
                    with col3:
                        st.metric("Avg Monthly Spending", f"${model_info['mean_monthly_spending']:.2f}")
                    
                    st.info(f"⚠️ Predictions are based on linear trend. Use with caution for planning.")
                    
                    # Predictions table
                    predictions_data = []
                    for i, (pred, date) in enumerate(zip(predictions, model_info['prediction_dates']), 1):
                        predictions_data.append({
                            'Month': date.strftime('%B %Y'),
                            'Predicted Spending': f"${pred:.2f}"
                        })
                    
                    pred_df = pd.DataFrame(predictions_data)
                    st.dataframe(pred_df, use_container_width=True)
                    
                    # Visualization
                    fig, ax = plt.subplots(figsize=(12, 6))
                    
                    # Historical data
                    df_monthly = df.copy()
                    df_monthly['YearMonth'] = df_monthly['Date'].dt.to_period('M')
                    historical = df_monthly.groupby('YearMonth')['Amount'].sum().reset_index()
                    historical['Date'] = historical['YearMonth'].dt.to_timestamp()
                    
                    ax.plot(historical['Date'], historical['Amount'], 'o-', label='Historical', linewidth=2, markersize=8)
                    ax.plot(model_info['prediction_dates'], predictions, 's--', label=f'Predicted (next {months_to_predict} months)', linewidth=2, markersize=8, color='red')
                    
                    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
                    ax.set_ylabel('Amount ($)', fontsize=12, fontweight='bold')
                    ax.set_title('Expense Trend & Prediction', fontsize=14, fontweight='bold')
                    ax.legend(fontsize=11)
                    ax.grid(alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
        
        # TAB 2: Trends
        with tab2:
            st.subheader("📊 Spending Trends")
            
            trend_analysis = get_spending_trend(df)
            
            if trend_analysis['trend'] != 'insufficient_data':
                st.markdown(f"## {trend_analysis['trend_text']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("First Half Avg", f"${trend_analysis['first_half_avg']:.2f}")
                with col2:
                    st.metric("Second Half Avg", f"${trend_analysis['second_half_avg']:.2f}")
                with col3:
                    st.metric("Change %", f"{trend_analysis['change_percent']:.2f}%")
                
                # Historical trend plot
                df_monthly = df.copy()
                df_monthly['YearMonth'] = df_monthly['Date'].dt.to_period('M')
                monthly_sum = df_monthly.groupby('YearMonth')['Amount'].sum().reset_index()
                monthly_sum['Month'] = monthly_sum['YearMonth'].astype(str)
                
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(range(len(monthly_sum)), monthly_sum['Amount'].values, 'o-', linewidth=2, markersize=8, color='#1f77b4')
                ax.set_xlabel('Month', fontsize=12, fontweight='bold')
                ax.set_ylabel('Amount ($)', fontsize=12, fontweight='bold')
                ax.set_title('Monthly Spending Trend', fontsize=14, fontweight='bold')
                ax.set_xticks(range(len(monthly_sum)))
                ax.set_xticklabels(monthly_sum['Month'].values, rotation=45, ha='right')
                ax.grid(alpha=0.3)
                
                # Add trend line
                z = np.polyfit(range(len(monthly_sum)), monthly_sum['Amount'].values, 1)
                p = np.poly1d(z)
                ax.plot(range(len(monthly_sum)), p(range(len(monthly_sum))), "r--", alpha=0.8, linewidth=2, label='Trend')
                ax.legend()
                
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("⚠️ " + trend_analysis['message'])
        
        # TAB 3: Anomalies
        with tab3:
            st.subheader("⚠️ Unusual Spending Detected")
            
            anomalies = detect_anomalies(df, threshold_std=2)
            
            if len(anomalies) > 0:
                st.warning(f"🔴 Found {len(anomalies)} unusual transactions (>2 std from mean)")
                st.dataframe(anomalies[['Date', 'Description', 'Amount', 'Category']].sort_values('Amount', ascending=False), use_container_width=True)
                
                # Summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Anomalous Amount", f"${anomalies['Amount'].sum():.2f}")
                with col2:
                    st.metric("Average Anomalous Amount", f"${anomalies['Amount'].mean():.2f}")
                with col3:
                    st.metric("Count", len(anomalies))
            else:
                st.success("✅ No unusual spending detected!")
        
        # TAB 4: Category Insights
        with tab4:
            st.subheader("💼 Category-based Insights")
            
            spending_by_category = get_spending_by_category(df)
            total_spending = spending_by_category.sum()
            
            # Identify overspending
            avg_per_category = total_spending / len(spending_by_category)
            
            st.markdown("### 💡 Smart Insights:")
            
            for category, amount in spending_by_category.items():
                percentage = (amount / total_spending * 100)
                
                if amount > avg_per_category * 1.5:
                    st.warning(
                        f"⚠️ **{category}**: ${amount:.2f} ({percentage:.1f}%) - "
                        f"This is {(amount/avg_per_category - 1)*100:.0f}% above average!",
                        icon="📈"
                    )
                elif amount < avg_per_category * 0.5:
                    st.info(
                        f"✅ **{category}**: ${amount:.2f} ({percentage:.1f}%) - Well controlled spending",
                        icon="📉"
                    )
                else:
                    st.success(
                        f"📊 **{category}**: ${amount:.2f} ({percentage:.1f}%)",
                        icon="➡️"
                    )
            
            # Recommendations
            st.markdown("### 🎯 Recommendations:")
            top_category = spending_by_category.index[0]
            top_amount = spending_by_category.iloc[0]
            
            if top_amount / total_spending > 0.4:
                st.warning(
                    f"⚠️ **{top_category}** accounts for {(top_amount/total_spending*100):.1f}% of spending. "
                    f"Consider setting a budget limit for this category."
                )
            
            # Best control category
            best_category = spending_by_category.index[-1]
            st.success(f"✅ **{best_category}** is your least spending category - keep it up!")


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
    <p>Smart Expense Analyzer v1.0 | Built with Streamlit, Pandas & Scikit-learn</p>
    </div>
    """,
    unsafe_allow_html=True
)
