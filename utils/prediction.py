"""Expense prediction utilities using Linear Regression"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta


def prepare_data_for_prediction(df):
    """
    Prepare data for time series prediction.
    
    Args:
        df (pd.DataFrame): Dataframe with Date and Amount columns
        
    Returns:
        pd.DataFrame: Monthly aggregated data with numeric date features
        dict: Information about the data
    """
    df = df.copy()
    df['YearMonth'] = df['Date'].dt.to_period('M')
    
    # Aggregate by month
    monthly_data = df.groupby('YearMonth')['Amount'].sum().reset_index()
    monthly_data.columns = ['YearMonth', 'Amount']
    
    # Convert to datetime for easier calculations
    monthly_data['Date'] = monthly_data['YearMonth'].dt.to_timestamp()
    
    # Create numeric feature (days since first date)
    first_date = monthly_data['Date'].min()
    monthly_data['DaysSinceStart'] = (monthly_data['Date'] - first_date).dt.days
    
    return monthly_data, {
        'num_months': len(monthly_data),
        'first_month': monthly_data['YearMonth'].iloc[0],
        'last_month': monthly_data['YearMonth'].iloc[-1],
        'mean_monthly_spending': monthly_data['Amount'].mean()
    }


def predict_next_month(df, months_ahead=1):
    """
    Predict spending for the next month(s) using Linear Regression.
    
    Args:
        df (pd.DataFrame): Dataframe with Date and Amount columns
        months_ahead (int): Number of months to predict ahead
        
    Returns:
        list: Predicted amounts for each month
        dict: Model information
    """
    monthly_data, info = prepare_data_for_prediction(df)
    
    # Need at least 2 data points
    if len(monthly_data) < 2:
        return None, {'error': 'Insufficient data for prediction (need at least 2 months)'}
    
    # Prepare features (X) and target (y)
    X = monthly_data[['DaysSinceStart']].values
    y = monthly_data['Amount'].values
    
    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate R² score
    r2_score = model.score(X, y)
    
    # Prepare data for prediction
    last_days_since_start = monthly_data['DaysSinceStart'].iloc[-1]
    last_date = monthly_data['Date'].iloc[-1]
    
    predictions = []
    prediction_dates = []
    
    for i in range(1, months_ahead + 1):
        # Assume 30 days per month on average
        future_days = last_days_since_start + (i * 30)
        predicted_amount = model.predict([[future_days]])[0]
        
        # Don't predict negative spending
        predicted_amount = max(0, predicted_amount)
        predictions.append(predicted_amount)
        
        future_date = last_date + timedelta(days=i*30)
        prediction_dates.append(future_date)
    
    model_info = {
        'r2_score': r2_score,
        'coefficient': model.coef_[0],
        'intercept': model.intercept_,
        'num_months_trained': len(monthly_data),
        'prediction_dates': prediction_dates,
        'mean_monthly_spending': monthly_data['Amount'].mean()
    }
    
    return predictions, model_info


def get_spending_trend(df):
    """
    Analyze spending trend over time.
    
    Args:
        df (pd.DataFrame): Dataframe with Date and Amount columns
        
    Returns:
        dict: Trend analysis
    """
    df = df.copy()
    df['YearMonth'] = df['Date'].dt.to_period('M')
    
    monthly_data = df.groupby('YearMonth')['Amount'].sum().reset_index()
    
    if len(monthly_data) < 2:
        return {'trend': 'insufficient_data', 'message': 'Need at least 2 months of data'}
    
    first_half_avg = monthly_data['Amount'].iloc[:len(monthly_data)//2].mean()
    second_half_avg = monthly_data['Amount'].iloc[len(monthly_data)//2:].mean()
    
    change_percent = ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0
    
    if change_percent > 5:
        trend = 'increasing'
        trend_text = f"📈 Spending is INCREASING by {change_percent:.1f}%"
    elif change_percent < -5:
        trend = 'decreasing'
        trend_text = f"📉 Spending is DECREASING by {abs(change_percent):.1f}%"
    else:
        trend = 'stable'
        trend_text = f"📊 Spending is STABLE (change: {change_percent:.1f}%)"
    
    return {
        'trend': trend,
        'trend_text': trend_text,
        'change_percent': change_percent,
        'first_half_avg': first_half_avg,
        'second_half_avg': second_half_avg
    }


def detect_anomalies(df, threshold_std=2):
    """
    Detect unusually high spending transactions.
    
    Args:
        df (pd.DataFrame): Dataframe with Amount column
        threshold_std (float): Number of standard deviations for anomaly detection
        
    Returns:
        pd.DataFrame: Dataframe with anomalous transactions (high spending outliers)
    """
    df = df.copy()
    
    mean = df['Amount'].mean()
    std = df['Amount'].std()
    
    # Mark anomalies
    df['IsAnomaly'] = df['Amount'] > (mean + threshold_std * std)
    
    anomalies = df[df['IsAnomaly']]
    
    return anomalies[[col for col in df.columns if col != 'IsAnomaly']]
