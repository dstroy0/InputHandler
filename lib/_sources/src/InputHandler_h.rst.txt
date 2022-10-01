InputHandler.h file
=====================

typedefs
---------
.. doxygentypedef:: IH_pname

.. doxygentypedef:: IH_eol

.. doxygentypedef:: IH_input_cc

.. doxygentypedef:: IH_wcc

ENUMS
------
.. doxygenenum:: UI_CMD_ID      

.. doxygenenum:: UI_WC_FLAG

.. doxygenenum:: UI_COMPARE

.. doxygenenum:: UI_ARG_HANDLING
  
.. doxygenenum:: UITYPE

PROGMEM variables
------------------
.. doxygenvariable:: UserInput_type_strings_pgm    

.. doxygenvariable:: _pname

..
    .. doxygenvariable:: _peol

..
    .. doxygenvariable:: _pinputcc

..
    .. doxygenvariable:: _pwcc

..
    .. doxygenvariable:: _pdelimseq

..
    .. doxygenvariable:: _pststpseq

..
    .. doxygenvariable:: _DEFAULT_UI_INPUT_PRM_


Structs
--------
.. doxygenstruct:: InputProcessDelimiterSequences
   :members:
   :undoc-members:

.. doxygenstruct:: InputProcessStartStopSequences
   :members:
   :undoc-members:

.. doxygenstruct:: InputProcessParameters
   :members:
   :undoc-members:

.. doxygenstruct:: CommandRuntimeCalc
   :members:
   :undoc-members:

.. doxygenstruct:: CommandParameters
   :members:
   :undoc-members:

Classes
--------
.. doxygenclass:: CommandConstructor
   :members: 
   :protected-members:
   :private-members:
   :undoc-members:       
   :allow-dot-graphs:

.. doxygenclass:: UserInput
   :members: 
   :protected-members:
   :private-members:
   :undoc-members:      
   :allow-dot-graphs:

Source file
------------
.. literalinclude:: ../../../src/InputHandler.h
    :language: cpp
    :linenos:
    :caption: src/InputHandler.h