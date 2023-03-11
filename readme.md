# Development canceled
This project has been discontinued due to several technical limitations that did not generate a user-friendly product. 
A new version of this same project is under development. A link to the repository will be published soon.

# About
K-AVT is a tool for translating games through image analysis and automatic translators. It is primarily designed to translate visual novels from Japanese into English or Spanish. It is currently a proof of concept and is in alpha.

[Official website of the project](https://theerogereviewer.wordpress.com/k-avt/)

## How does it work ?

The tool is based on [Python3](https://www.python.org/) and  [Tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter).

Screenshots of the game are taken. The images are then analyzed to identify characters using various OCR tools such as [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) and [EasyOCR](https://github.com/JaidedAI/EasyOCR). The character sequences are sent to translation engines such as [DeepL](https://www.deepl.com/) and [Google](https://translate.google.com/). The translated text is displayed in the tool.

# Download Executable version and Use

You can download the latest version of the tool from:
- [Anonfiles](https://anonfiles.com/XfT3WfP8x8/kavt_rar)
- [Gofile](https://gofile.io/d/D4LVW2)


**The first time you run it, it may take a while to start. It will download some machine learning models from the internet.**

Why does antivirus give me a warning?:

This version is not officially "signed", so some antivirus may think it is malicious. If you want to continue, add the "kavt.exe" program to your antivirus exception list. 
If you are suspicious, you can always download this repository and manually run the tool with Python. The code is Open Source and you can clearly see that there is nothing wrong with it.

Why is the tool so heavy?:

The tool uses several models and machine learning tools, including [Torch](https://pytorch.org/). Unfortunately, we have not yet been able to optimize the way we compress the size of the program and Torch contributes to this weight.

Instructions for use:

1) You must select a "box" on the screen where the images are captured. To do this, first click on **Set Zone**. Then we move the cursor to the upper left corner of this "box" and with the **space key** we mark the corner. Then move the cursor to the lower right corner of this "box" and press the **space key** again. Imagine that we are marking the upper left and lower right boundary of an imaginary rectangle where the program will search for text.
2) You can use **Capture** to take a snapshot of the configured area. With "Translate" we send the text to be translated. With "Capture and Translate" we perform both actions simultaneously.
3) In the upper options bar you can change the OCR and translator used. You can also configure the language settings.
4) We recommend using DeepL as a translator. For that you must create an account [here](https://www.deepl.com/pro?cta=header-pro-button) (is free of charge) and get your API Key. Then you can enter your API Key in the Config menu. 
5) The automatic mode detects "substantial" changes on the screen and tries to generate a translation immediately. It is useful when there are dialog boxes where the text changes constantly but they are always in the same place.


# Install this repo
The installation of this repo **is not** straightforward as various AI and ML tools must be supported. That's why we offer the executable version if you just want to use the tool.

In these instructions, whenever we talk about "command", we refer to using such "command" in CMD or PowerShell of Windows.

### A) Base tools

Validate that you have Ptyhon3.9, Pip and Poetry installed on your computer. If you are missing any of those things follow these instructions:

1) Download and install Python3.9 from [here](https://www.python.org/downloads/release/python-399/).
2) Verify that you have the correct version of Python**3.9** running with this command: ```python --version```. If it doesn't work it may be a problem in the path or that you have multiple versions of python installed.
3) Verify that you have the [Pip](https://pypi.org/) Package Manager with this command: ```pip --version```
4) If you do not have Pip Package Manager installed, install it with this command: ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py``` Verify again that Pip will be installed with the previous step. 
5)  Install the [Poetry](https://python-poetry.org/) Environment Manager with this command: ```pip install --user poetry```
6) Verify that you have the Poetry Environment Manager installed with:  ```poetry --version```

### B) Secondary tools

1) You need to have "Visual CCP Build Tools" installed on your computer. This Microsoft tool is used to internally compile some packages. You can find it [here](https://visualstudio.microsoft.com/es/visual-cpp-build-tools/). Restart your computer after performing these actions.

2) **Optional recommended** If you have an **Nvidia graphics card with CUDA technology** (almost all of them do), you can make the algorithms run much faster. First verify that you have the latest video drives installed. Then install the CUDA specific drivers from [here](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local). **Download Cuda version 11**. After installing the drivers it may be necessary to reboot. You can check if your card is ready to use CUDA using this command: ```nvcc --version``` You should see a series of information displayed including "CUDA version 11".


### C) Installing the repository

1) Copy this repository with git or download it.
2) Navigate to the repository directory and use the command: ```poetry shell``` This will trigger a development environment for the project.
3) Use the command: ```poetry install``` to install the repository.
4) **Optional recommended** If you have installed the CUDA drivers, you can install the part of the repository dedicated to the use of the graphics card with: ```poe force-cuda11```

# Run

1) In the project directory use the command: ```poetry shell``` This will trigger a development environment for the project.
2) Then use the command: ```python ./kavt.py```. **The first run may be slower, since the OCR models must be downloaded** (automatic).

# Compile

Compiling the repository into an executable is difficult, so I have created a script that automates most of the operations. This script may not behave correctly on your computer and you may need to modify it.

In the repository directory use the command:  ```python compile.py``` That should execute, in an orderly fashion, all that is necessary.

If you want to see details of the operation, you should do this:
1) Run:  ```python compileA.py``` Which performs initial operations prior to compilation.
2) Run: ```poetry shell``` and ```pyinstaller --clean --specpath ./ kavt.spec``` This starts the [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/#) compiler
3) Run: ```python compileB.py``` This executes necessary operations on the compiled computer program
