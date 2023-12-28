# Chinese Chess AI

This is the project about creating a simple Chinese Chess AI using for education purpose in module *IT3160E - Introduction to AI* of Hanoi University of Science and Technology

## Table of Contents
- [Chinese Chess AI](#chinese-chess-ai)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [How to use](#how-to-use)
    - [Python guide:](#python-guide)
    - [PyPy guide:](#pypy-guide)
  - [Details about our code](#details-about-our-code)

## Introduction



## Features



## How to use

For optimal performance, we strongly advise executing our code using the Pypy compiler. Utilizing Pypy can enhance performance by 2-3 times for each operation. It's worth noting that all results presented in our report were obtained using Pypy for measurement purposes. Nevertheless, you can still execute this code in Python with a reduced performance level. Below is a step-by-step installation guide:

### Python guide:
1. Clone the repository:
```bash
git clone https://github.com/auphong2707/chinese-chess-ai-agent.git
```
2. Navigate to the project directory:
```bash
cd chinese-chess-ai-agent
```
3. Intall required modules:
```bash
pip install -q -r requirements.txt
```
4. Run the game:
```bash
python main.py
```
### PyPy guide:
1. Clone the repository:
```bash
git clone https://github.com/auphong2707/chinese-chess-ai-agent.git
```
2. Navigate to the project directory:
```bash
cd chinese-chess-ai-agent
```
3. Prepare PyPy **(for Window user)**:
- For **Command Prompt (Powershell)**
```bash
curl -o pypy3.10-v7.3.14-win64.zip https://downloads.python.org/pypy/pypy3.10-v7.3.14-win64.zip
tar -xf pypy3.10-v7.3.14-win64.zip
ren pypy3.10-v7.3.14-win64 pypy
pypy\pypy.exe -m ensurepip
pypy\pypy.exe -m pip install pygame-ce
```
- For **Git Bash**
```bash
curl -O https://downloads.python.org/pypy/pypy3.10-v7.3.14-win64.zip
unzip pypy3.10-v7.3.14-win64.zip
mv pypy3.10-v7.3.14-win64 pypy
pypy/pypy.exe -m ensurepip
pypy/pypy.exe -m pip install pygame-ce
```
4. Run the game
- For **Command Prompt (Powershell)**
```bash
pypy\pypy.exe main.py
```
- For **Git Bash**
```bash
pypy/pypy.exe main.py
```
**Notice**: At step 3, if you are using an OS other than Window, you may need to download Pypy from [here](https://www.pypy.org/download.html), add the extracted folder to PATH. Afer that, you need to install the pygame community edition by using these commands:
```bash
pypy -m ensurepip
pypy -m pip install pygame-ce
```
Finally, you can run the game:
```bash
pypy main.py
```

## Details about our code
