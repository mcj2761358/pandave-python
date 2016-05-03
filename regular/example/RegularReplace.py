import re

content = '近日 , 一位网友的帖子让无数人感动泪崩。帖子中写到该网友无意中点进了已故 5 年多的高中同学的 QQ 空间 , 却发现自 2010 年同学不幸离世至今 5 年多的时间里 , 同学母亲一直坚持不断地在儿子的 QQ 空间留言板上留言。<br><br><noscript><img src="https://pic3.zhimg.com/e0e856c5539acb9fa7215f988bae808a_b.jpg" data-rawwidth="349" data-rawheight="600" class="content_image" width="349"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="349" data-rawheight="600" class="content_image lazy" width="349" data-actualsrc="https://pic3.zhimg.com/e0e856c5539acb9fa7215f988bae808a_b.jpg"><br><noscript><img src="https://pic3.zhimg.com/fd188bf3ad6b37b49c8c0bcfaf249366_b.jpg" data-rawwidth="342" data-rawheight="600" class="content_image" width="342"></noscript><img src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg" data-rawwidth="342" data-rawheight="600" class="content_image lazy" width="342" data-actualsrc="https://pic3.zhimg.com/fd188bf3ad6b37b49c8c0bcfaf249366_b.jpg"><br><br><br><br>收获这么多赞很高兴，高兴这个世界上母爱是被大多数人拥有与认同的，希望在外漂泊的游子，包括有幸能够待在父母身边的人，珍惜过去的我们或曾忽略的财富，因为，有些东西，如果失去了，便不会再拥有。'

content = content.replace("<noscript>","");
content = content.replace("</noscript>","");


pattern = re.compile(r'<img src="//zhstatic.zhihu.com.*?>')
results = re.findall(pattern, content)

for validImg in results :
    # print(validImg)
    content = content.replace(validImg,"");
    # print(content)

pattern = re.compile(r'<img src=".*?".*?width=(.*?) .*?>')
results = re.findall(pattern, content)
for width in results :
    content = content.replace(width,'width="80%"');
    # print(width);


answerContent = '有山有水有动物<br><img data-rawwidth="720" data-rawheight="537" src="https://pic1.zhimg.com/e190cc9bf12eb797a6f6946f756a78b0_b.jpeg" class="origin_image zh-lightbox-thumb" width="720" data-original="https://pic1.zhimg.com/e190cc9bf12eb797a6f6946f756a78b0_r.jpeg">';
imgFlagPattern = re.compile(r'<img.*?src="https://.*?".*?>')
imgFlagResult = re.findall(imgFlagPattern, answerContent);
# print(imgFlagResult)




spiderUrl = "http://www.zhihu.com/question/20899988/a";
spiderpattern = re.compile(r'http://www.zhihu.com/question/\d+$')
results = re.match(spiderpattern,spiderUrl)
print(results)
