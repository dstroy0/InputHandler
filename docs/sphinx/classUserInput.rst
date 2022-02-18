UserInput class
~~~~~~~~~~~~~~~~

.. cpp:class:: UserInput

    .. doxygenfunction:: UserInput::UserInput(char*,uint16_t*,uint16_t,const char*,const char*,const char*,const char*)

Basic API
============
.. doxygenfunction:: UserInput::NextArgument

.. doxygenfunction:: UserInput::AddUserCommand(UserCallbackFunctionParameters *command)

.. doxygenfunction:: UserInput::GetCommandFromStream(Stream&,uint16_t,const char*)

.. doxygenfunction:: UserInput::ListUserCommands

.. doxygenfunction:: UserInput::SetDefaultHandler(void(*function)(UserInput*))

.. doxygenfunction:: UserInput::OutputIsAvailable

Advanced API
=============

.. doxygenfunction:: UserInput::ReadCommand(uint8_t*,size_t)

Configuration API
==================

.. doxygenfunction:: UserInput::ListUserInputSettings(UserInput *inputprocess)

Protected API
==============

These are the members and functions made available to derivatives that inherit from the UserInput class.

.. doxygenfunction:: UserInput::getToken(char*,uint8_t*,size_t,uint16_t*)
