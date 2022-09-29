import os
import sys

# pathing
os.chdir("../..")
lib_root_path = os.path.abspath(os.curdir)

_html_static_path = lib_root_path + "/docs/source/static"
sys.path.insert(0, lib_root_path)
#sys.path.append(tool_path)

sys.path.append(_html_static_path)

print("lib root path: \n" + lib_root_path)

print("If you don't see the file path here, Sphinx wont know about it and will yell at you.")
print("sys.path: ")
for item in sys.path:
    print(item)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "InputHandler"
copyright = "2022, Douglas Quigg (dquigg123@gmail.com)"
author = "Douglas Quigg (dstroy0 dquigg123@gmail.com), Brenden Doherty (2bndy5 2bndy5@gmail.com)"

breathe_projects = {
    "InputHandler": "../doxyxml/"
}
breathe_default_project = "InputHandler"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.imgmath","spinx.ext.todo","sphinx.ext.autodoc", "sphinx.ext.viewcode", "breathe"]

templates_path = ["templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["static"]
