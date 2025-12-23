#!/bin/bash

case "$1" in
	r)
		shift
		python3 examples/ui_and_images.py "$@"
		;;
	r2)
		shift
		python3 examples/interaction.py "$@"
		;;
	r3)
		shift
		python3 examples/one_million_points.py "$@"
		;;
	r4)
		shift
		python3 examples/minimal.py "$@"
		;;
	*)
		echo "invalid option for run.sh"
		;;
esac
