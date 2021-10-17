## Datasheet Viewer

> A replacement of the [Datasheet Viewer](https://github.com/Daxxn/DatasheetViewer) C# application on Windows. Its hands down, one of the most usefull apps I've ever built and i needed to replace it. The PDF viewer isnt built into the app this time, it just wasnt worth it. The Fedora default document viewer (Evince) is good enough. It can be replaced in the settings if needed.

Theres some other usefull features for the linux version that was more dificult on windows. Such as:

- Multiple datasheets open at the same time.
- A much cleaner UI.
- No need to worry about the PDF viewer.

### Installation:

> I still dont know how to create an executable for a python/QT application however, Python is built into linux and if you need to look at datasheets so often that this app would be useful, python would be a good thing to install.

### Fork and Run:

1. Fork the project, pretty standard.
1. `pip install PySide6`
1. Go to the directory in the terminal.
1. Run `python ./main.py`

(TODO - Need to create a setup script or something to configure settings.)