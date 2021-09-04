;;; eaf-vue-demo.el --- Vue demo

;; Filename: eaf-vue-demo.el
;; Description: Vue demo
;; Author: Andy Stewart <lazycat.manatee@gmail.com>
;; Maintainer: Andy Stewart <lazycat.manatee@gmail.com>
;; Copyright (C) 2021, Andy Stewart, all rights reserved.
;; Created: 2021-08-01 10:30:42
;; Version: 0.1
;; Last-Updated: 2021-08-01 10:30:42
;;           By: Andy Stewart
;; URL: http://www.emacswiki.org/emacs/download/eaf-vue-demo.el
;; Keywords:
;; Compatibility: GNU Emacs 28.0.50
;;
;; Features that might be required by this library:
;;
;;
;;

;;; This file is NOT part of GNU Emacs

;;; License
;;
;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 3, or (at your option)
;; any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program; see the file COPYING.  If not, write to
;; the Free Software Foundation, Inc., 51 Franklin Street, Fifth
;; Floor, Boston, MA 02110-1301, USA.

;;; Commentary:
;;
;; Vue demo
;;

;;; Installation:
;;
;; Put eaf-vue-demo.el to your load-path.
;; The load-path is usually ~/elisp/.
;; It's set in your ~/.emacs like this:
;; (add-to-list 'load-path (expand-file-name "~/elisp"))
;;
;; And the following to your ~/.emacs startup file.
;;
;; (require 'eaf-vue-demo)
;;
;; No need more.

;;; Customize:
;;
;;
;;
;; All of the above can customize by:
;;      M-x customize-group RET eaf-vue-demo RET
;;

;;; Change log:
;;
;; 2021/08/01
;;      * First released.
;;

;;; Acknowledgements:
;;
;;
;;

;;; TODO
;;
;;
;;

;;; Require


;;; Code:

(defcustom eaf-rss-reader-keybinding
  '(("M-p" . "add_subscription")
    ("C-p" . "js_scroll_up")
    ("C-n" . "js_scroll_down")
    ("a" . "add_feed")
    ("r" . "remove_feed")
    ("C-r" . "mark_as_read")
    ("C-u" . "mark_as_un_read")
    ("b" . "goback")
    )
  "The keybinding of EAF RSS Reader."
  :type 'cons)

;;;###autoload
(defun eaf-open-rss-reader ()
  "Open EAF Rss Reader"
  (interactive)
  (eaf-open "eaf-rss-reader" "rss-reader"))

(add-to-list 'eaf-app-binding-alist '("rss-reader" . eaf-rss-reader-keybinding))

(setq eaf-rss-reader-module-path (concat (file-name-directory load-file-name) "buffer.py"))
(add-to-list 'eaf-app-module-path-alist '("rss-reader" . eaf-rss-reader-module-path))

(provide 'eaf-rss-reader)

;;; eaf-vue-demo.el ends here
