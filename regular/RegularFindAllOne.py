import re

pattern = re.compile(r'\d+')

match = re.findall(pattern, 'one1two2three3four4')


print(match)