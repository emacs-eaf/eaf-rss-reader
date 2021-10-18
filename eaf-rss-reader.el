
(defcustom eaf-rss-reader-keybinding
  '(("A" . "add_feed")
    ("*" . "add_feed")
    ("R" . "remove_feed")
    ("x" . "remove_feed")
    ("r" . "alter_read_status")
    ("u" . "alter_read_status")
    ("g" . "handle_refresh_rsshub_list")
    ("b" . "js_goback")
    ("k" . "js_select_prev_item")
    ("j" . "js_select_next_item")
    ("C-k" . "js_open_current_item")
    ("C-j" . "js_up_item")
    ("h". "js_up_item")
    ("l" . "js_open_current_item")
    ("i" . "js_open_current_item")
    ("<down>" . "js_select_next_item")
    ("<up>" . "js_select_prev_item")
    ("<right>" . "js_open_current_item")
    ("<left>". "js_up_item")
    ("C-m" . "js_open_current_item")
    ("C-n" . "js_select_next_item")
    ("C-p" . "js_select_prev_item")
    ("<" . "select_prev_view_key")
    (">". "select_next_view_key")
    ("F" . "select_prev_view_key")
    ("H". "select_next_view_key")
    ("<f12>" . "open_devtools")
    )
  "The keybinding of EAF RSS Reader."
  :type 'cons)

;;;###autoload
(add-to-list 'eaf-app-binding-alist '("rss-reader" . eaf-rss-reader-keybinding))

(setq eaf-rss-reader-module-path (concat (file-name-directory load-file-name) "buffer.py"))
(add-to-list 'eaf-app-module-path-alist '("rss-reader" . eaf-rss-reader-module-path))

(defun eaf-open-rss-reader ()
  "Open EAF Rss Reader"
  (interactive)
  (eaf-open "eaf-rss-reader" "rss-reader"))

(defun eaf-open-rss-link (url)
  "Open RSS link in other window."
  (interactive "M[EAF/browser] URL: ")
  (when (< (length (window-list)) 2)
    (split-window-right))
  (other-window 1)
  (eaf-open (eaf-wrap-url url) "browser")
  (other-window -1))

(provide 'eaf-rss-reader)

;;; eaf-rss-reader.el ends here
