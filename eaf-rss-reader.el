
(defcustom eaf-rss-reader-keybinding
  '(("A" . "add_feed")
    ("R" . "remove_feed")
    ("g" . "handle_refresh_rsshub_list")
    ("n" . "js_select_next_feed")
    ("p" . "js_select_prev_feed")
    ("j" . "js_select_next_article")
    ("k" . "js_select_prev_article")
    ("N" . "js_select_last_feed")
    ("P" . "js_select_first_feed")
    ("J" . "js_select_last_article")
    ("K" . "js_select_first_article")
    ("<f12>" . "open_devtools")
    )
  "The keybinding of EAF RSS Reader."
  :type 'cons)

;;;###autoload
(add-to-list 'eaf-app-binding-alist '("rss-reader" . eaf-rss-reader-keybinding))

(setq eaf-rss-reader-module-path (concat (file-name-directory load-file-name) "buffer.py"))
(add-to-list 'eaf-app-module-path-alist '("rss-reader" . eaf-rss-reader-module-path))

(defvar eaf-rss-reader-last-url ""
  "Record last url of rss reader open.")

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
  (let ((rss-url (eaf-wrap-url url)))
    (cond ((catch 'found-eaf
             (eaf-for-each-eaf-buffer
              (when (and (string= eaf--buffer-url eaf-rss-reader-last-url)
                         (string= eaf--buffer-app-name "browser"))
                (switch-to-buffer buffer)
                (unless (string= eaf-rss-reader-last-url rss-url)
                  (setq-local eaf--buffer-url rss-url)
                  (eaf-call-async "call_function_with_args" eaf--buffer-id "change_url" rss-url))
                (throw 'found-eaf t)))))
          (t
           (eaf-open rss-url "browser")))
    (setq eaf-rss-reader-last-url rss-url))
  (other-window -1))

(provide 'eaf-rss-reader)

;;; eaf-rss-reader.el ends here
