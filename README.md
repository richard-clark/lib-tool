EAGLE Library Tool
==================

This module allows removal of unused EAGLE library items and the creation of libraries from components referenced in board and schematic files

Requirements
------------

This module requires the [EAGLE-Python][eaglepy] package for reading and writing EAGLE files.

Installation
------------

See [this page][eaglepy_installation] for EAGLE-Python installation instructions.

This module can be run by cloning into this repository:

	git checkout https://github.com/richard-clark/lib-tool
	cd lib-tool
	python lib-tool.py -h

Usage
-----

This module can be invoked from the command line, most simply as:

	python lib_tool.py -s my_schem.sch -l foo
	
This will remove unused library items, create a library named ``foo.lbr`` in the same directory, and create a copy named ``my_schem_out.sch`` which only references ``foo.lbr``. (If a board, ``my_schem.brd`` is also present in the same directory, it will update it and export ``my_schem_out.brd``.)

To overwrite the original input files (not recommended), use the ``-o`` flag:

	python lib_tool.py -o -s my_schem.sch -l foo
	
To specify the output files, use ``-S`` for the schematic file and ``-B`` for the board file, and ``-L`` for the library file:

	python lib_tool.py -s my_schem.sch -l foo -S foo.sch -B bar.brd -L foo_2.lbr
	
The module always requires an input schematic file. It assumes that there is a board file with the same name in the same path but with the ``.brd`` extension (as opposed to the ``.sch`` extension). If no board exists, use the ``-n`` flag to prevent the tool from looking for a board:

	python lib_tool.py -n -s my_schem.sch -l foo
	
To create a library, but _not_ remove unused items, use the ``-u`` flag:

	python lib_tool.py -u -s my_schem.sch -l foo
	
To remove unused items, but _not_ create a library, omit the ``-l`` flag:

	python lib_tool.py -s my_schem.sch
	
Duplicate Names
---------------

If two or more referenced libraries contain symbols, packages, or device sets with the same name, each will be renamed as ``original_library_name + object_name``. So, for example, given two libraries, ``foo`` and ``bar``, each with a package named ``res``, the package from ``foo`` would be renamed ``foo_res`` and the package from bar would be renamed ``bar_res``.
	
[eaglepy]: https://github.com/richard-clark/eaglepy
[eaglepy_installation]: ../projects/eagle-python.html#installation "EAGLE-Python Installation"