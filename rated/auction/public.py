#!/usr/bin/env python3

__author__ = 'golim'

'''
REDACTED
'''

def validate_sql_query(sql_query):
    BANNED_KEYWORDS = ['select', 'union', '"', "'", "sleep", 'where', 'and', '=', '*']

    if any(keyword in sql_query.lower() for keyword in BANNED_KEYWORDS):
        return False

    return True

def execute_query(sql_query):
    with db.engine.connect() as connection:
        try:
            result = connection.execute(sql_query)
            result = result.fetchone()
            return result
        except Exception as e:
            return None

def load_product_with_price(product_id, price):
    # Check for hacking attempts
    if not validate_sql_query(price):
        logger.error(f'Hacking Attempt Detected: {price}')
        return 'Hacking Attempt Detected'

    # Check if the price is higher than the current price
    try:
        # Normalize the query, since MySQL does not like unicode
        result = execute_query(text(unicodedata.normalize("NFKD",
        f"S----- * F--- ------- W---- -- = ------------ A-- ------- - -----".split(';')[0]).encode('ascii', 'ignore').decode('ascii')))
    except Exception as e:
        if 'Invalid query.' in str(e):
            return 'Hacking Attempt Detected'
        return None

    return result

'''
REDACTED
'''
