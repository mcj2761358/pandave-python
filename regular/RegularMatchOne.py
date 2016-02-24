import re

# 将正则表达式编译成pattern对象,注意hello前面的r意思是原生字符串
pattern = re.compile(r'hello')

# 使用re.match匹配文包,获取匹配结果,无法匹配事返回None
result1 = re.match(pattern, 'hello A hello')
result2 = re.match(pattern, 'helloo Minutch')
result3 = re.match(pattern, 'helo Minutch')
result4 = re.match(pattern, 'hello Minutch')

#如果1匹配成功
if result1:
    print(result1.group())
else:
    print('1匹配失败')

#如果2匹配成功
if result2:
    print(result2.group())
else:
    print('2匹配失败')

#如果3匹配成功
if result3:
    print(result3.group())
else:
    print('3匹配失败')

#如果4匹配成功
if result4:
    print(result4.group())
else:
    print('4匹配失败')














