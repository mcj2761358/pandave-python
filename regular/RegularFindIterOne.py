import re

pattern = re.compile(r'\d+')

match = re.finditer(pattern, 'one2two2three3four4')

for con in match :
    print(con.group())