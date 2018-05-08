import re
string = "A"
regex = re.compile(r'([A-Z][0-9]?->[a-z][A-Z]?([|][a-z][A-Z]?)*(\n|\Z))*')
print(regex.match(string))
