#INSTALL ALL DEPENDENCIES
install:
	sudo apt-get install python3.6 python3-pip moreutils python3-kivy figlet
	sudo pip3 install -r requirements.txt

#EXECUTE THE APPLICATION
run:
	sudo python3 main.py

#EXECUTE ALL TESTS
tests:
	cd test/ && python3 test.py
