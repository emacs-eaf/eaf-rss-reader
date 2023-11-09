;;; Code:

(defcustom eaf-rss-reader-split-horizontally t
  "Split web page horizontally, split web page vertically if this option set with nil."
  :type 'boolean)

(defcustom eaf-rss-reader-web-page-other-window t
  "Whether open eaf rss webpage in other window"
  :type 'boolean)

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
    ("q" . "eaf-rss-reader-close-page-or-quit")
    ("," . "eaf-rss-reader-scroll-up-web-page")
    ("." . "eaf-rss-reader-scroll-down-web-page")
    ("r" . "eaf-rss-reader-refresh-web-page")
    (";" . "eaf-rss-reader-immersive-translation-web-page")
    ("'" . "eaf-rss-reader-translate-web-page")
    ("u" . "jump_to_unread")
    ("C-j" . "jump_to_unread")
    ("f" . "open_link")
    ("<f12>" . "open_devtools")
    )
  "The keybinding of EAF RSS Reader."
  :type 'cons)

(defcustom eaf-rss-reader-phone-agent-list nil
  "Some site can't show content complete, you can add rss link in this list,
site can switch to phone style before load url."
  :type 'list)

;;;###autoload
(add-to-list 'eaf-app-binding-alist '("rss-reader" . eaf-rss-reader-keybinding))

(setq eaf-rss-reader-module-path (concat (file-name-directory load-file-name) "buffer.py"))
(add-to-list 'eaf-app-module-path-alist '("rss-reader" . eaf-rss-reader-module-path))

(defun eaf-open-rss-reader ()
  "Open EAF Rss Reader"
  (interactive)
  (eaf-open default-directory "rss-reader"))

(defun eaf-rss-reader-web-page ()
  (catch 'found-rss-reader-page
    (eaf-for-each-eaf-buffer
     (when (or (string-equal eaf--buffer-url eaf-rss-last-visit-url)
               (string-equal eaf--buffer-url (format "%s/" eaf-rss-last-visit-url)))
       (throw 'found-rss-reader-page buffer)))))

(defun eaf-rss-reader-get-buffer ()
  (catch 'found-rss-reader-buffer
    (eaf-for-each-eaf-buffer
     (when (string-equal eaf--buffer-app-name "rss-reader")
       (throw 'found-rss-reader-buffer buffer)))))

(defun eaf-rss-reader-content-page ()
  (or
   ;; If blog redirect domain, `eaf--buffer-url' is not equal `eaf-rss-last-visit-url'.
   (eaf-rss-reader-web-page)
   ;; Because some blog will redirect domain, so `eaf-rss-reader-web-page' can't works expect.
   ;; Then we need check window beside EAF RSS buffer, return it if beside buffer is EAF browser buffer.
   (let ((window-number (length (cl-remove-if #'window-dedicated-p (window-list)))))
     (when (equal window-number 2)
       (save-window-excursion
         (with-selected-window (get-buffer-window (eaf-rss-reader-get-buffer))
           (other-window 1)
           (when (and eaf--buffer-url
                      (string-equal eaf--buffer-app-name "browser"))
             (current-buffer))))))))

(defvar eaf-rss-last-visit-url nil)

(defun eaf-open-rss-link (feed-link url)
  "Open RSS link in other window."
  (interactive "M[EAF/browser] URL: ")
  ;; Try split window to open web pag.
  (delete-other-windows)
  (if eaf-rss-reader-split-horizontally
      (split-window-right)
    (split-window-below))
  (other-window 1)

  ;; Open web page.
  (let* ((rss-url (eaf-wrap-url url))
         (rss-web-page (eaf-rss-reader-web-page))
         (agent (if (member feed-link eaf-rss-reader-phone-agent-list) "phone" "pc")))
    (cond (rss-web-page
           (switch-to-buffer rss-web-page)
           (with-current-buffer rss-web-page
             (eaf-call-async "execute_function_with_args" eaf--buffer-id "load_url_with_agent" rss-url agent)))
          (t
           (eaf-open rss-url "browser" agent)))
    (setq eaf-rss-last-visit-url rss-url))

  ;; Switch back to rss reader buffer according to `eaf-rss-reader-web-page-other-window'
  (if eaf-rss-reader-web-page-other-window
      (other-window -1)
    (delete-other-windows)))

(defun eaf-rss-reader-close-page-or-quit ()
  (interactive)
  (save-excursion
    (let ((rss-web-page (eaf-rss-reader-content-page)))
      (if rss-web-page
          (progn
            (switch-to-buffer rss-web-page)
            (kill-buffer-and-window)
            (setq eaf-rss-last-visit-url nil))
        (eaf-call-async "eval_function" eaf--buffer-id "insert_or_close_buffer" (key-description (this-command-keys-vector)))))))

(defun eaf-rss-reader-run-in-web-page (command)
  (let ((rss-web-page (eaf-rss-reader-content-page)))
    (when rss-web-page
      (with-current-buffer rss-web-page
        (eaf-call-async "eval_function" eaf--buffer-id command (key-description (this-command-keys-vector)))))))

(defun eaf-rss-reader-scroll-up-web-page ()
  (interactive)
  (eaf-rss-reader-run-in-web-page "scroll_up"))

(defun eaf-rss-reader-scroll-down-web-page ()
  (interactive)
  (eaf-rss-reader-run-in-web-page "scroll_down"))

(defun eaf-rss-reader-refresh-web-page ()
  (interactive)
  (eaf-rss-reader-run-in-web-page "refresh_page"))

(defun eaf-rss-reader-translate-web-page ()
  (interactive)
  (eaf-rss-reader-run-in-web-page "translate_page")

  ;; We need select EAF RSS buffer after open translate page.
  (run-with-timer "2" nil (lambda() (select-window (get-buffer-window (eaf-rss-reader-get-buffer))))))

(defun eaf-rss-reader-immersive-translation-web-page ()
  (interactive)
  (eaf-rss-reader-run-in-web-page "immersive_translation"))

(provide 'eaf-rss-reader)

;;; eaf-rss-reader.el ends here
