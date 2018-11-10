# memechain-gui
MemeChain GUI https://kekcoin.co/memechain

This is the development repository for the Memechain GUI. THIS SOFTWARE IS IN DEVELOPMENT AND SHOULD NOT BE USED IN PRODUCTION.

## Installation

This installation guide will be using Linux/Unix throughout.

### Python Dependencies

Python will need to be installed on your system. To install python-pip run

```
sudo apt install python-pip
```

Once you have python-pip installed you will need to install the python dependencies by running

```
pip install flask pypiwin32 pythonnet comtypes pywebview sightengine
```

## How to Compile the Memechain GUI

We use pyinstaller. To install this run 

```
pip install pyinstaller
```

To compile the Memechain GUI using pyinstaller run

```
pyinstaller main.py ^
    --clean ^
    --windowed --noconsole ^
    --hidden-import "clr" --name "Memechain" ^
    --icon "static/img/favicon.ico" ^
    --paths "C:\Python27" ^
    --add-data "static;./static/" ^
    --add-data "templates;./templates/" ^
    --add-data "app.py;./" ^
    --add-data "utils.py;./" ^
    --add-data "C:\Python27\Lib\site-packages\webview\lib\WebBrowserInterop.x64.dll;./" ^
    --add-data "C:\Python27\Lib\site-packages\webview\lib\WebBrowserInterop.x86.dll;./" ^
    --exclude-module "tkinter"
```

You may need to change the paths to point to your python installation.

## Social Channels

| Site | link |
|:-----------|:-----------|
| Bitcointalk | https://bitcointalk.org/index.php?topic=2026344.0 |
| Twitter | https://twitter.com/KekcoinCore |
| Reddit | http://www.reddit.com/r/KekcoinOfficial |
| Telegram | https://t.me/KekcoinOfficial |
