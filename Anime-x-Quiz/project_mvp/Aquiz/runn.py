#!/usr/bin/python3
"""run app"""
import os
import sys

# Append the parent directory of the current script to the Python path
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Aquiz import app

if __name__ == '__main__':
    app.run(debug=True)