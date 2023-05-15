import re
sqli_blacklist = [
    "SELECT", "CREATE", "INSERT", "FROM", "ALTER", "ADD", "PRIMARY",
    "UPDATE",
    "SET",
    "DELETE",
    "TRUNCATE",
    "WHERE",
    "OR",
    "AND",
    "DROP"
]


def getKeyword():
    url = "NORMAL192.168.73.152/checkdb.php?name = WHERE+user+%3D+23 & pass = where"
    if re.search(r"(WHERE)", url):
        return True
    else:
        return False


print(getKeyword())
