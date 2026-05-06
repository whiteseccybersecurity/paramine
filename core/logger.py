VERBOSE = True

def set_verbose(value):
    global VERBOSE
    VERBOSE = value

def info(message):
    if VERBOSE:
        print(message)

def vuln(message):
    print(message)