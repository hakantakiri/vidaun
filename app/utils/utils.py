def clean_name(name: str):
    clean_name = ''
    for c in name:
        if( c >'a' and c<'z') or  (c >'A' and c<'Z') or (c >'0' and c<'9') or (c == '_' or c == "-"):
            clean_name = clean_name + "" + c
    return clean_name
