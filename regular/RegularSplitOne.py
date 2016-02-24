import re

pattern = re.compile(r'\d+')

# match = re.split(pattern, 'one1two2three3four4')
match = re.split(pattern, 'one')


print(match)