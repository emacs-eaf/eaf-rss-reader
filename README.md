### EAF RSS Reader

<p align="center">
  <img width="800" src="./img/screenshot.png">
</p>

RSS Reader application for the [Emacs Application Framework](https://github.com/emacs-eaf/emacs-application-framework).

### Load application

```Elisp
(add-to-list 'load-path "~/.emacs.d/site-lisp/eaf-rss-reader/")
(require 'eaf-rss-reader)
```

### The keybinding of EAF RSS Reader.

| Key   | Event   |
| :---- | :------ |
| `A` | add_feed |
| `R` | remove_feed |
| `g` | refresh_feed |
| `n` | js_select_next_feed |
| `p` | js_select_prev_feed |
| `j` | js_select_next_article |
| `k` | js_select_prev_article |
| `m` | js_mark_article_as_read |
| `M` | js_mark_feed_as_read |
| `N` | js_select_last_feed |
| `P` | js_select_first_feed |
| `J` | js_select_last_article |
| `K` | js_select_first_article |
| `x` | eaf-rss-reader-close-web-page |
| `,` | eaf-rss-reader-scroll-up-web-page |
| `.` | eaf-rss-reader-scroll-down-web-page |
| `r` | eaf-rss-reader-refresh-web-page |
| `u` | jump_to_unread |
| `C-j` | jump_to_unread |
| `f` | open_link |
| `<f12>` | open_devtools |
