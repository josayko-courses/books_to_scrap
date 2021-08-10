def urlcat(base, str):
    for str in str.split('/'):
        if str != "..":
            base += ('/' + str)
    return base


def urlnext(str):
    next_url = ""
    for str in str.split('/'):
        if ".html" not in str:
            next_url += str
    return next_url
