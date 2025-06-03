#!/bin/bash

case "$1" in
	r)
		shift
		python3 scripts/main.py "$@"
		;;
	*)
		echo "invalid option for run.sh"
		;;
esac
