### EAF RSS Reader

<p align="center">
  <img width="800" src="./img/screenshot.png">
</p>

RSS Reader application for the [Emacs Application Framework](https://github.com/emacs-eaf/emacs-application-framework).

### Load application

[Install EAF](https://github.com/emacs-eaf/emacs-application-framework#install) first, then add below code in your emacs config:

```Elisp
(add-to-list 'load-path "~/.emacs.d/site-lisp/emacs-application-framework/")
(require 'eaf)
(require 'eaf-rss-reader)
```

### The keybinding of EAF RSS Reader.

| Key   | Event   |
| :---- | :------ |
| `A` | add_feed |
| `R` | remove_feed |
| `g` | refresh_feed |
| `i` | import_opml |
| `o` | export_opml |
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
| `-` | zoom_out |
| `=` | zoom_in |
| `x` | eaf-rss-reader-close-page-or-quit |
| `q` | eaf-rss-reader-close-page-or-quit |
| `,` | eaf-rss-reader-scroll-up-web-page |
| `.` | eaf-rss-reader-scroll-down-web-page |
| `r` | eaf-rss-reader-refresh-web-page |
| `;` | eaf-rss-reader-immersive-translation-web-page |
| `'` | eaf-rss-reader-translate-web-page |
| `u` | jump_to_unread |
| `C-j` | jump_to_unread |
| `f` | open_link |
| `<f12>` | open_devtools |

