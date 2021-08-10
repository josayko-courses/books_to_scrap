def urlcat(base, str):
    for str in str.split('/'):
        if str != "..":
            base += ('/' + str)
    return base
