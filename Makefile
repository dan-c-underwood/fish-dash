all: copy build

.PHONY: all clean

copy:
	fish ./copy.fish

build:
	python3 ./build.py

clean:
	rm -rf ./fish.docset
	rm -rf ./icon.png
	rm -rf ./logo.png

compress:
	tar --exclude='.DS_Store' -cvzf fish.tgz fish.docset
