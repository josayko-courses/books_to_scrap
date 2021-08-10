def urlcat(base, chunk):
    for str in chunk.split('/'):
        if str != "..":
            base += ('/' + str)
    return base
