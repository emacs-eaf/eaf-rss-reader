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
| `N` | js_select_last_feed |
| `P` | js_select_first_feed |
| `J` | js_select_last_article |
| `K` | js_select_first_article |
| `x` | eaf-rss-reader-close-web-page |
| `F` | open_link |
| `m` | mark_article_as_read |
| `M` | mark_feed_as_read |
| `<f12>` | open_devtools |
