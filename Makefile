XARGS := xargs -0 $(shell test $$(uname) = Linux && echo -r)
GREP_T_FLAG := $(shell test $$(uname) = Linux && echo -T)

all:
	@echo "make clean - reset the project and remove auto-generated assets."
	@echo "make docs - run sphinx to create project documentation."
	@echo "make test - run the jasmine based unit tests."

clean:
	rm -rf docs/_build
	rm -rf *.mp4
	rm -rf *.log
	rm -rf .git/avatar/*
	find . \( -name '*.py[co]' -o -name dropin.cache \) -delete
	find . \( -name '*.bak' -o -name dropin.cache \) -delete
	find . \( -name '*.tgz' -o -name dropin.cache \) -delete
	find . | grep -E "(__pycache__)" | xargs rm -rf

docs: clean
	$(MAKE) -C docs html
	@echo "\nDocumentation can be found here:"
	@echo file://`pwd`/docs/_build/html/index.html
	@echo "\n"

test: clean
	jasmine ci --config tests/jasmine.yml
