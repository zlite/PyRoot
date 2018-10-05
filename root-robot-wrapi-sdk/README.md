# WRAPI.v1.0.Alpha

##Installing under MacOS

### Contents
* Installing WRAPI
* Installing Node.js
* Installing Flake8 (optional but strongly recommended)
* Installing Aton and its plugins (optional but strongly recommended)
* Using WRAPI with Atom
* Tips and troubleshoting
* Installing OpenCV (optional)
* Who do I talk to?

### Installing WRAPI
* Just clone this repository into your local machine. [Here is more information about cloning](https://confluence.atlassian.com/bitbucket/clone-a-repository-223217891.html).
* WRAPI is a set of Python and Node.js files and libraries, most of them in source form. So you can move to different locations on your machine if you want. You should be able also to keep parallel working copies of WRAPI.

##### Important note
The installation notes here assume that your computer has a working Python 2.7.9 (or higher) installation.

### Installing Node.js
* Go to https://nodejs.org/, donwload and install the last Atom LTS version (v6.2.1 or superior). Just follow the package's installing instructions, but be sure to choose the **"Install for all users"** option.
* If something goes wrong with Node.js (now or later when trying to run stuff), try unistalling it completely and installing it again. Here is more information about uninstalling Node.js in MacOS: http://benznext.com/completely-uninstall-node-js-from-mac-os-x/

### Installing Flake8 (optional but strongly recommended)
Open a terminal and run the following commands:

	sudo easy_install pip
	pip install flake8
	pip install flake8-docstrings

### Installing Atom and its plugins (optional but strongly recommended)
* Go to https://atom.io/, donwload and install the last Atom version on your computer (uncompress the downloaded file, and move the uncompressed **Atom** app to the **Applications** folder).

* Close all the welcome and other windows.
* Open **Settings** (you can do it by pressing **Cmd + ,**).
* Go to "Install" (on the left list).
* Type on the search dialog "node-debugger", and  press "Install" (currently used version 1.7.0). Package website: https://atom.io/packages/node-debugger
* Quit Atom.
* Run Atom.
* Open **Settings** (you can do it by pressing **Cmd + ,**).
* Go to "Packages" (on the left list).
* Press "Settings" on "node-debugger".
* In "Node Path", type the following:

        /usr/local/bin/node

* Quit Atom.
* Run Atom.
* Open **Settings** (you can do it by pressing **Cmd + ,**).
* Go to "Install" (on the left list).
* Type on the search dialog "Script", and press "Install" (currently used version 3.8.3): Package website: https://atom.io/packages/script
* Quit Atom.
* Run Atom.
* Configure linter-flake8 plugin:
    * Set "Max Line Lengh" to 128.
* Configure language-python plugin:
    * Set "Preferred Line Lengh" to 128.
* Optionally, you can also install Atom's plugin "Python-Tools": https://atom.io/packages/python-tools
* Other useful packages are:
    * https://atom.io/packages/multi-cursor
    * https://atom.io/packages/open-recent
    * https://atom.io/packages/linter
    	* Settings: Disable: "Show Inline Error Tooltips"
    * https://atom.io/packages/linter-flake8
    	* Warning: Will not work without installing flake8 and flake8-docstrings with pip (from the command line).
    * https://atom.io/packages/highlight-selected
    * https://atom.io/packages/pigments

### Using WRAPI with Atom
##### Open the WRAPI folder in Atom
* Run Atom
* In Atom's menu: File->Add Project Folder
* In the dialog window, select WRAPI's **v1.0** folder.

##### Run the BLE server
* In Atom, if you don't see the left-panel with the list of WRAPI's files, press **ALT + \**
* In the left panel, go to the **Servers** folder and clikk on it.
* From that folder, double click the **BleSocketServer.js** file. That will open it on Atom's editor.
* Press **F5** (**Fn + F5** in most laptops). Do this a few times, until you see the message "Server is listening." in the **stdout/stderr** window.

##### Turn on the robot
* Once you turn on the robot, you will see a message similar to this one:

        peripheral discovered (8df799f0d7204f63adfafb59ab4abd25 with address <d7:f6:02:25:cf:f6, unknown>, connectable true, RSSI -64:
        Local name: NaN
        Advertised services:
        ["48c5d828ac2a442d97a30c9822b04979"]
        Serial found.
        Tx found.
        txChannel initialized.
        Rx found.

* Now you can use the mouse/trackpad to reduce the size of the **stdout/stderr** window.
* To stop the program, just press the red "x" button on the right panel of the **stdout/stderr** window.

##### Important note
In the current Alpha version, if the robot gets disconnected for some reason, the server **MUST BE REINITIALIZED**.

##### Playing with the examples
Try opening examples from the left panel. For running an openned example from the editor, just press **Ctrl + i**. Some examples to start with are:

* HelloWorld0.py
* Bumpers0.py
* BumpersCallback0.py
* Square1.py
* Fractal0.py
* LineFollower0.py
* LineFollower2.py
* MirrorMaze0.py

And if you are going to use OpenCV (see section below on how to install it), you can try some video tracking examples too:

* VideoTracking8.py

##### Important note
Don't forget to stop the example, by pressing **ESC**. Failing in doing so, or pressing **Ctrl + i** again without having stopped the running program, will lead to multiple instances of the same program running in parallel. See the **_Tips and troubleshoting_** section below for more information about this.

### Tips and troubleshoting
Atom and its plugins may be tricky. So here are some tips:

* With the current Python script pluging, it's easy to run a new version of your code (by pressing **Ctrl + i**) without having stopped a previous running instances (by pressing **ESC**). Thus, both versions of the Python program will be running in parallel, taking a lot of CPU resources, and probably bad functioning. **Workaround:** A possible solution for this is to keep the operating system's **Activity Monitor** program, filtering by name with the string "pyhon". This will show you how many Python programs are running at a given moment. You can also use the Activity Monitor to force quit an instance that you forgot to close.
* Please be aware of that while Atom is running Python code, it becomes VERY slow. **Workaround:** To continue editing, it's always a good idea to stop the running code.
* Plese note that if you run and then stop JavaScript code with Node.js a few times (let's say 5 to 10 times), it's very possible that the code will start running very slow. **Workaround:** Restart Atom.

### Installing OpenCV (optional)
Open a terminal and run the following commands. You may get some warnings, specially after the "brew install" commands; just ignore them:

    pip install numpy
    brew install cmake pkg-config
    brew install jpeg libpng libtiff openexr
    brew install eigen tbb
    cd ~
    git clone https://github.com/Itseez/opencv.git
    cd opencv
    git checkout 3.0.0
    cd ~
    git clone https://github.com/Itseez/opencv_contrib
    cd opencv_contrib
    git checkout 3.0.0
    cd ~/opencv
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D PYTHON2_PACKAGES_PATH=/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages -D PYTHON2_LIBRARY=/Library/Frameworks/Python.framework/Versions/2.7/bin/python -D PYTHON2_INCLUDE_DIR=/Library/Frameworks/Python.framework/Headers -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules ..
    make -j2
    make install
    pip install imutils

##### Verify installation
The following path may be different on your computer:

    cd /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages
    ls -l cv2.so

You should get this result:

    -rwxr-xr-x  1 user_name  admin  2021204 Aug 10 19:27 cv2.so

For more information about installing OpenCV, [click here](http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/).

### Who do I talk to?
* http://codewithroot.com/
* http://scansorial.com/

