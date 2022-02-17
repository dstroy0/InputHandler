UserInput class
~~~~~~~~~~

.. cpp:class:: UserInput

    .. doxygenfunction:: UserInput::UserInput(char*,uint16_t*,uint16_t,const char*,const char*,const char*,const char*)

Basic API
============

.. doxygenfunction:: UserInput::GetCommandFromStream

Advanced API
============

.. doxygenvariable:: UserInput::ReadCommand

Configuration API
==================

.. doxygenvariable:: UserInput::ListUserInputSettings

Protected API
==============

These are the members and functions made available to derivatives that inherit from the UserInput class.

.. doxygenfunction:: UserInput::getToken
