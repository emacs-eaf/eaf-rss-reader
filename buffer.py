#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import time
import feedparser
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QThread
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

        self.rsshub_json_dir = os.path.join(os.path.dirname(__file__), "public")
        self.rsshub_json = os.path.join(self.rsshub_json_dir, "list.json")
        
        self.feedlink_json_dir = os.path.join(os.path.dirname(__file__), "public")
        self.feedlink_json = os.path.join(self.feedlink_json_dir, "link.json")

        self.url = url
        self.refresh_time = 600
        self.view_key_map = {'all':0, 'read': 1, 'unread':2}
        self.view_key_list = ['all', 'read', 'unread']
        
        self.add_feedlink_threads = []
        self.refresh_feedlink_threads = []
        self.keep_refresh_rss_threads = []

        self.mainItem = SaveLoadFeeds(self.feedlink_json, self.rsshub_json)

        with open(self.index_file, "r", encoding='utf-8') as f:
            html = self.convert_index_html(f.read(), self.index_file_dir)
            self.buffer_widget.setHtml(html, QUrl("file://"))

        self.first_file = os.path.expanduser(arguments)
        self.buffer_widget.loadFinished.connect(self.load_first_file)        
        
        self.keep_refresh_rss(self.refresh_time)
        

    def load_first_file(self):
        self.buffer_widget.eval_js(
            '''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list))
            )

    def add_feedlink_thread(self, feedlink, index):
        thread = FetchRssFeedParserThread(feedlink, index)
        thread.fetch_result.connect(self.add_feedlink_widget)
        self.add_feedlink_threads.append(thread)
        thread.start()

    def keep_refresh_rss(self, refresh_time):
        thread = KeepRefreshRss(self.feedlink_json, self.rsshub_json, self.refresh_time)
        thread.fetch_result.connect(self.auto_refresh_rsshub_list)
        self.keep_refresh_rss_threads.append(thread)
        thread.start()

    # call add from emacs    
    def handle_add_feed(self, new_feedlink):
        index = self.mainItem.last_feed_index + 1
        self.add_feedlink_thread(new_feedlink, index)

    def alter_read_status(self):
        feedlink_index = self.buffer_widget.execute_js("giveCurFeedIndex()")
        article_index = self.buffer_widget.execute_js("giveCurArticleIndex()")
        article_status = self.mainItem.rsshub_list[feedlink_index]['feed_article_list'][article_index]['isRead']
        article_title = self.mainItem.rsshub_list[feedlink_index]['feed_article_list'][article_index]['title']

        if (article_index < 0):
            return 
        self.mainItem.rsshub_list[feedlink_index]['feed_article_list'][article_index]['isRead'] = not article_status
        self.mainItem.save_rsshub_json()

        # method1 : reload the list.json to javascript
        # self.buffer_widget.eval_js(
        #    '''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list))
        #    )

        # method2 : call articlePanel.vue -> changeReadStatus(key)
        self.buffer_widget.eval_js(
            '''changeReadStatus(\"{}\", \"{}\", \"{}\");'''.format(article_title, not article_status, 1)
            )

        if article_status == False:
            message_to_emacs("Set {} as read.".format(article_title))
        else:
            message_to_emacs("Set {} as unread.".format(article_title))

    def remove_feed_widget(self, feedlink_index, curFeedIndex):
        feed_title = self.mainItem.rsshub_list[feedlink_index]['feed_title']
        feed_link = self.mainItem.rsshub_list[feedlink_index]['feed_link']
        # feed selected, select next feed
        if curFeedIndex != -1:
            feed_count = len(self.mainItem.feedlink_list)
            success_flag = self.mainItem.remove_feedlink_widget(feedlink_index)
            if success_flag:
                self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))
                if feed_count == 1:
                    self.buffer_widget.eval_js('''changeCurFeedByIndex({});'''.format(json.dumps(-1)))
                    self.buffer_widget.eval_js('''changeCurArticleByIndex({});'''.format(json.dumps(-1)))
                    self.buffer_widget.eval_js('''changeOpenFeed({});'''.format(json.dumps('false')))
                    self.buffer_widget.eval_js('''changeOpenArticle({});'''.format(json.dumps('false')))
                else:
                    self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(feedlink_index)))
                    self.buffer_widget.eval_js('''changeCurArticleByIndex({});'''.format(json.dumps(-1)))
                    self.buffer_widget.eval_js('''changeOpenFeed({});'''.format(json.dumps('false')))
                    self.buffer_widget.eval_js('''changeOpenArticle({});'''.format(json.dumps('false')))
                message_to_emacs("Feed: \"{}\" \"{}\", index:\"{}\", has been removed".format(feed_title, feed_link, feedlink_index))
            else:
                message_to_emacs("Failed to remove link, please check you current Feed-Index {}.".format(feedlink_index))
        # feed not selected
        else:
            success_flag = self.mainItem.remove_feedlink_widget(feedlink_index)    
            if success_flag:
                self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))
                self.buffer_widget.eval_js('''changeCurFeedByIndex({});'''.format(json.dumps(-1)))
                self.buffer_widget.eval_js('''changeCurArticleByIndex({});'''.format(json.dumps(-1)))
                self.buffer_widget.eval_js('''changeOpenArticle({});'''.format(json.dumps('false')))
                self.buffer_widget.eval_js('''changeOpenFeed({});'''.format(json.dumps('false')))
                message_to_emacs("Feed: \"{}\" \"{}\", index:\"{}\", has been removed".format(feed_title, feed_link, feedlink_index))
            else:
                message_to_emacs("Failed to remove link, please check you current Feed-Index {}.".format(feedlink_index))

    def refresh_feedlink_thread(self, index):
        feedlink = self.mainItem.rsshub_list[index]['feed_link']
        thread = FetchRssFeedParserThread(feedlink, index)
        thread.fetch_result.connect(self.refresh_feedlink_widget)
        self.refresh_feedlink_threads.append(thread)
        thread.start()

        def handle_refresh_rsshub_list(self):
          curFeedIndex = self.buffer_widget.execute_js("giveCurFeedIndex()")
        self.refresh_feedlink_thread(curFeedIndex)

    # call remove from emacs
    def handle_remove_feed(self):
        curFeedIndex = self.buffer_widget.execute_js("giveCurFeedIndex()")
        self.remove_feed_widget(curFeedIndex, curFeedIndex)

    def select_next_view_key(self):
        cur_view_key = self.buffer_widget.execute_js("giveViewKey()")
        cur_view_num = self.view_key_map[cur_view_key]
        # use mod to make the line to a cycle
        cur_view_num = (cur_view_num + 1) % 3
        selected_key = self.view_key_list[cur_view_num]
        self.buffer_widget.eval_js('''changeViewKey({});'''.format(json.dumps(selected_key)))

    def select_prev_view_key(self):
        cur_view_key = self.buffer_widget.execute_js("giveViewKey()")
        cur_view_num = self.view_key_map[cur_view_key]
        cur_view_num = (cur_view_num - 1) % 3
        selected_key = self.view_key_list[cur_view_num]
        self.buffer_widget.eval_js('''changeViewKey({});'''.format(json.dumps(selected_key)))

    @interactive
    def add_feed(self):
        self.send_input_message("Add new feed: ", "add_feed")

    @interactive
    def remove_feed(self):
        ''' Remove current selected feed.'''
        self.send_input_message("Are you sure you want to remove this feed?", "remove_feed", "yes-or-no")

    @PostGui()
    def auto_refresh_rsshub_list(self, article_list, index, diff, pointer):
        if pointer == 1:
            message_to_emacs("All updates have been completed.")
        elif article_list == ['refresh_start'] and pointer == 0:
            message_to_emacs("Updating. It is recommended not to add or delete feeds.")
        elif article_list == ['AttributeError'] and pointer == 0:
            link = self.mainItem.feedlink_list[index]
            message_to_emacs("Failed to refresh link '{}', maybe you refresh too frequently.".format(link))
        else:
            title = self.mainItem.rsshub_list[index]['feed_title']
            message_to_emacs("The content of '{}' is up-to-date and {} articles have been updated.".format(title, diff))
            self.mainItem.rsshub_list[index]['feed_article_list'] = article_list
            self.mainItem.save_rsshub_json()
            self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))

    @PostGui()
    def add_feedlink_widget(self, new_rss, new_feedlink):
        if new_feedlink in self.mainItem.feedlink_list:
            message_to_emacs("Feedlink '{}' exists.".format(new_feedlink))
        else: 
            flag = self.mainItem.add_feedlink_widget(new_rss)
            if (flag == 1):
                self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))
                self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(len(self.mainItem.feedlink_list)-1)))
                message_to_emacs("Successfully add new feedlink '{}'.".format(new_feedlink))
            else:
              message_to_emacs("Failed to add feed, please check your link {}.".format(new_feedlink))

    @PostGui()
    def refresh_feedlink_widget(self, new_rss, feedlink):
        if new_rss == {}:
            message_to_emacs("Failed to refresh link '{}', maybe you refresh too frequently.".format(feedlink_index))
            return
        feedlink_index = new_rss["feed_index"]
        feed_title = new_rss["feed_title"]
        new_rss_article_list = new_rss["feed_article_list"]
        old_rss = self.mainItem.rsshub_list[feedlink_index]["feed_article_list"]
        old_rss_map = {}
        for item in old_rss:
            title = item['title']
            status = item['isRead']
            old_rss_map[title] = status
        
        for item in new_rss_article_list:
            new_title = item["title"]
            new_index = item["index"]
            if new_title in old_rss_map:
                new_rss_article_list[new_index]['isRead'] = old_rss_map[new_title]

        self.mainItem.rsshub_list[feedlink_index]["feed_article_list"] = new_rss_article_list
        
        self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.mainItem.rsshub_list)))    
        self.buffer_widget.eval_js('''changeCurArticleByIndex({});'''.format(json.dumps(-1)))
        self.buffer_widget.eval_js('''changeCurFeedByIndex({});'''.format(json.dumps(feedlink_index)))
        self.buffer_widget.eval_js('''changeOpenArticle({});'''.format(json.dumps('false')))
        self.buffer_widget.eval_js('''changeOpenFeed({});'''.format(json.dumps('true')))
        self.mainItem.save_rsshub_json()
        message_to_emacs("Refresh feed:{} link:{} success.".format(feed_title, feedlink))

    # call add from vue
    @QtCore.pyqtSlot(str)
    def add_feedlink(self, new_feedlink):
        index = self.mainItem.last_feed_index + 1
        self.add_feedlink_thread(new_feedlink, index)

    # call remove from vue
    @QtCore.pyqtSlot(str, str)
    def remove_feedlink(self, feedlink_index, curFeedIndex):
        feedlink_index = int(feedlink_index)
        curFeedIndex = int(curFeedIndex)
        self.remove_feed_widget(feedlink_index, curFeedIndex)
        
    @QtCore.pyqtSlot(str, str, bool)
    def change_read_status(self, feedlink_index, article_index, status):
        feedlink_index = int(feedlink_index)
        article_index = int(article_index)
        article_title = self.mainItem.rsshub_list[feedlink_index]['feed_article_list'][article_index]['title']

        self.mainItem.rsshub_list[feedlink_index]['feed_article_list'][article_index]['isRead'] = status
        self.mainItem.save_rsshub_json()

        if status == True:
            message_to_emacs("Set {} as read.".format(article_title))
        else:
            message_to_emacs("Set {} as unread.".format(article_title))

    @QtCore.pyqtSlot(str)
    def view_original_page(self, url):
        eval_in_emacs("eaf-open-browser-other-window", [url])

    # call refresh from vue
    @QtCore.pyqtSlot(str)
    def refresh_rsshub_list(self, feedlink_index):
        feedlink_index = int(feedlink_index)
        if feedlink_index < 0:
            return 
        self.refresh_feedlink_thread(feedlink_index)

    def handle_input_response(self, callback_tag, result_content):
        if callback_tag == "add_feed":
            self.handle_add_feed(result_content)
        elif callback_tag == "remove_feed":
            self.handle_remove_feed()

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
    def add_feedlink_widget(self, new_rss):
        new_feedlink = ''
        if new_rss == {}:
            return 0
        else:
            self.last_feed_index += 1
            new_feedlink = new_rss['feed_link']
        
        self.feedlink_list.append(new_feedlink)
        self.save_feedlink_json()

        self.rsshub_list.append(new_rss)
        self.save_rsshub_json()
        return 1

    # 0 : remove feedlink faild
    # 1 : remove feedlink success 
    def remove_feedlink_widget(self, feedlink_index):
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

    def reget_all(self):
        file = open(self.rsshub_json, 'w')
        file.write("")
        file.close()
        self.last_feed_index = -1
        for item in self.feedlink_list:
            self.last_feed_index += 1
            rss = RssFeedParser(item, self.last_feed_index).feed_info
            self.rsshub_list.append(rss)
            message_to_emacs('{} load finished!'.format(item))
        self.save_rsshub_json()
    

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
        # remove <li> withoout ol ul
        rss_str = rss_str.replace("<li>", "- ").replace("</li>", "")

        # handle <a>
        for a in html("a").items():
            a_str = re.search(r"<a.+?</a>", html_unescape(str(a)), flags=re.DOTALL)[0]
            if a.text() and str(a.text()) != a.attr("href"):
                rss_str = rss_str.replace(a_str, f" {a.text()}: {a.attr('href')}\n")
            else:
                rss_str = rss_str.replace(a_str, f" {a.attr('href')}\n") 

        # remove tags
        html_tags = [
            "a","b","i","p","s","h1","h2","h3","h4","h5","code","del","div","dd","dl","dt","em","font","iframe","pre","small","span","strong","sub","table","td","th","tr",
        ]
        for i in html_tags:
            rss_str = re.sub(rf'<{i} .+?"/?>', "", rss_str)
            rss_str = re.sub(rf"</?{i}>", "", rss_str)

        rss_str = re.sub('<br .+?"/>|<(br|hr) ?/?>', "\n", rss_str)
        rss_str = re.sub(r"</?h\d>", "\n", rss_str)

        # remov video and img
        rss_str = re.sub(r'<video .+?"?/>|</video>|<img.+?>', "", rss_str)

        # remove \n 
        while re.search("\n\n", rss_str):
            rss_str = re.sub("\n\n", "\n", rss_str)
        rss_str = rss_str.strip()

        return rss_str

    def get_description(self, raw_description):
        description = self.handle_html_tag(raw_description)
        return description

