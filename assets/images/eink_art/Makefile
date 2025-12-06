.PHONY: photos

photos:
	mkdir -p photos
	for x in `ls ./original/`; do bash ../../../scripts/photo_script.sh original/$$x photos/$$x; done
