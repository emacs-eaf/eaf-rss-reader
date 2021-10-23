
(defcustom eaf-rss-reader-keybinding
  '(("A" . "add_feed")
    ("R" . "remove_feed")
    ("g" . "refresh_feed")
    ("n" . "js_select_next_feed")
    ("p" . "js_select_prev_feed")
    ("j" . "js_select_next_article")
    ("k" . "js_select_prev_article")
    ("N" . "js_select_last_feed")
    ("P" . "js_select_first_feed")
    ("J" . "js_select_last_article")
    ("K" . "js_select_first_article")
    ("x" . "eaf-rss-reader-close-web-page")
    ("f" . "open_link")
    ("m" . "js_mark_article_as_read")
    ("M" . "js_mark_feed_as_read")
    ("C-j" . "jump_to_unread")
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

(defun eaf-rss-reader-web-page ()
  (catch 'found-rss-reader-buffer
    (eaf-for-each-eaf-buffer
     (when (and (boundp 'eaf--buffer-type)
                (string= eaf--buffer-type "eaf-rss-reader"))
       (throw 'found-rss-reader-buffer buffer)))))

(defun eaf-open-rss-link (url)
  "Open RSS link in other window."
  (interactive "M[EAF/browser] URL: ")
  (when (< (length (window-list)) 2)
    (split-window-right))
  (other-window 1)
  (let ((rss-url (eaf-wrap-url url))
        rss-web-page)
    (cond ((setq rss-web-page (eaf-rss-reader-web-page))
           (switch-to-buffer rss-web-page)
           (with-current-buffer rss-web-page
             (unless (string= eaf--buffer-url rss-url)
               (eaf-call-async "call_function_with_args" eaf--buffer-id "change_url" rss-url))))
          (t
           (eaf-open rss-url "browser")
           (setq-local eaf--buffer-type "eaf-rss-reader"))))
  (other-window -1))

(defun eaf-rss-reader-close-web-page ()
  (interactive)
  (save-excursion
    (let ((rss-web-page (eaf-rss-reader-web-page)))
      (when rss-web-page
        (switch-to-buffer rss-web-page)
        (kill-buffer-and-window)))))

(provide 'eaf-rss-reader)

;;; eaf-rss-reader.el ends here
