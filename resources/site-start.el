(require 'package)

(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package)
  (eval-when-compile
    (unless (bound-and-true-p package--initialized)
      (package-initialize))  ;; be sure load-path includes package directories
    (require 'use-package)))

(use-package org)
(use-package dockerfile-mode)
(use-package yaml-mode)
(use-package terraform-mode)
(use-package graphviz-dot-mode)
(use-package plantuml-mode)

; configure plantuml
(setq plantuml-jar-path "/usr/bin/plantuml")
(setq org-plantuml-executable-path "/usr/bin/plantuml")
(setq plantuml-default-exec-mode 'executable)
(setq org-plantuml-exec-mode 'plantuml)


; load languages for Org major mode.
; those are used when executing a Org file
; (not when tangling nor weaving it)
(org-babel-do-load-languages
  'org-babel-load-languages
  '((emacs-lisp . t)
    (python . t)
    (dot . t)
    (plantuml . t)))

; disable backup files. They are not needed and it won't make =monitoring= going crazy
(setq make-backup-files nil) 

; python-mode specific settings
(setq python-indent-guess-indent-offset t) 
(setq python-indent-guess-indent-offset-verbose nil)