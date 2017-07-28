#!/bin/bash
if [[ -z "$@" ]]; then
	echo "add.sh <title>"
	exit 1
fi
title="$@"
filename="$(echo $@ | tr ' ' '_' | tr '[:upper:]' '[:lower:]')"
if [[ -e $filename.md ]]; then
	echo "$filename.md already exists"
	exit 1
fi
echo "Title: $title" >> $filename.md
echo "Date: $(date -Iminutes)" >> $filename.md
echo "Author: Wxcafé" >> $filename.md
echo "Category: " >> $filename.md
echo "Slug: $filename" >> $filename.md
echo -e '\n'>> $filename.md
vim +7 $filename.md -s <( echo -n A)
