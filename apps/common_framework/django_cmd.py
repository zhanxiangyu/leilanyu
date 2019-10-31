# -*- coding: utf-8 -*-
import os
import subprocess
import sys


def django_dumpdata(args):
    return django_manage('dumpdata', args, True)


def django_loaddata(path):
    return django_manage('loaddata', arg=path)


def django_flush():
    return django_manage('flush', '--no-input')


def django_manage(cmd, arg=None, str_cmd=False):
    if not str_cmd:
        if arg:
            args = [sys.executable, 'manage.py', cmd, arg]
        else:
            args = [sys.executable, 'manage.py', cmd]
        process = subprocess.Popen(args, env=os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        if arg:
            args = sys.executable + ' manage.py ' + cmd + arg
        else:
            args = sys.executable + ' manage.py ' + cmd
        process = subprocess.Popen(args, env=os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True)

    output, error = process.communicate()

    return process.returncode, output, error
