#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import json
import feedparser
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from pyquery import PyQuery as Pq
from core.webengine import BrowserBuffer
from html import unescape as html_unescape

class AppBuffer(BrowserBuffer):
    def __init__(self, buffer_id, url, arguments):
        BrowserBuffer.__init__(self, buffer_id, url, arguments, False)

        self.load_index_html(__file__)

        self.index_file_dir = os.path.join(os.path.dirname(__file__), "dist")
        self.index_file = os.path.join(self.index_file_dir, "index.html")

        self.pic_file_dir = os.path.join(os.path.dirname(__file__), "src")
        self.pic_file_dir = os.path.join(self.pic_file_dir, "assets")
        self.pic_file = os.path.join(self.pic_file_dir, "logo.png")

        self.json_file_dir = os.path.join(os.path.dirname(__file__), "public")
        self.json_file = os.path.join(self.json_file_dir, "list.json")

        self.link_json_file_dir = os.path.join(os.path.dirname(__file__), "public")
        self.link_json_file = os.path.join(self.link_json_file_dir, "link.json")

        self.url = url
        self.link_list = []
        self.rsshub = []

        self.mainItem = SaveLoadFeeds(self.link_json_file, self.json_file)
        
        ''' self.sl_obj = SaveLoadFeeds(self.json_file)
        self.pre_feeds = self.sl_obj.fetch_feeds
        print("hello")
        print(type(self.pre_feeds))
        print("hello") '''
        
        ''' for feed in self.feeds:
            self.rss = RssFeedParser(feed)
            self.sl_obj.add_new_feed(self.rss.feed_info) '''

        with open(self.index_file, "r", encoding='utf-8') as f:
            html = self.convert_index_html(f.read(), self.index_file_dir)
            self.buffer_widget.setHtml(html, QUrl("file://"))

        ''' self.sl_obj.save_feeds;
        self.feed_info = self.sl_obj.cur_feed; '''
        
        # 解析 feed, 在此添加 feed
        self.feeds = [
                      "https://www.with-emacs.com/rss.xml",
                      "https://www.oschina.net/news/rss",
                      "https://www.oschina.net/project/rss",
                    ]
        for item in self.feeds:
            rss = RssFeedParser(item).feed_info
            self.rsshub.append(rss)

        # vue 注入数据
        self.first_file = os.path.expanduser(arguments)
        self.buffer_widget.loadFinished.connect(self.load_first_file)        
        
        # 写json
        with open(self.json_file, "w") as f:
            f.write(json.dumps(self.rsshub, ensure_ascii=False))

    def fetch_lick_list(self):
        self.mainItem.get_feed_link_list()
        self.link_list = self.self.mainItem.link_list
    
    def fetch_rss_hub(self):
        '''
        这里需要一个更新rss_hub的算法
        比较新的解析文件和已有的解析文件
        将已读文章去除而保留未读文章
        添加新解析文件的文章

        或者，S(新的解析文件) - S(旧的解析文件中的已读)
        S表示集合
        '''
        self.link_list = self.self.mainItem.rss_hub

    @QtCore.pyqtSlot(str)
    def add_feed_link(self, feed_link):
        self.mainItem.add_feed_link_widget(feed_link)
        
    @QtCore.pyqtSlot(str)
    def remove_feed_link(self, feed_link):
        self.mainItem.remove_feed_link_widget(feed_link)

    @QtCore.pyqtSlot(str)
    def mark_as_read(self, article_title):
        pass

    @QtCore.pyqtSlot(str)
    def mark_as_unread(self, article_title):
        pass

    def load_first_file(self):
        self.buffer_widget.execute_js('''addFiles({});'''.format(json.dumps(self.rsshub)))

    def add_subscription(self):
        self.send_input_message("Subscribe to RSS feed: ", "add_subscription")

    def handle_input_response(self, callback_tag, result_content):
        # print 调试用
        if callback_tag == "add_feed":
            print("add_feed")
            self.send_input_message("Subscribe to RSS feed: ", "add_subscription")
            self.buffer_widget.add_subscription(result_content)
        elif callback_tag == "remove_feed":
            print("remove_feed")
        elif callback_tag == "mark_as_read":
            print("mark_as_read")
        elif callback_tag == "mark_as_un_read":
            print("mark_as_un_read")
        elif callback_tag == "show_list_status_all":
            print("show_list_status_all")
        elif callback_tag == "show_list_status_read":
            print("show_list_status_red")
        elif callback_tag == "show_list_status_unread":
            print("show_list_status_unred")
        elif callback_tag == "show_all_feed":
            print("show_all_feed")
        elif callback_tag == "origin":
            print("origin")
        elif callback_tag == "goback":
            print("goback")

