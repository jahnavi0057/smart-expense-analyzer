"""Expense categorization utilities"""

import pandas as pd


# Keyword mappings for categories
CATEGORY_KEYWORDS = {
    'Food': [
        'restaurant', 'cafe', 'coffee', 'lunch', 'dinner', 'breakfast',
        'grocery', 'supermarket', 'pizza', 'burger', 'food', 'drinks',
        'bakery', 'milk', 'bread', 'chicken', 'beef', 'fish', 'vegetable',
        'fruit', 'fast food', 'delivery', 'uber eats', 'food delivery'
    ],
    'Transport': [
        'uber', 'taxi', 'bus', 'train', 'metro', 'car', 'fuel', 'gas',
        'parking', 'transit', 'transportation', 'flight', 'airfare',
        'hotel', 'travel', 'bike', 'rental', 'lyft', 'grab'
    ],
    'Bills': [
        'electricity', 'water', 'internet', 'phone', 'mobile', 'utility',
        'bill', 'subscription', 'insurance', 'rent', 'payment', 'loan',
        'tax', 'credit card', 'monthly', 'services'
    ],
    'Shopping': [
        'amazon', 'mall', 'shop', 'store', 'retail', 'clothing', 'dress',
        'shoes', 'electronics', 'phone', 'laptop', 'computer', 'gadget',
        'book', 'game', 'toy', 'furniture', 'home', 'decor', 'walmart',
        'target', 'best buy'
    ],
    'Others': []  # Default category
}


def get_category_for_description(description):
    """
    Categorize an expense based on its description.
    
    Args:
        description (str): Description of the expense
        
    Returns:
        str: Category name
    """
    if not isinstance(description, str):
        return 'Others'
    
    description_lower = description.lower()
    
    # Check each category's keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        if category == 'Others':
            continue
        for keyword in keywords:
            if keyword in description_lower:
                return category
    
    return 'Others'


def categorize_expenses(df):
    """
    Add category column to dataframe based on descriptions.
    
    Args:
        df (pd.DataFrame): Dataframe with 'Description' column
        
    Returns:
        pd.DataFrame: Dataframe with added 'Category' column
    """
    df = df.copy()
    df['Category'] = df['Description'].apply(get_category_for_description)
    return df


def get_spending_by_category(df):
    """
    Calculate total spending per category.
    
    Args:
        df (pd.DataFrame): Dataframe with 'Amount' and 'Category' columns
        
    Returns:
        pd.Series: Total amount per category, sorted descending
    """
    return df.groupby('Category')['Amount'].sum().sort_values(ascending=False)


def get_category_statistics(df):
    """
    Get detailed statistics per category.
    
    Args:
        df (pd.DataFrame): Dataframe with 'Amount' and 'Category' columns
        
    Returns:
        pd.DataFrame: Statistics including count, sum, mean, min, max
    """
    category_stats = df.groupby('Category')['Amount'].agg([
        ('Count', 'count'),
        ('Total', 'sum'),
        ('Average', 'mean'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(2)
    
    category_stats['Percentage'] = (
        (category_stats['Total'] / category_stats['Total'].sum() * 100)
        .round(2)
    )
    
    return category_stats.sort_values('Total', ascending=False)


def get_category_distribution(df):
    """
    Get count of transactions per category.
    
    Args:
        df (pd.DataFrame): Dataframe with 'Category' column
        
    Returns:
        pd.Series: Count of transactions per category
    """
    return df['Category'].value_counts()


def recategorize_transaction(df, index, new_category):
    """
    Manually update category for a specific transaction.
    
    Args:
        df (pd.DataFrame): Dataframe
        index (int): Row index
        new_category (str): New category name
        
    Returns:
        pd.DataFrame: Updated dataframe
    """
    df = df.copy()
    if index < len(df):
        df.at[index, 'Category'] = new_category
    return df
