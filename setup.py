#!/usr/bin/python3.4

# Using py2exe compiling program, to bundle an exe

from distutils.core import setup
import py2exe
import pygame

setup(console=["Main_Program.py"])