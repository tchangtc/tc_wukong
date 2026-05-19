#!/bin/bash

function check_and_install_python {    
    if ! command -v python3 >/dev/null; then
        echo "Preparing to install python3"
        if command -v apt-get >/dev/null; then
            sudo apt-get install -y python3
            if [[ $? -eq 0 ]]; then
                echo "python3 installed successfully"
            else
                echo "python3 installation failed"
                exit 1
            fi
        elif command -v yum >/dev/null; then
            sudo yum update
            sudo yum install -y python3
            if [[ $? -eq 0 ]]; then
                echo "python3 installed successfully"
            else
                echo "python3 installation failed"
                exit 1
            fi
        else
            echo "python3 installation failed: unsupported system type"
            exit 1
        fi
    fi
}

echo "---------- Welcome to wukong-starter one-click install script ----------"
system=$(uname -a)
os_name=(${system// / })
if [ ${os_name[0]} == "Darwin" ]
then
    read -p "Is your system macOS? [Y/n]: " confirm
    if [[ ${confirm} != "Y" && ${confirm} != "y" && ${confirm} != "" ]]
    then
        echo "Installation failed: system detection error, exiting"
        exit
    else
        python ./scripts/install.py 1
    fi
elif [[ ${os_name[0]} == "Linux" && ${os_name[2]} =~ "Microsoft" ]]
then
    read -p "Is your system Windows 10 WSL? [Y/n]:" confirm
    if [[ ${confirm} != "Y" && ${confirm} != "y" && ${confirm} != "" ]]
    then
        echo "Installation failed: system detection error, exiting"
        exit 1
    else
        check_and_install_python
        python3 ./scripts/install.py 2
    fi
elif [[ ${os_name[0]} == "Linux" && ${os_name[1]} != "raspberrypi" ]]
then
    if [[ ${confirm} != "Y" && ${confirm} != "y" && ${confirm} != "" ]]
    then
        echo "Installation failed, system detection error, exiting. Please report this to the author"
        exit 1
    else
        check_and_install_python
        python3 ./scripts/install.py 0
    fi
fi
