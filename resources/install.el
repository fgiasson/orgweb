(require 'package) 

(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)

(package-initialize) 
(package-refresh-contents)

(package-install 'use-package)
(package-install 'yaml-mode)
(package-install 'dockerfile-mode)
(package-install 'terraform-mode)