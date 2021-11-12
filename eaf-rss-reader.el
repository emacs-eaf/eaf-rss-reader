;;; Code:

(defcustom eaf-rss-reader-refresh-time "600"
  "The default feed refresh time."
  :type 'int)

(defcustom eaf-rss-reader-keybinding
  '(("A" . "add_feed")
    ("R" . "remove_feed")
    ("g" . "refresh_feed")
    ("i" . "import_opml")
    ("o" . "export_opml")
    ("n" . "js_select_next_feed")
    ("p" . "js_select_prev_feed")
    ("j" . "js_select_next_article")
    ("k" . "js_select_prev_article")
    ("m" . "js_mark_article_as_read")
    ("M" . "js_mark_feed_as_read")
    ("N" . "js_select_last_feed")
    ("P" . "js_select_first_feed")
    ("J" . "js_select_last_article")
    ("K" . "js_select_first_article")
    ("-" . "zoom_out")
    ("=" . "zoom_in")
    ("x" . "eaf-rss-reader-close-page-or-quit")
    ("," . "eaf-rss-reader-scroll-up-web-page")
    ("." . "eaf-rss-reader-scroll-down-web-page")
    ("r" . "eaf-rss-reader-refresh-web-page")
    ("u" . "jump_to_unread")
    ("C-j" . "jump_to_unread")
    ("f" . "open_link")
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
  ;; Try split window to open web pag.
  (when (< (length (cl-remove-if #'window-dedicated-p (window-list))) 2) ;we need remove dedicated window, such as sort-tab window
    (split-window-right))
  (other-window 1)

  ;; Open web page.
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

  ;; Switch back to rss reader buffer.
  (other-window -1))

(defun eaf-rss-reader-close-page-or-quit ()
  (interactive)
  (save-excursion
    (let ((rss-web-page (eaf-rss-reader-web-page)))
      (if rss-web-page
          (progn
            (switch-to-buffer rss-web-page)
            (kill-buffer-and-window))
        (eaf-call-async "execute_function" eaf--buffer-id "insert_or_close_buffer" (key-description (this-command-keys-vector)))))))

(defun eaf-rss-reader-run-in-web-page (command)
  (let ((rss-web-page (eaf-rss-reader-web-page)))
    (when rss-web-page
      (with-current-buffer rss-web-page
        (eaf-call-async "execute_function" eaf--buffer-id command (key-description (this-command-keys-vector)))))))

(defun eaf-rss-reader-scroll-up-web-page ()
  (interactive)
  (eaf-rss-reader-run-in-web-page "scroll_up"))

(defun eaf-rss-reader-scroll-down-web-page ()
  (interactive)
  (eaf-rss-reader-run-in-web-page "scroll_down"))

(defun eaf-rss-reader-refresh-web-page ()
  (interactive)
  (eaf-rss-reader-run-in-web-page "refresh_page"))

(provide 'eaf-rss-reader)

;;; eaf-rss-reader.el ends here
