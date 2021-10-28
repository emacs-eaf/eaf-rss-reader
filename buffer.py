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
from PyQt5.QtGui import QColor
from pyquery import PyQuery as Pq
from core.webengine import BrowserBuffer
from html import unescape as html_unescape
from core.utils import eval_in_emacs, PostGui, get_emacs_vars, interactive, message_to_emacs, get_emacs_func_result, get_emacs_config_dir, touch, get_emacs_var


def count_new_rss(old_rss, new_rss):
    count = 0
    total = len(old_rss)
    old_rss_map = {}
    for item in old_rss:
        old_rss_map[item['title']] = True
    for item in new_rss:
        if item['title'] not in old_rss_map:
            count += 1
    return count

def keep_read_status(old_rss, new_rss):
    old_rss_map = {}
    for item in old_rss:
        old_rss_map[item['title']] = item['isRead']
    for item in new_rss:
        if item["title"] in old_rss_map:
            new_rss[item["index"]]['isRead'] = old_rss_map[item["title"]]
    return new_rss

class AppBuffer(BrowserBuffer):
    def __init__(self, buffer_id, url, arguments):
        BrowserBuffer.__init__(self, buffer_id, url, arguments, False)
        self.config_dir = get_emacs_config_dir()

        self.index_file_dir = os.path.join(os.path.dirname(__file__), "dist")
        self.index_file = os.path.join(self.index_file_dir, "index.html")

        self.rsshub_json = os.path.join(self.config_dir, "rss-reader", "list.json")
        self.feedlink_json = os.path.join(self.config_dir, "rss-reader", "link.json")

        # Make sure rss reader config directory is created.
        touch(self.rsshub_json)
        touch(self.feedlink_json)

        self.url = url
        self.refresh_time = int(get_emacs_var("eaf-rss-reader-refresh-time"))
        self.current_feed_index = -1
        self.current_article_index = -1
        self.add_feedlink_threads = []
        self.refresh_feedlink_threads = []
        self.keep_refresh_rss_threads = []

        self.main_item = SaveLoadFeeds(self.feedlink_json, self.rsshub_json)

        self.keep_refresh_rss(self.refresh_time)

        self.load_index_html(__file__)

    def init_app(self):
        self.init_var()
        self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.main_item.rsshub_list)))

    def init_var(self):
        if self.theme_mode == "dark":
            if self.theme_foreground_color == "#000000":
                select_color = "#333333"
                foreground_color = "#AAAAAA"
                read_color = QColor(foreground_color).darker(150).name()
                line_color = QColor(foreground_color).darker(250).name()
            else:
                select_color = QColor(self.theme_background_color).darker(150).name()
                foreground_color = QColor(self.theme_foreground_color).name()
                read_color = QColor(self.theme_foreground_color).darker(150).name()
                line_color = QColor(self.theme_foreground_color).darker(250).name()
        else:
            if self.theme_background_color == "#FFFFFF":
                select_color = "#EEEEEE"
                foreground_color = "#333333"
                read_color = QColor(foreground_color).lighter(150).name()
                line_color = QColor(foreground_color).darker(250).name()
            else:
                select_color = QColor(self.theme_background_color).darker(120).name()
                foreground_color = QColor(self.theme_foreground_color).name()
                read_color = QColor(self.theme_background_color).darker(200).name()
                line_color = QColor(self.theme_background_color).darker(200).name()

        self.buffer_widget.eval_js('''initFeedsListColor(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")'''.format(
            self.theme_background_color,
            foreground_color,
            select_color,
            read_color,
            line_color
        ))

        self.buffer_widget.eval_js('''initArticlesListColor(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")'''.format(
            self.theme_background_color,
            foreground_color,
            select_color,
            read_color,
            line_color
        ))

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
        self.add_feedlink_thread(new_feedlink, self.main_item.last_feed_index + 1)

    @QtCore.pyqtSlot(int)
    def update_current_feed_index(self, new_feed_index):
        self.current_feed_index = new_feed_index

    @QtCore.pyqtSlot(int)
    def update_current_article_index(self, new_article_index):
        self.current_article_index = new_article_index

    def refresh_feed(self):
        thread = FetchRssFeedParserThread(self.main_item.rsshub_list[self.current_feed_index]['feed_link'], self.current_feed_index)
        thread.fetch_result.connect(self.refresh_feedlink_widget)
        self.refresh_feedlink_threads.append(thread)
        thread.start()

    # call remove from emacs
    def handle_remove_feed(self):
        feed_count = len(self.main_item.feedlink_list)

        if feed_count == 1:
            self.buffer_widget.eval_js('''changeCurrentFeedByIndex({});'''.format(json.dumps(-1)))
            self.buffer_widget.eval_js('''changeCurrentArticleByIndex({});'''.format(json.dumps(-1)))
        # select last feed
        elif feed_count - 1 == self.current_feed_index:
            self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(self.current_feed_index - 1)))
            self.buffer_widget.eval_js('''selectArticleByIndex({});'''.format(json.dumps(0)))
        # select next feed
        else:
            self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(self.current_feed_index)))
            self.buffer_widget.eval_js('''selectArticleByIndex({});'''.format(json.dumps(0)))

        # remove feed in list.json and link.json
        if self.main_item.remove_feedlink_widget(self.current_feed_index):
            self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.main_item.rsshub_list)))
            message_to_emacs("Feed: \"{}\" \"{}\", index:\"{}\", has been removed".format(
                self.main_item.rsshub_list[self.current_feed_index]['feed_title'],
                self.main_item.rsshub_list[self.current_feed_index]['feed_link'],
                self.current_feed_index))
        else:
            # Failed to remove feed, turn back to prev feed and prev article.
            self.buffer_widget.eval_js('''changeCurrentFeedByIndex({});'''.format(json.dumps(self.current_feed_index)))
            self.buffer_widget.eval_js('''changeCurrentArticleByIndex({});'''.format(json.dumps(self.current_article_index)))
            message_to_emacs("Failed to remove link, please check you current Feed-Index {}.".format(feedlink_index))

    def jump_to_unread(self):
        index = self.current_article_index
        if self.current_feed_index != -1:
            for item in self.main_item.rsshub_list[self.current_feed_index]['feed_article_list']:
                if not item['isRead']:
                    index = item['index']
                    self.buffer_widget.eval_js('''selectArticleByIndex({});'''.format(json.dumps(index)))
                    return

    @interactive
    def add_feed(self):
        self.send_input_message("Add new feed: ", "add_feed")

    @interactive
    def remove_feed(self):
        ''' Remove current selected feed.'''
        self.send_input_message("Are you sure you want to remove this feed?", "remove_feed", "yes-or-no")

    @PostGui()
    def auto_refresh_rsshub_list(self, article_list, index, diff, is_refresh_finished):
        # all update finished
        if is_refresh_finished:
            message_to_emacs("All updates have been completed.")
        # updating
        elif article_list == ['refresh_start'] and not is_refresh_finished:
            message_to_emacs("Updating. It is recommended not to add or delete feeds.")
        # get error when fetch feed
        elif article_list == ['AttributeError']:
            link = self.main_item.feedlink_list[index]
            message_to_emacs("Failed to refresh link '{}', maybe you refresh too frequently.".format(link))
        # updated one feed
        else:
            title = self.main_item.rsshub_list[index]['feed_title']
            message_to_emacs("The content of '{}' is up-to-date and {} articles have been updated.".format(title, diff))
            self.main_item.rsshub_list[index]['feed_article_list'] = article_list
            self.main_item.save_rsshub_json()
            self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.main_item.rsshub_list)))

    @PostGui()
    def add_feedlink_widget(self, new_rss, new_feedlink):
        if new_feedlink in self.main_item.feedlink_list:
            message_to_emacs("Feedlink '{}' exists.".format(new_feedlink))
        else:
            if self.main_item.add_feedlink_widget(new_rss):
                self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.main_item.rsshub_list)))
                self.buffer_widget.eval_js('''selectFeedByIndex({});'''.format(json.dumps(len(self.main_item.feedlink_list)-1)))
                self.buffer_widget.eval_js('''selectArticleByIndex({});'''.format(json.dumps(0)))
                message_to_emacs("Successfully add new feedlink '{}'.".format(new_feedlink))
            else:
                message_to_emacs("Failed to add feed, please check your link {}.".format(new_feedlink))

    @PostGui()
    def refresh_feedlink_widget(self, new_rss, feedlink):
        if new_rss == {}:
            message_to_emacs("Failed to refresh link '{}', maybe you refresh too frequently.".format(feedlink_index))
        else:
            feed_index = new_rss["feed_index"]
            title = new_rss["feed_title"]
            new_rss = new_rss["feed_article_list"]
            old_rss = self.main_item.rsshub_list[feed_index]["feed_article_list"]
            count = count_new_rss(old_rss, new_rss)
            if count != 0:
                new_rss = keep_read_status(old_rss, new_rss)
                self.main_item.rsshub_list[feed_index]["feed_article_list"] = new_rss
                self.main_item.save_rsshub_json()
                self.buffer_widget.eval_js('''addFeedsListFiles({});'''.format(json.dumps(self.main_item.rsshub_list)))
                self.buffer_widget.eval_js('''changeCurrentFeedByIndex({});'''.format(json.dumps(feed_index)))
                self.buffer_widget.eval_js('''changeCurrentArticleByIndex({});'''.format(json.dumps(0)))
            message_to_emacs("The content of '{}' is up-to-date and {} articles have been updated.".format(title, count))

    @QtCore.pyqtSlot(int, int, str)
    def mark_article_as_read(self, feedlink_index, article_index, link):
        self.main_item.rsshub_list[feedlink_index]['feed_article_list'][article_index]['isRead'] = True
        self.main_item.save_rsshub_json()

        eval_in_emacs("eaf-open-rss-link", [link])

    @QtCore.pyqtSlot()
    def mark_feed_as_read(self):
        for article in self.main_item.rsshub_list[self.current_feed_index]['feed_article_list']:
            article["isRead"] = True

        self.main_item.save_rsshub_json()

    def handle_input_response(self, callback_tag, result_content):
        if callback_tag == "add_feed":
            self.handle_add_feed(result_content)
        elif callback_tag == "remove_feed":
            self.handle_remove_feed()
        else:
            BrowserBuffer.handle_input_response(self, callback_tag, result_content)

    def resize_view(self):
        (_, _, width, height) = get_emacs_func_result("eaf-get-window-size-by-buffer-id", [self.buffer_id])
        self.buffer_widget.resize(width, height)

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
        with open(self.rsshub_json, "r") as f:
            try:
                self.rsshub_list = json.load(f)
            except json.decoder.JSONDecodeError:
                pass

    def fetch_feedlink_list(self):
        with open(self.feedlink_json, 'r') as f:
            try:
                self.feedlink_list = json.load(f)
            except json.decoder.JSONDecodeError:
                pass

    def add_feedlink_widget(self, new_rss):
        new_feedlink = ''
        if new_rss == {}:
            return False
        else:
            self.last_feed_index += 1
            new_feedlink = new_rss['feed_link']

            self.feedlink_list.append(new_feedlink)
            self.save_feedlink_json()

            self.rsshub_list.append(new_rss)
            self.save_rsshub_json()

            return True

    def remove_feedlink_widget(self, feedlink_index):
        if not feedlink_index in range(0, self.last_feed_index + 1):
            return False
        else:
            self.feedlink_list.pop(feedlink_index)
            self.save_feedlink_json()

            for item in self.rsshub_list[feedlink_index::]:
                item['feed_index'] -= 1

            self.rsshub_list.pop(feedlink_index)
            self.save_rsshub_json()

            self.last_feed_index -= 1
            return True

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

            shortDescription = item.summary

            item = {
                "title" : item.title,
                "link" : item.link,
                "time" : item.published,
                "author" : author,
                "index" : article_index,
                "shortDescription" : shortDescription if len(shortDescription) <= 120 else shortDescription[: 120] + "...",
                "isRead" : False
            }
            article_list.append(item)
            article_index += 1

        return article_list

