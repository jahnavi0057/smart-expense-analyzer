"""Test script to verify all functionality works correctly"""

import sys
import pandas as pd
from utils.preprocessing import load_and_validate_csv, clean_data, calculate_basic_stats
from utils.categorization import categorize_expenses, get_spending_by_category, get_category_statistics
from utils.prediction import predict_next_month, get_spending_trend, detect_anomalies

print("=" * 60)
print("SMART EXPENSE ANALYZER - FUNCTIONALITY TEST")
print("=" * 60)

# Test 1: Load sample data
print("\n✓ TEST 1: Loading sample data...")
try:
    df = pd.read_csv('sample_expenses.csv')
    print(f"  ✅ Loaded {len(df)} transactions")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 2: Clean data
print("\n✓ TEST 2: Cleaning data...")
try:
    df_cleaned, summary = clean_data(df)
    print(f"  ✅ Cleaned data: {summary['final_rows']} rows")
    print(f"     - Duplicates removed: {summary['duplicates_removed']}")
    print(f"     - Missing values removed: {summary['rows_with_missing_values']}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 3: Categorize expenses
print("\n✓ TEST 3: Categorizing expenses...")
try:
    df_categorized = categorize_expenses(df_cleaned)
    categories = df_categorized['Category'].unique()
    print(f"  ✅ Found {len(categories)} categories: {list(categories)}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 4: Calculate statistics
print("\n✓ TEST 4: Calculating statistics...")
try:
    stats = calculate_basic_stats(df_categorized)
    print(f"  ✅ Total expenses: ${stats['total_expenses']:.2f}")
    print(f"     - Average expense: ${stats['average_expense']:.2f}")
    print(f"     - Transactions: {stats['transaction_count']}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 5: Get spending by category
print("\n✓ TEST 5: Spending by category...")
try:
    spending = get_spending_by_category(df_categorized)
    print(f"  ✅ Category breakdown:")
    for category, amount in spending.items():
        percentage = (amount / spending.sum() * 100)
        print(f"     - {category}: ${amount:.2f} ({percentage:.1f}%)")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 6: Category statistics
print("\n✓ TEST 6: Detailed category statistics...")
try:
    cat_stats = get_category_statistics(df_categorized)
    print(f"  ✅ Generated statistics for {len(cat_stats)} categories")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 7: Spending trends
print("\n✓ TEST 7: Analyzing spending trends...")
try:
    trend = get_spending_trend(df_categorized)
    print(f"  ✅ Trend: {trend['trend_text']}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 8: Predictions
print("\n✓ TEST 8: Predicting next month...")
try:
    predictions, model_info = predict_next_month(df_categorized, months_ahead=1)
    if predictions:
        print(f"  ✅ Prediction: ${predictions[0]:.2f}")
        print(f"     - R² Score: {model_info['r2_score']:.3f}")
    else:
        print(f"  ⚠️  {model_info.get('error', 'Prediction unavailable')}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 9: Anomaly detection
print("\n✓ TEST 9: Detecting anomalies...")
try:
    anomalies = detect_anomalies(df_categorized)
    print(f"  ✅ Found {len(anomalies)} anomalies")
    if len(anomalies) > 0:
        print(f"     - Highest: ${anomalies['Amount'].max():.2f}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - Ready to run Streamlit app!")
print("=" * 60)
print("\nTo start the app, run:")
print("  streamlit run app.py")
print("=" * 60)
