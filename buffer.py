#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import feedparser
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from pyquery import PyQuery as Pq
from core.webengine import BrowserBuffer
from html import unescape as html_unescape
from core.utils import eval_in_emacs, PostGui, get_emacs_vars, interactive, message_to_emacs, get_emacs_func_result

class AppBuffer(BrowserBuffer):
    def __init__(self, buffer_id, url, arguments):
        BrowserBuffer.__init__(self, buffer_id, url, arguments, False)

        self.load_index_html(__file__)

        self.index_file_dir = os.path.join(os.path.dirname(__file__), "dist")
        self.index_file = os.path.join(self.index_file_dir, "index.html")

        self.pic_file_dir = os.path.join(os.path.dirname(__file__), "src")
        self.pic_file_dir = os.path.join(self.pic_file_dir, "assets")
        self.pic_file = os.path.join(self.pic_file_dir, "logo.png")

        self.rsshub_json_dir = os.path.join(os.path.dirname(__file__), "public")
        self.rsshub_json = os.path.join(self.rsshub_json_dir, "list.json")

        self.feedlink_json_dir = os.path.join(os.path.dirname(__file__), "public")
        self.feedlink_json = os.path.join(self.feedlink_json_dir, "link.json")

        self.url = url
        
        self.feedlink_list = []
        self.rsshub_list = []

        self.mainItem = SaveLoadFeeds(self.feedlink_json, self.rsshub_json)

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
        
        '''
        # 解析 feed, 在此添加 feed
        self.link_feeds_list = [
                      "https://www.with-emacs.com/rss.xml",
                      "https://www.oschina.net/news/rss",
                      "https://www.oschina.net/project/rss",
                    ]
        for item in self.link_feeds_list:
            rss = RssFeedParser(item).feed_info
            self.rsshub.append(rss)
        '''
        # self.mainItem.add_feedlink_widget("https://www.with-emacs.com/rss.xml")
        # self.mainItem.add_feedlink_widget("https://www.oschina.net/news/rss")
        # self.mainItem.test_method()
        # vue 注入数据
        self.first_file = os.path.expanduser(arguments)
        self.buffer_widget.loadFinished.connect(self.load_first_file)        
        
        # 写json
        # with open(self.json_file, "w") as f:
        #    f.write(json.dumps(self.mainItem.rsshub_list, ensure_ascii=False))

    def fetch_link_list(self):
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

    # add from vue
    @QtCore.pyqtSlot(str)
    def add_feedlink(self, new_feedlink):
        self.mainItem.add_feedlink_widget(new_feedlink)
        self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))

        # this.selectFeedByIndex(newIndex-1) is faster than window.pyobject.add_feedlink(new_feedlink);
        self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(len(self.mainItem.feedlink_list)-1)))

    @QtCore.pyqtSlot(int)
    def remove_feedlink(self, feedlink):
        self.handle_remove_feed(feedlink)

    @QtCore.pyqtSlot(str, str, bool)
    def change_read_status(self, feedlink_index, article_index, status):
        feedlink_index = int(feedlink_index)
        article_index = int(article_index)
        self.mainItem.rsshub_list[feedlink_index]['feed_article_list'][article_index]['isRead'] = status
        self.mainItem.save_rsshub_json()

    @QtCore.pyqtSlot(str)
    def refresh_feed_link_list(self):
        pass

    def alter_read_status(self):
        feedlink_index = self.buffer_widget.execute_js("getCurFeedIndex()")
        article_index = self.buffer_widget.execute_js("getCurArticleIndex()")
        article_status = self.buffer_widget.execute_js("getCurArticleStatus()")
        article_title = self.buffer_widget.execute_js("getCurArticleTitle()")
        
        self.mainItem.rsshub_list[feedlink_index]['feed_article_list'][article_index]['isRead'] = not article_status
        self.mainItem.save_rsshub_json()

        # method1 : reload the list.json to javascript
        # self.buffer_widget.eval_js(
        #    '''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list))
        #    )

        # method2 : call articlePanel.vue -> changeReadStatus(key)
        article_status = self.buffer_widget.execute_js("getCurArticleStatus()")
        self.buffer_widget.eval_js(
            '''changeReadStatus(\"{}\", \"{}\", \"{}\");'''.format(article_title, not article_status, 1)
            )

    def load_first_file(self):
        self.buffer_widget.eval_js(
            '''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list))
            )
    
    @interactive
    def add_feed(self):
        self.send_input_message("Add new feed: ", "add_feed")

    # add from emacs    
    def handle_add_feed(self, new_feedlink):
        if new_feedlink in self.mainItem.feedlink_list:
            message_to_emacs("Feedlink '{}' exists.".format(new_feedlink))
        else: 
            success_flag = self.mainItem.add_feedlink_widget(new_feedlink)
            if (success_flag == 1):
                self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))
                self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(len(self.mainItem.feedlink_list)-1)))
                message_to_emacs("Add new feedlink '{}' success.".format(new_feedlink))

    def handle_remove_feed(self, feedlink_index):
        # 先确认是否删除
        # ...

        # 选中状态，下移；没有选中就不变

        feed_title = self.mainItem.rsshub_list[feedlink_index]['feed_title']
        feed_num = len(self.mainItem.feedlink_list) - 1
        success_flag = self.mainItem.remove_feedlink_widget(feedlink_index)
        if success_flag:
            self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))
            if feed_num == 1:
                self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(-1)))
            else:
                self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(feedlink_index - 1)))
            self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))
            message_to_emacs("Remove Feed-Index {} success.".format(feed_title))
        else:
            message_to_emacs("Failed to remove link, please check you current Feed-Index {}.".format(feedlink_index))

    def goBack(self):
        self.buffer_widget.eval_js("goBack();")

    def handle_input_response(self, callback_tag, result_content):
        if callback_tag == "add_feed":
            self.handle_add_feed(result_content)
        elif callback_tag == "remove_feed":
            print("remove_feed")
        
        elif callback_tag == "show_list_status_all":
            print("show_list_status_all")
        elif callback_tag == "show_list_status_read":
            print("show_list_status_red")
        elif callback_tag == "show_list_status_unread":
            print("show_list_status_unrrefreshed")
        
        elif callback_tag == "show_all_feed":
            print("show_all_feed")
        elif callback_tag == "origin":
            print("origin")

class SaveLoadFeeds:
    def __init__(self, feedlink_json, rsshub_json):
        self.feedlink_list = []
        self.rsshub_list = []

        self.feedlink_json = feedlink_json
        self.rsshub_json = rsshub_json
        self.last_feed_index = -1

        self.fetch_feedlink_list()
        self.fetch_rsshub_list()
        
        if len(self.feedlink_list) == 0:
            self.last_feed_index = -1
        else:
            self.last_feed_index = len(self.feedlink_list) - 1

    def save_rsshub_json(self):
        with open(self.rsshub_json, "w") as f:
            f.write(json.dumps(self.rsshub_list, ensure_ascii=False))

    def save_feedlink_json(self): 
        with open(self.feedlink_json, "w") as f:
            f.write(json.dumps(self.feedlink_list, ensure_ascii=False))

    def fetch_rsshub_list(self):
        if not os.path.exists(self.rsshub_json):
            file = open(self.rsshub_json, 'w')
            file.write("")
            file.close()
        with open(self.rsshub_json, "r") as f:
            try:
                self.rsshub_list = json.load(f)
            except json.decoder.JSONDecodeError:
                pass

    def fetch_feedlink_list(self):
        if not os.path.exists(self.feedlink_json):
            file = open(self.feedlink_json, 'w')
            file.write("")
            file.close()
        with open(self.feedlink_json, 'r') as f:
            try:
                self.feedlink_list = json.load(f)
            except json.decoder.JSONDecodeError:
                pass
    
    # 0 : add feedlink faild
    # 1 : add feedlink success
    def add_feedlink_widget(self, new_feedlink):
        try:
            self.last_feed_index += 1
            new_rss = RssFeedParser(new_feedlink, self.last_feed_index).feed_info
        except AttributeError:
            self.last_feed_index -= 1
            return 0
        self.feedlink_list.append(new_feedlink)
        self.save_feedlink_json()

        self.rsshub_list.append(new_rss)
        self.save_rsshub_json()
        return 1

    # 0 : remove feedlink faild
    # 1 : remove feedlink success 
    def remove_feedlink_widget(self, feedlink_index):
        
        print("last")
        print(self.last_feed_index + 1)
        print("feedlink_index")
        print(feedlink_index)

        if not feedlink_index in range(0, self.last_feed_index + 1):
            return 0 
        self.feedlink_list.pop(feedlink_index)
        self.save_feedlink_json()

        for item in self.rsshub_list[feedlink_index::]:
            item['feed_index'] -= 1
        self.rsshub_list.pop(feedlink_index)
        self.save_rsshub_json()

        self.last_feed_index -= 1
        return 1

    # 调试用，检查文件更新情况
    def test_method(self):
        print("**********show feed_link_list**********")
        print(self.feedlink_list)
        print('\n\n\n')
        print("**********show rss_hub**********")
        print(self.rsshub_list)
        print('\n\n\n')        

class RssFeedParser:
    def __init__(self, feed, index):
        self.feed = feed
        self.d = feedparser.parse(self.feed)
        try:
            self.title = self.d.feed.title
        except AttributeError:
            message_to_emacs("AttributeError please check your link {}".format(self.feed))
            return 
        self.subtitle = self.d.feed.subtitle
        self.article_list = self.get_article_list(self.d.entries)
        self.feed_info = {
            "feed_link" : self.feed,
            "feed_title" : self.title,
            "feed_subtitle" : self.subtitle,
            "feed_index" : index,
            "feed_article_list" : self.article_list
        }

    def get_article_list(self, article_entries):
        article_list = []
        article_index = 0
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
                "index" : article_index,
                "description" : description,
                # 截取前 120 字放入 cardList 呈现
                "shortDescription" : description if len(description) <= 120 else description[: 120] + "...",
                "isRead" : False
            }
            article_list.append(item)
            article_index += 1

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

