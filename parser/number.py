def trim_to_next_number(string: str):
    string = str(string)
    for l in string:
        if l.isnumeric():
            break
        string = string[1:]
    return string
