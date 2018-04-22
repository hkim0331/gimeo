#!/bin/sh
# -*- mode: Shell-script; coding: utf-8; -*-
# update 2017-03-19.

if [ $# -ne 1 ]; then
    echo usage: $0 VERSION
    exit
else
    VERSION=$1
fi

TODAY=`date +%F`

# linux's sed is gnu sed, macos not.
if [ -e /usr/local/bin/gsed ]; then
    SED=/usr/local/bin/gsed
else
    SED=`which sed`
fi
if [ -z ${SED} ]; then
    echo can not find SED
    exit
fi

for i in "cgi/gimeo.cgi cgi/gimeo-del.cgi"; do
    ${SED} -i.bak "s/^hkimura,.*$/hkimura, ${VERSION}, ${TODAY}./" $i
done

# example of sed 'c' command.
#${SED} -i.bak "/(defvar \*version\*/ c\
#(defvar *version* \"${VERSION}\")" *.lisp

echo ${VERSION} > VERSION
