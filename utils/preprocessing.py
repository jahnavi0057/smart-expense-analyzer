"""Data preprocessing utilities for expense data"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_and_validate_csv(uploaded_file):
    """
    Load CSV file and validate required columns.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        pd.DataFrame: Loaded dataframe or None if validation fails
        str: Error message or None if successful
    """
    try:
        df = pd.read_csv(uploaded_file)
        
        # Check required columns
        required_columns = ['Date', 'Description', 'Amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return None, f"Missing required columns: {', '.join(missing_columns)}"
        
        return df, None
    except Exception as e:
        return None, f"Error loading file: {str(e)}"


def clean_data(df):
    """
    Clean and preprocess expense data.
    
    Args:
        df (pd.DataFrame): Raw dataframe with Date, Description, Amount
        
    Returns:
        pd.DataFrame: Cleaned dataframe
        dict: Summary of cleaning operations
    """
    original_rows = len(df)
    cleaning_summary = {}
    
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # Remove duplicates
    duplicates_removed = len(df) - len(df.drop_duplicates())
    df = df.drop_duplicates()
    cleaning_summary['duplicates_removed'] = duplicates_removed
    
    # Remove rows with missing critical values
    initial_rows = len(df)
    df = df.dropna(subset=['Date', 'Description', 'Amount'])
    rows_with_missing_values = initial_rows - len(df)
    cleaning_summary['rows_with_missing_values'] = rows_with_missing_values
    
    # Convert Date to datetime
    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except Exception as e:
        raise ValueError(f"Error converting Date column: {str(e)}")
    
    # Convert Amount to numeric, removing any non-numeric characters
    try:
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        invalid_amounts = df['Amount'].isna().sum() - rows_with_missing_values
        df = df.dropna(subset=['Amount'])
        cleaning_summary['invalid_amounts_removed'] = max(0, invalid_amounts)
    except Exception as e:
        raise ValueError(f"Error converting Amount column: {str(e)}")
    
    # Remove negative amounts (assuming expenses are positive)
    negative_amounts = len(df[df['Amount'] < 0])
    df = df[df['Amount'] >= 0]
    cleaning_summary['negative_amounts_removed'] = negative_amounts
    
    # Strip whitespace from Description
    df['Description'] = df['Description'].str.strip()
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    cleaning_summary['final_rows'] = len(df)
    cleaning_summary['total_rows_removed'] = original_rows - len(df)
    
    return df, cleaning_summary


def get_monthly_data(df):
    """
    Extract year-month from date and group expenses by month.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        
    Returns:
        pd.DataFrame: Dataframe with added YearMonth column
    """
    df = df.copy()
    df['YearMonth'] = df['Date'].dt.to_period('M')
    return df


def calculate_basic_stats(df):
    """
    Calculate basic statistics for expenses.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        
    Returns:
        dict: Dictionary with statistics
    """
    return {
        'total_expenses': df['Amount'].sum(),
        'average_expense': df['Amount'].mean(),
        'min_expense': df['Amount'].min(),
        'max_expense': df['Amount'].max(),
        'transaction_count': len(df),
        'date_range': f"{df['Date'].min().date()} to {df['Date'].max().date()}"
    }
