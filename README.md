# wukong

This project is an improved version based on the original demo provided by wzpan. It provides an educational development environment for wukong-robot.

It draws inspiration from Docker and [musistudio/wukong-robot-install-script](https://github.com/musistudio/wukong-robot-install-script), but removes the wukong-robot core. If you want to install wukong-robot itself, please use that tool instead.

## Supported Systems

This script has been tested on the following platforms:

* Ubuntu 16.04
* Mac OS X
* WSL on Windows 10 (Windows Subsystem for Linux)

## Install Development Environment

``` bash
git clone https://github.com/tchangtc/tc_wukong.git
cd wukong-starter
./install.sh
```

During installation, you may be prompted for your sudo password when installing tools. Also, homebrew installation requires pressing Enter to confirm — just follow the prompts.

If you encounter issues, please submit feedback on the [issue page](https://github.com/wzpan/wukong-starter/issues).

## Start Development Environment

``` bash
source start.sh
```

After that, you can start developing in this environment. On first launch, install `pyaudio` as well:

``` bash
pip3 install pyaudio
```

## Linux User Notes

If Linux users encounter this error:

```
swig: error while loading shared libraries: libpcre.so.1: cannot open shared object file: No such file or directory
```

Refer to [this article](https://www.jianshu.com/p/3dbad433783f) and create a symlink to resolve it.

## Mac User Notes

If brew fails to install software, try using Tsinghua University's [Homebrew mirror](https://mirror.tuna.tsinghua.edu.cn/help/homebrew/) and [Homebrew bottles mirror](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew-bottles/).

## Windows User Notes

It is recommended to use a virtual machine with Ubuntu for development and learning. If you go this route, refer to the [Linux User Notes](#linux-user-notes) above. The instructions below are only for Windows + WSL users.

Before running this script, you need to start the pulseaudio-server first.

Download and extract [pulseaudio.zip](http://hahack-1253537070.file.myqcloud.com/misc/pulseaudio.zip) and run pulseaudio.exe from the bin directory in CMD.
