### EAF RSS Reader

<p align="center">
  <img width="800" src="./screenshot-1.png">
</p>

<p align="center">
  <img width="800" src="./screenshot-2.png">
</p>

<p align="center">
  <img width="800" src="./screenshot-3.png">
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
| `g` | handle_refresh_rsshub_list |
| `k` | js_select_prev_item |
| `j` | js_select_next_item |
| `h` | js_up_item |
| `l` | js_open_current_item |
| `<down>` | js_select_next_item |
| `<up>` | js_select_prev_item |
| `<left>` | js_up_item |
| `<right>` | js_open_current_item |
| `C-n` | js_select_next_item |
| `C-p` | js_select_prev_item |
| `C-h` | js_up_item |
| `C-m` | js_open_current_item |
| `<f12>` | open_devtools |

