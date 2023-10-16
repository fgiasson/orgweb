(require 'package)

(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package)
  (eval-when-compile
    (unless (bound-and-true-p package--initialized)
      (package-initialize))  ;; be sure load-path includes package directories
    (require 'use-package)))

(use-package dockerfile-mode)
(use-package yaml-mode)
(use-package terraform-mode)
(use-package org)

(setq make-backup-files nil) 

; python-mode specific settings
(setq python-indent-guess-indent-offset t) 
(setq python-indent-guess-indent-offset-verbose nil)