class FetchRssFeedParserThread(QThread):
    fetch_result = QtCore.pyqtSignal(dict, str)

    def __init__(self, feedlink, index):
        QThread.__init__(self)
        self.feedlink = feedlink
        self.index = index

    def get_rss_result(self):
        try:
            return RssFeedParser(self.feedlink, self.index).feed_info
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
        self.main_item = SaveLoadFeeds(self.feedlink_json, self.rsshub_json)

    def get_rss(self, feedlink, index):
        try:
            return RssFeedParser(feedlink, index).feed_info
        except AttributeError:
            return {}

    def run(self):
        while (1):
            self.main_item.fetch_feedlink_list()
            link_list = self.main_item.feedlink_list
            is_refresh_finished = False
            self.fetch_result.emit(['refresh_start'], -1, -1, is_refresh_finished)
            for index, link in enumerate(link_list):
                new_rss = self.get_rss(link, index)
                if new_rss == {}:
                    self.fetch_result.emit(['AttributeError'], index, 0, is_refresh_finished)
                    continue
                new_rss = new_rss['feed_article_list']
                # rsshub_list may be changed when refresh
                self.main_item.fetch_rsshub_list()
                old_rss = self.main_item.rsshub_list[index]['feed_article_list']
                count = count_new_rss(old_rss, new_rss)
                if count != 0:
                    new_rss = keep_read_status(old_rss, new_rss)
                    self.fetch_result.emit(new_rss, index, count, is_refresh_finished)

            is_refresh_finished = True
            self.fetch_result.emit([], -1, -1, is_refresh_finished)
            time.sleep(self.refresh_time)
