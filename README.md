# zhihu_link

## requirements
* MongoDB
* Neo4j
* pymongo
* py2neo
* requests
* BeautifulSoup

## MISC
* 这个爬虫需要自己的知乎cookie才能爬取。建议使用chrome，安装EditThisCookie插件，将知乎的cookie复制粘贴到zhihu_cookie.json文件。
* 知乎用户的唯一性不是靠用户名，而是html里内嵌隐藏的data-id，在ajax获取数据是发送的表单数据里也需要这个值。所以Neo4j中使用此值可以唯一标识用户。
* 关于此爬虫的具体的一些细节可以参考博文[基于Neo4j的知乎关系爬虫](http://tripleday.github.io/2016/06/29/zhihu-link/)。