class SaveLoadFeeds:
    def __init__(self, link_json_file, json_file):
        self.feed_link_list = []
        self.rss_hub = []
        self.link_json_file = link_json_file
        self.json_file = json_file

    def save_json_file(self):
        with open(self.json_file, "w") as f:
            f.write(json.dumps(self.rss_hub, ensure_ascii=False))

    def save_link_json_file(self):
        with open(self.link_json_file, "w") as f:
            f.write(json.dumps(self.feed_link_list, ensure_ascii=False))

    def get_feed_link_list(self):
        with open(self.json_file, 'r') as f:
            self.feed_link_list = json.load(f)
    
    def add_feed_link_widget(self, feed_link):
        self.link_json_file.append(feed_link)
        self.save_feed_link_file()
        new_rss = RssFeedParser(feed_link).feed_info
        self.rsshub.append(new_rss)
        self.save_json_file()

    def remove_feed_link_widget(self, feed_link):
        self.feed_link_list.remove(feed_link)
        self.save_feed_link_file()
        for item in self.rss_hub:
            if item.feed == feed_link:
                self.rss_hub.remove(item)
                break
        self.save_json_file()

    # 调试用，检查文件更新情况
    def test_method(self):
        print("**********show feed_link_list**********")
        print(self.feed_link_list)
        print('\n\n\n')
        print("**********show rss_hub**********")
        print(self.rss_hub)
        print('\n\n\n')

class RssFeedParser:
    def __init__(self, feed):
        self.feed = feed
        self.d = feedparser.parse(self.feed)
        self.title = self.d.feed.title
        self.subtitle = self.d.feed.subtitle
        self.article_list = self.get_article_list(self.d.entries)
        self.feed_info = {
            "feed_link" : self.feed,
            "feed_title" : self.title,
            "feed_subtitle" : self.subtitle,
            "feed_article_list" : self.article_list
        }

    def get_article_list(self, article_entries):
        article_list = []

        for item in article_entries:
            # 部分 entry 没有 author 属性
            try:
                author = item.author
            except AttributeError:
                author = ""
            description = self.get_description(item.summary)

            item = {
                "title" : item.title,
                "link" : item.link,
                "time" : item.published,
                "author" : author, 
                "description" : description,
                # 截取前 120 字放入 cardList 呈现
                "shortDescription" : description if len(description) <= 120 else description[: 120] + "...",
                "isRead" : False
            }
            article_list.append(item)

        return article_list

    def handle_html_tag(self, html):
        rss_str = html_unescape(str(html))
        html = Pq(html)
        for ul in html("ul").items():
            for li in ul("li").items():
                li_str_search = re.search("<li>(.+)</li>", repr(str(li)))
                rss_str = rss_str.replace(str(li), f"\n- {li_str_search.group(1)}").replace(
                    "\\n", "\n"
                ) 
            
        for ol in html("ol").items():
            for index, li in enumerate(ol("li").items()):
                li_str_search = re.search("<li>(.+)</li>", repr(str(li)))
                rss_str = rss_str.replace(
                    str(li), f"\n{index + 1}. {li_str_search.group(1)}"
                ).replace("\\n", "\n")
        rss_str = re.sub("</?(ul|ol)>", "", rss_str)
        # 处理没有被 ul / ol 标签包围的 li 标签
        rss_str = rss_str.replace("<li>", "- ").replace("</li>", "")

        # <a> 标签处理
        for a in html("a").items():
            a_str = re.search(r"<a.+?</a>", html_unescape(str(a)), flags=re.DOTALL)[0]
            if a.text() and str(a.text()) != a.attr("href"):
                rss_str = rss_str.replace(a_str, f" {a.text()}: {a.attr('href')}\n")
            else:
                rss_str = rss_str.replace(a_str, f" {a.attr('href')}\n") 

        # 处理一些 HTML 标签
        html_tags = [
            "a","b","i","p","s","h1","h2","h3","h4","h5","code","del","div","dd","dl","dt","em","font","iframe","pre","small","span","strong","sub","table","td","th","tr",
        ]
        # 直接去掉标签，留下内部文本信息
        for i in html_tags:
            rss_str = re.sub(rf'<{i} .+?"/?>', "", rss_str)
            rss_str = re.sub(rf"</?{i}>", "", rss_str)

        rss_str = re.sub('<br .+?"/>|<(br|hr) ?/?>', "\n", rss_str)
        rss_str = re.sub(r"</?h\d>", "\n", rss_str)

        # 删除图片、视频标签
        rss_str = re.sub(r'<video .+?"?/>|</video>|<img.+?>', "", rss_str)

        # 去掉多余换行
        while re.search("\n\n", rss_str):
            rss_str = re.sub("\n\n", "\n", rss_str)
        rss_str = rss_str.strip()

        return rss_str

    def get_description(self, raw_description):
        description = self.handle_html_tag(raw_description)
        return description
