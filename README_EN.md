dfad
## What is weixin_crawler?

weixin_crawler is a WeChat public account article crawler implemented using Scrapy, Flask, Echarts, Elasticsearch, etc., with its own analysis report and full-text search function, millions of documents can be searched instantly. The original intention of weixin_crawler is to crawl the history of WeChat public as much and as quickly as possible.

If you want to see if this project is interesting first, this less than 3 minute intro video must be what you need:

https://www.youtube.com/watch?v=CbfLRCV7oeU&t=8s

## main feature

Written in Python3

2. The crawler framework is Scrapy and actually uses many features of Scrapy. It is a good open source project for deep learning of Scrapy.

3. Use Flask, Flask-socketio, Vue to achieve a highly available UI interface. Powerful and practical, a good data assistant for new media operations and other positions

4. Thanks to the use of Scrapy, MongoDB, Elasticsearch, data crawling, storage, and indexing are simple and efficient

5. Support all historical post crawling of WeChat public account

6. Support crawling of data such as reading, likes, praises, and comments on WeChat public account articles

7. Comes with a data analysis report for a single public account

8. Use Elasticsearch to achieve full-text search, support multiple search and pattern and sorting patterns, and provide trend analysis charts for search results

9. Support for grouping public numbers, you can use grouped data to limit the search scope

10. Original mobile phone automatic operation method can realize unsupervised crawler

11. Anti-climbing measures are simple and rude

## Main tools used

| Language | | Python3.6 |
| --- | ------- | ------------------------------------- -------- |
| Frontend | Web Framework | Flask / Flask-socketio / gevent |
| | js / css library | Vue / Jquery / W3css / Echarts / Front-awsome |
| Backend | Reptiles | Scrapy |
| | Storage | Mongodb / Redis |
| | Index | Elasticsearch |

## Running method

> #### Insatall mongodb / redis / elasticsearch and run them in the background
>
> 1. downlaod mongodb / redis / elasticsearch from their official sites and install them
>
> 2. run them at the same time under the default configuration. In this case mongodb is localhost: 27017 redis is localhost: 6379 (or you have to config in weixin_crawler / project / configs / auth.py)
>
> #### Install proxy server and run proxy.js
>
> 1. install nodejs and then npm install anyproxy and redis in weixin_crawler / proxy
>
> 2. cd to weixin_crawler / proxy and run node proxy.js
>
> 3. install anyproxy https CA in both computer and phone side
>
> 4. if you are not sure how to use anyproxy, [here] (https://github.com/alibaba/anyproxy) is the doc
>
> #### Install the needed python packages
>
> 1. NOTE: you may can not simply type pip install -r requirements.txt to install every package, twist is one of them which is needed by scrapy
>
> 2. I am not sure if your python enviroment will throw other package not found error, just install any package that is needed
>
> #### Some source code have to be modified (maybe it is not reasonable)
>
> 1. scrapy Python36 \ Lib \ site-packages \ scrapy \ http \ request \ \ __ init \ __. Py-> weixin_crawler \ source_code \ request \\ __ init \ __. Py
>
> 2. scrapy Python36 \ Lib \ site-packages \ scrapy \ http \ response \ \ __ init \ __. Py-> weixin_crawler \ source_code \ response \\\ __ init \ __. Py
>
> 3. pyecharts Python36 \ Lib \ site-packages \ pyecharts \ base.py-> weixin_crawler \ source_code \ base.py. In this case function get_echarts_options is added in line 106
>
> #### If you want weixin_crawler work automatically those steps are necessary or you shoud operate the phone to get the request data that will be detected by Anyproxy manual
>
> 1. Install abd and add it to your path (windows for example)
>
> 2. install android emulator (NOX suggested) or plugin your phone and make sure you can operate them with abd from command line tools
>
> 3. If mutiple phone are connected to your computer you have to find out their adb ports which will be used to add crawler
>
> #### Run the main.py
>
> Just run python weixin_crawler \ project \ main.py. Now open the browser and everything you want would be in localhost: 5000.
>
> In this long step list you may get stucked, join our community for help, tell us what you have done and what kind of error you have found.
>
> Let's go to explore the world in localhost: 5000 together

## function display

UI main interface

! [1] (readme_img / Crawler main interface.gif)

Add public account crawl task and list of crawled public accounts

! [1] (readme_img / public number.png)

Reptile interface

! [] (readme_img / caiji.png)

Set interface

! [] (readme_img / settings.png)

Public account history article list

! [] (readme_img / list of historical articles.gif)

report

! [] (readme_img / report.gif)

search for

! [] (readme_img / search.gif)

## Join the community

Maybe you belong to:

-Just graduated from technical white, no project development experience

-Old driver who can easily make weixin_crawler run

-Reptile Daniel

-You may be engaged in new media operations and do not understand programming at all, but hope to make full use of the various functions of weixin_crawler to serve your own work

No matter what category you belong to, as long as you have a strong interest in WeChat data analysis, joining our community through the author WeChat can get what you want.

## Give back to the author

weixin_crawler has been developed in free time since June 2018 (it took half a year), but the level of helpless authors is limited, so far I can barely come up with a usable version to share with all crawler enthusiasts, thank you for your expectations. If you like this project, look forward to your feedback.

You can give back to the author in any of the following ways (multiple choices are possible):

-A small star, and share this interesting open source project with other developers, even if there is only one, as long as he is also advancing on the road of technological advancement

-Give the author a cup of coffee, so staying up late in the fight will be a bit more efficient :)

-Join the community to contribute code, and let's create cooler crawlers together

-Join Knowledge Planet and listen to the author's thoughts on every function of weixin_crawler and every problem solving thought process, so you will know more determined developers

Author WeChat (remarks start with wc) | Join Knowledge Planet | Reward Authors |
| ----------------------- | ------------------------- | ----------------------- |
|! [] (readme_img / wq.jpg) |! [] (readme_img / Knowledge Planet.png) |! [] (readme_img / 打 赏 .png) |