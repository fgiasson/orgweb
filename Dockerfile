FROM alpine:3.18.4

# Install Bash
RUN apk add --no-cache bash=5.2.15-r5 && \
    apk add --no-cache emacs=28.2-r8 

# TODO: when the next version of Alpine will be released, uncomment that RUN command
#       in order to install the latest version of org-mode on melpa. This is only possible when
#       Emacs 29.1 will be available in Alpine since this is a new feature of Emacs 29.1
# RUN emacs --batch --eval "(progn (package-initialize) (package-refresh-contents) (setq package-install-upgrade-built-in t) (package-install 'org))"

