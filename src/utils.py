def winTicksToUnixTime(w_ts):
    WINDOWS_TICK_PER_SEC = 10000000
    SEC_TO_UNIX_EPOCH = 11644473600
    
    return w_ts / WINDOWS_TICK_PER_SEC - SEC_TO_UNIX_EPOCH