class FetchRssFeedParserThread(QThread):
    fetch_result = QtCore.pyqtSignal(dict, str)

    def __init__(self, feedlink, index):
        QThread.__init__(self)
        self.feedlink = feedlink
        self.index = index

    def get_rss_result(self):
        try:
            rss = RssFeedParser(self.feedlink, self.index).feed_info
            return rss
        except AttributeError:
            return {}

    def run(self):
        new_rss = self.get_rss_result()
        self.fetch_result.emit(new_rss, self.feedlink)

class KeepRefreshRss(QThread):
    fetch_result = QtCore.pyqtSignal(list, int, int, int)

    def __init__(self, feedlink_json, rsshub_json, refresh_time):
        QThread.__init__(self)
        self.feedlink_json = feedlink_json
        self.rsshub_json = rsshub_json
        self.refresh_time = refresh_time
        self.mainItem = SaveLoadFeeds(self.feedlink_json, self.rsshub_json)

    def get_rss(self, feedlink, index):
        try:
            rss = RssFeedParser(feedlink, index).feed_info
            return rss
        except AttributeError:
            return {}

    def compare(self, old, new):
        count = 0
        total = len(old)
        old_map = {}
        for item in old:
            old_map[item['title']] = 1
        for item in new:
            if item['title'] in old_map:
                count += 1
        if count == 0:
            return 0
        return total - count

    def keep_read_status(self, old, new):
        old_rss_map = {}
        for item in old:
            title = item['title']
            status = item['isRead']
            old_rss_map[title] = status

        for item in new:
            new_title = item["title"]
            new_index = item["index"]
            if new_title in old_rss_map:
                new[new_index]['isRead'] = old_rss_map[new_title]
        return new

    def run(self):
        while (1):
            self.mainItem.fetch_feedlink_list()
            link_list = self.mainItem.feedlink_list
            pointer = 0
            self.fetch_result.emit(['refresh_start'], -1, -1, pointer)
            for index, link in enumerate(link_list):
                pointer = 0
                new_rss = self.get_rss(link, index)
                if new_rss == {}:
                    self.fetch_result.emit(['AttributeError'], index, 0, pointer)
                    continue
                new_rss = new_rss['feed_article_list']
                # rsshub_list may be changed when refresh
                self.mainItem.fetch_rsshub_list()

                old_rss = self.mainItem.rsshub_list[index]['feed_article_list']
                diff = self.compare(old_rss, new_rss)
                if diff == 0:           
                    continue
                new_rss = self.keep_read_status(old_rss, new_rss)
                self.fetch_result.emit(new_rss, index, diff, pointer)

            pointer = 1
            self.fetch_result.emit([], -1, -1, pointer)
            time.sleep(self.refresh_time)
            
            pointer = 0
            self.fetch_result.emit(['refresh_start'], -1, -1, pointer)
            self.mainItem.fetch_feedlink_list()
            link_list = self.mainItem.feedlink_list
            