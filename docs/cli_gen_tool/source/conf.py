# cli_gen_tool docs conf.py

import os
import sys

# pathing
os.chdir("../../..")
lib_root_path = os.path.abspath(os.curdir)
tool_docs_path = lib_root_path + "/docs/cli_gen_tool/source"
tool_root_path = os.path.abspath(os.curdir) + "/tools/cli_gen_tool_src"
tool_path = tool_root_path + "/cli_gen_tool.py"

modules_path = tool_root_path + "/modules"
cli_modules_path = modules_path + "/cli"
uic_path = modules_path + "/uic"
_html_static_path = lib_root_path + "/docs/cli_gen_tool/source/static"
_templates_path = lib_root_path + "/docs/cli_gen_tool/source/templates"
sys.path.insert(0, tool_docs_path)
sys.path.append(tool_root_path)
sys.path.append(tool_path)
sys.path.append(modules_path)
sys.path.append(cli_modules_path)
sys.path.append(uic_path)
sys.path.append(_html_static_path)
sys.path.append(_templates_path)

print("tool root path: \n" + tool_root_path)

print(
    "If you don't see the module path here, it will not import and Sphinx will yell at you."
)
print("sys.path: ")
for item in sys.path:
    print(item)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "cli_gen_tool"
copyright = "2022, Douglas Quigg (dstroy0@gmail.com)"
author = "Douglas Quigg (dstroy0@gmail.com)"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_mdinclude",
]

templates_path = ["templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["static"]
