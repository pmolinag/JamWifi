#INSTALL ALL DEPENDENCIES
install:
	sudo apt-get install python3.6.7 python3-pip moreutils python3-kivy
	sudo pip3 install -r requirements.txt

#EXECUTE THE APPLICATION
exe:
	sudo python3 jammer.py

#EXECUTE ALL TESTS
tests:
	cd test/ && python3 test.py

