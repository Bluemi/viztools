#!/bin/bash

case "$1" in
	r)
		shift
		python3 scripts/main.py "$@"
		;;
	r2)
		shift
		python3 scripts/main2.py "$@"
		;;
	*)
		echo "invalid option for run.sh"
		;;
esac
