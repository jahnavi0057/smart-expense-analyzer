# 💰 Smart Expense Analyzer

A modern, interactive web application built with **Streamlit** for analyzing, categorizing, and predicting personal expenses. Get insights into your spending patterns and make informed financial decisions.

## ✨ Features

### 📤 Data Upload & Processing
- Upload CSV files with transaction data (Date, Description, Amount)
- Automatic data validation and cleaning
- Handles missing values, duplicates, and invalid data
- Real-time data quality metrics

### 💼 Expense Categorization
Automatically categorizes transactions into:
- **Food** 🍔 (restaurants, groceries, cafes)
- **Transport** 🚗 (uber, taxi, fuel, parking)
- **Bills** 📋 (utilities, phone, insurance, subscriptions)
- **Shopping** 🛍️ (clothing, electronics, online shopping)
- **Others** 📌 (miscellaneous)

### 📊 Comprehensive Analytics
- **Total spending** and expense statistics
- **Category breakdown** with visual representations
- **Bar charts** showing spending by category
- **Pie charts** displaying spending distribution
- Transaction count analysis
- Detailed category statistics (count, sum, average, min, max, percentage)

### 🔮 Predictions & Forecasting
- **Linear Regression model** for expense prediction
- Predict spending for next 1-12 months
- Model quality indicator (R² score)
- Historical vs. predicted visualization
- Spending trend analysis (increasing/decreasing/stable)

### ⚠️ Advanced Insights
- **Anomaly detection** for unusual transactions
- **Overspending warnings** per category
- **Smart recommendations** based on spending patterns
- **Spending trend analysis** comparing first half vs. second half
- Category-specific insights and recommendations

## 📁 Project Structure

```
expense_analyzer/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── sample_expenses.csv         # Sample data for testing
├── test.py                     # Test script
└── utils/
    ├── __init__.py
    ├── preprocessing.py        # Data cleaning and validation
    ├── categorization.py       # Expense categorization logic
    └── prediction.py           # Linear regression predictions
```

## 🚀 Quick Start

### 1. Installation

Clone or download the project:
```bash
cd expense_analyzer
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Test Functionality (Optional)

```bash
python test.py
```

This runs automated tests to verify all features are working correctly.

## 📋 Usage Guide

### Step 1: Upload Your Data
1. Navigate to the "📤 Upload & Process" section
2. Prepare a CSV file with columns:
   - **Date**: Transaction date (format: YYYY-MM-DD)
   - **Description**: What you spent money on
   - **Amount**: Transaction amount
3. Click "Upload CSV file" and select your file
4. Review the preview of raw data

Example CSV format:
```
Date,Description,Amount
2024-01-01,Grocery Shopping,45.50
2024-01-02,Gas Station,35.00
2024-01-03,Restaurant,28.75
```

### Step 2: Clean & Preprocess
1. Click "Clean & Preprocess Data"
2. Review the cleaning summary (duplicates removed, invalid data, etc.)
3. Automatically categorized and ready for analysis

### Step 3: Analyze Categories
1. Go to "💼 Category Analysis"
2. View spending by category (total amounts and percentages)
3. Explore detailed statistics
4. Check transaction counts per category

### Step 4: View Predictions & Insights
1. Navigate to "🔮 Predictions & Insights"
2. **💡 Predictions Tab**: Set months to predict and see spending forecast
3. **📊 Trends Tab**: Analyze if spending is increasing or decreasing
4. **⚠️ Anomalies Tab**: Identify unusual transactions
5. **💼 Category Insights Tab**: Get smart recommendations

### Step 5: Download Results
- Download cleaned data as CSV
- All visualizations can be saved directly from the Streamlit interface

## 🛠️ Technology Stack

- **Streamlit** 1.31.1 - Interactive web framework
- **Pandas** 2.1.4 - Data manipulation and analysis
- **Numpy** 1.26.3 - Numerical computing
- **Scikit-learn** 1.3.2 - Machine learning (Linear Regression)
- **Matplotlib** 3.8.2 - Data visualization
- **Python** 3.8+

## 📊 Sample Data

A `sample_expenses.csv` file is included with 75 sample transactions across 3 months. Use this to test the application immediately!

```bash
# To test with sample data:
1. Open the app (streamlit run app.py)
2. Click "Upload CSV file" and select sample_expenses.csv
3. Click "Clean & Preprocess Data"
4. Explore all the analysis features
```

## 🔍 How It Works

### Data Cleaning
- Removes duplicates
- Validates date and amount formats
- Removes rows with missing critical values
- Removes negative amounts (assuming all expenses are positive)
- Sorts by date

### Categorization
Uses keyword matching on transaction descriptions:
- Matches keywords like "grocery", "fuel", "restaurant", etc.
- Assigns transactions to appropriate categories
- Falls back to "Others" if no match found

### Prediction Model
- Aggregates expenses by month
- Uses Linear Regression with time as feature
- Calculates R² score for model quality
- Predicts future spending based on historical trend

### Anomaly Detection
- Calculates mean and standard deviation of expenses
- Flags transactions > 2 standard deviations from mean
- Great for identifying unusual purchases

## 💡 Tips & Best Practices

1. **CSV Format**: Ensure your Date column is in YYYY-MM-DD format
2. **Description Quality**: More detailed descriptions help with categorization
3. **Consistent Data**: Use consistent transaction descriptions for better categorization
4. **Regular Updates**: Feed the app new transactions for more accurate predictions
5. **Validation**: Review categorized transactions and recategorize if needed

## ⚙️ Configuration

No configuration needed! The app works out of the box. However, you can modify:

- **Anomaly Detection Threshold**: In `utils/prediction.py`, change `threshold_std` parameter
- **Keywords**: In `utils/categorization.py`, modify `CATEGORY_KEYWORDS` to add/remove keywords
- **Date Format**: Automatically detects common date formats

## 📈 Model Accuracy

The Linear Regression model accuracy depends on:
- **Number of months**: More data = better predictions
- **Spending consistency**: Volatile spending = lower accuracy
- **Trend**: Strong trends = better predictions

R² Score Guide:
- **> 0.7** 🟢 Good model
- **0.4 - 0.7** 🟡 Fair model
- **< 0.4** 🔴 Poor model (use with caution)

## 🐛 Troubleshooting

### "Missing required columns" error
- Ensure your CSV has exactly these columns: `Date`, `Description`, `Amount`
- Check spelling and case sensitivity

### "Error converting Date column"
- Check date format is YYYY-MM-DD
- Try: 2024-01-31, 2024/01/31, or 01-31-2024

### "Insufficient data for prediction"
- You need at least 2 months of data
- Add more transactions and try again

### Streamlit not found
```bash
pip install streamlit==1.31.1
python -m streamlit run app.py
```

## 📝 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Feel free to modify and extend this application:
- Add more categories
- Implement different prediction models
- Add export formats (PDF, Excel)
- Create custom alerts and notifications

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the sample CSV format
3. Run the test script to verify functionality

---

**Happy Expense Tracking! 💰📊**
