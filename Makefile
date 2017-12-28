.PHONY: install
install:
	python3 setup.py install
.PHONY: clean
clean:
	rm -rf build dist *.egg-info
