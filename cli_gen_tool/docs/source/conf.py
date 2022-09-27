import os
import sys

# pathing
os.chdir('../..')
tool_root_path = os.path.abspath(os.curdir)
tool_path = tool_root_path + "\\cli_gen_tool.py"
res_path = tool_root_path + "\\res"
modules_path = res_path + "\\modules"
cli_modules_path = modules_path + "\\cli"
uic_path = res_path + "\\uic"
sys.path.insert(0,tool_root_path)
sys.path.append(tool_path)
sys.path.append(res_path)
sys.path.append(modules_path)
sys.path.append(cli_modules_path)
sys.path.append(uic_path)

print("tool root path : \n" + tool_root_path)
print("sys.path: ")
for item in sys.path:
    print(item)
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cli_gen_tool'
copyright = '2022, Douglas Quigg (dstroy0@gmail.com)'
author = 'Douglas Quigg (dstroy0@gmail.com)'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
