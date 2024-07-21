import os
import sys
import subprocess
import sqlite3
import threading
import re
import json
import pathlib
import argparse
import datetime
import time
import shutil
import argparse
import numpy as np
import platform


def command(cmd):
    print('command',cmd)
    os.system(cmd)

def build_clear():
    pass

def build_abi(input,output,abi,ndk,platform,toolchain,make_program,ext_params):
    print('----build_abi----' , input,output,abi)
    print('----ext_params----' , ext_params)
    ext_params_str = ''
    if ext_params:
        ext_params = ext_params.split(',')
        ext_params = ['-D'+p for p in ext_params]
        ext_params_str = ' '.join(ext_params)
    print('ext_params_str',ext_params_str)

    script = 'cmake -G"Unix Makefiles"\
                    -DCMAKE_ANDROID_ARCH_ABI=%s\
                    -DCMAKE_ANDROID_NDK=%s\
                    -DCMAKE_MAKE_PROGRAM=%s\
                    -DCMAKE_TOOLCHAIN_FILE=%s\
                    -S %s\
                    -B %s\
                    %s'%(abi,ndk,make_program,toolchain,input,output,ext_params_str)
    command(script)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' , '--input', type = str , help='set src path')
    parser.add_argument('-o' , '--output', type = str , help='set output path')
    parser.add_argument('-n' , '--android_ndk', type = str ,default=os.environ.get('ANDROID_NDK'), help='set android_ndk')
    parser.add_argument('-p' , '--platform', type = str , default='22' , help='set android platform')
    parser.add_argument('-a' , '--abi',type = str, choices=['armeabi-v7a','arm64-v8a','x86','x86_64'], help='set android arch abi,armeabi-v7a arm64-v8a x86 x86_64')
    parser.add_argument('-c' , '--clear' , action="store_true" ,default=False,  help='build clear')
    parser.add_argument('-e' , '--ext_params' ,type = str , help='set cmake extend params,split with ","')
    args = parser.parse_args()
    if not args.input:
        raise RuntimeError('input path is not set!')
    if not args.output:
        raise RuntimeError('output path is not set!')
    else:
        if not os.path.exists(args.output):
            pathlib.Path(args.output).mkdir(parents=True)
        CMakeCache = '%s/CMakeCache.txt'%(args.output)
        if os.path.exists(CMakeCache):
            os.remove(CMakeCache)
        CMakeFiles = '%s/CMakeFiles'%(args.output)
        if os.path.exists(CMakeFiles):
            shutil.rmtree(CMakeFiles)
    if not args.android_ndk:
        raise RuntimeError('android_ndk is not set!')
    INPUT = args.input.replace('\\','/')
    OUTPUT = args.output.replace('\\','/')
    ANDROID_NDK = args.android_ndk.replace('\\','/')
    sysstr = platform.system()
    if (sysstr == "Windows"):
       MAKE_PROGRAM = '%s/prebuilt/windows-x86_64/bin/make.exe'%(ANDROID_NDK)
    elif (sysstr == "Linux"):
        MAKE_PROGRAM = '%s/prebuilt/linux-x86_64/bin/make'%(ANDROID_NDK)
    else:
        print ("Other System ")
    MAKE_PROGRAM = MAKE_PROGRAM.replace('\\','/')
    ANDROID_TOOLCHAIN = '%s/android.toolchain.cmake'%(sys.path[0])
    ANDROID_TOOLCHAIN = ANDROID_TOOLCHAIN.replace('\\','/')
    if args.clear:
        build_clear()
    else:
        build_abi(INPUT,OUTPUT,args.abi,ANDROID_NDK,args.platform,ANDROID_TOOLCHAIN,MAKE_PROGRAM,args.ext_params)

if __name__ == "__main__":
    main()
