from datetime import datetime

def time_trans(time):
    """日期字串轉換系統時間"""
    return datetime.strptime(time, "%Y-%m-%d")