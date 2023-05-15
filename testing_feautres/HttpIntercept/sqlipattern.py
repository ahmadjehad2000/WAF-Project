import re
# sqli_blacklist = [
#     "SELECT", "CREATE", "INSERT", "FROM", "ALTER", "ADD", "PRIMARY",
#     "UPDATE",
#     "SET",
#     "DELETE",
#     "TRUNCATE",
#     "WHERE",
#     "OR",
#     "AND",
#     "DROP"
# ]


def pattern_apost(url) -> bool:
    if re.search(r"(%27)", url):
        return True
    else:
        return False


def pattern_comment(url) -> bool:
    if re.search(r"(%23)", url):
        return True
    else:
        return False


def pattern_keyword(url):
    if re.search(r"(SELECT)", url):
        return True
    elif re.search(r"(CREATE)", url):
        return True
    elif re.search(r"(INSERT)", url):
        return True
    elif re.search(r"(ALTER)", url):
        return True
    elif re.search(r"(TRUNCATE)", url):
        return True
    elif re.search(r"(DROP)", url):
        return True
    else:
        return False
