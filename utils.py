def get_pw(file):
    pw = None
    with open(file) as f:
        pw = f.read()
    return pw
