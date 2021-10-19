
(defcustom eaf-rss-reader-keybinding
  '(("A" . "add_feed")
    ("R" . "remove_feed")
    ("g" . "handle_refresh_rsshub_list")
    ("n" . "js_select_next_feed")
    ("p" . "js_select_prev_feed")
    ("j" . "js_select_next_article")
    ("k" . "js_select_prev_article")
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
