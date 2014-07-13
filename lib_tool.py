import argparse
from eaglepy import eagle, primitives, default_layers
import os

def camel_case_to_snake_case(s):
    """
    Attempt to convert camel case to snake case.
    
    Inserts an underscore between any upper-case letter which immediately follows a lower-case letter.
    
    :param s: The input string. 
    
    :returns: The snake-case representation of the input string.
    """
    
    out_str = ''
    
    if len(s) > 0:
        out_str += s[0]
    
    for i in range(1, len(s)):
        if s[i-1].isalpha() and s[i-1].islower() and s[i].isalpha() and s[i].isupper():
            out_str += '_'
        out_str += s[i]

    return out_str

def formatted_library_name(name):
    """
    Given a library name, return the symbol name or package name-friendly version. 
    
    The requires that the string be converted to uppercase and that spaces be removed. 
    Snake case is converted to camel case for improved readability. 
    
    :param name: The library name.
    
    :returns: A name suitable for use in a packge or symbol name.
    """
    
    return camel_case_to_snake_case(name).upper().replace(' ', '_')
    
def get_lib_and_package_for_package_name_dict(libraries):
     
    """
    Get a dictionary whose key is a package name and whose value is a list of the corresponding
    libraries and packages, each stored as a tuple:
     
    packages = {
       package_name_1: [(library_1_1, package_1_1)],
       package_name_2: [(library_2_1, package_2_1), (library_2_2, package_2_2)]
    }
     
    (Note: package_name_2 has duplicate packages.)
    
    :param libraries: A list of libraries.
    
    :returns: A dictionary whose key is the package name and whose value is a list of library/package
    tuples with that name.
    
    """
     
    packages = {}
     
    # Whether duplicate package names exist.
    duplicate_package_names = False
     
    # Iterate over each library
    for l in libraries:
        # Iterate over each package in the library. Add it to the dictionary of packages.
        for p in l.packages:
            if packages.has_key(p.name):
                packages[p.name].append((l, p))
                duplicate_package_names = True
            else:
                packages[p.name] = [(l, p)]
     
    if duplicate_package_names:
        print('Duplicate package names found.')
         
    return packages
     
  
def get_lib_and_symbol_for_symbol_name_dict(libraries):
     
    """
    Get a dictionary whose key is a symbol name and whose value is a list of the corresponding
    libraries and symbols, each stored as a tuple:
     
    packages = {
       symbol_name_1: [(library_1_1, symbol_1_1)],
       symbol_name_2: [(library_2_1, symbol_2_1), (library_2_2, symbol_2_2)]
    }
     
    (Note: symbol_name_2 has duplicate symbols.)
    
    :param libraries: A list of libraries.
    
    :returns: A dictionary whose key is the symbol name and whose value is a list of library/symbol
    tuples with that name.
    
    """
     
    symbols = {}
     
    # Whether duplicate symbol names exist.
    duplicate_symbol_names = False
     
    # Iterate over each library
    for l in libraries:
        # Iterate over each package in the symbol. Add it to the dictionary of symbols.
        for s in l.symbols:
            if symbols.has_key(s.name):
                symbols[s.name].append((l, s))
                duplicate_symbol_names = True
            else:
                symbols[s.name] = [(l, s)]
     
    if duplicate_symbol_names:
        print('Duplicate symbol names found.')
         
    return symbols
  
def get_lib_and_dev_set_for_dev_set_name_dict(libraries):
     
    """
    Get a dictionary whose key is a device set name and whose value is a list of the corresponding
    libraries and device sets, each stored as a tuple:
     
    device_sets = {
       device_set_name_1: [(library_1_1, device_set_1_1)],
       device_set_name_2: [(library_2_1, device_set_2_1), (library_2_2, device_set_2_2)]
    }
     
    (Note: device_set_name_2 has duplicate device sets.)
    
    :param libraries: A list of libraries.
    
    :returns: A dictionary whose key is the device set name and whose value is a list of library/device set
    tuples with that name.
    """
     
    # Copy the device sets
    device_sets = {}
      
    duplicate_device_sets = False
      
    for l in libraries:
         
        for d in l.device_sets:
             
            if device_sets.has_key(d.name):
                device_sets[d.name].append((l, d))
                duplicate_device_sets = True
            else:
                device_sets[d.name] = [(l, d)]
                  
      
    if duplicate_device_sets:
        print('Duplicate device sets found.')
         
    return device_sets
    
    
def get_name_dict_and_append_item(lib_item_dict, out_list):
    """
    Given a dictionary whose keys are names and whose values are a list of library/item tuples,
    renames all items which have non-unique names. Append the renamed item to ``out_list``.
    
    :param lib_item_dict: A dictionary whose keys are names and whose values are a list of library/item tuples.
    :param out_list: The list to which to append the renamed item.
        
    """

    keys = lib_item_dict.keys()
    
    # Iterate over all of the packages.
    for _name in keys:
        pairs = lib_item_dict[_name]
        
        if len(pairs) > 1:
            # Duplicate names exist
            for p in pairs:
                lib = p[0]
                item = p[1]
                
                # Get a unique name for the item
                new_name = formatted_library_name(lib.name) + '_' + _name
                
                # Update the item name
                item.name = new_name
                
                print('Item {0} renamed from {1} to {2}'.format(item, _name, new_name))
                
                # Add the item to the list (of either packages or symbols or device_sets)
                out_list.append(item)
        else:
            lib = pairs[0][0]
            item = pairs[0][1]
        
            # Add the item to the list (of either packages or symbols or device_sets)
            out_list.append(item)
    
class Lib_Tool_Stats():
    def __init__(self):
        self.libs_removed = 0
        self.device_sets_removed = 0
        self.devices_removed = 0
        self.packages_removed = 0
        self.symbols_removed = 0
    
    def to_stdout(self):
        # Print statistics
        print('Removed {0} unused libraries'.format(self.libs_removed))
        print('Removed {0} unused device sets'.format(self.device_sets_removed))
        print('Removed {0} used devices.'.format(self.devices_removed))
        print('Removed {0} unused packages.'.format(self.packages_removed))
        print('Removed {0} unused symbols.'.format(self.symbols_removed))
    
def lib_tool(args):
    """
    Run the tool with the specified argument to remove unused items, extract items to a
    library, or both. 
    
    :param args: A ``Lib_Tool_Arg`` instance.
    
    :returns: A ``Lib_Tool_Stats`` instance.
    """

    # Create a new EAGLE library
    if args.library_name != None:
        lib = eagle.Library(name = args.library_name)

    # Open the file
    e_sch = eagle.Eagle.load(args.input_sch_file)
    
    # Get the drawing
    sch = e_sch.drawing.document
    
    # Get the board
    if args.input_brd_file != None:
        e_brd = eagle.Eagle.load(args.input_brd_file)
        brd = e_brd.drawing.document
    
    if args.keep_unused == False:
        # Create sets of used libraries, used device sets, and used devices
        used_libraries = set([])
        used_device_sets = set([])
        used_devices = set([])
        
        for p in sch.parts:
            if not p.library in used_libraries:
                used_libraries.add(p.library)
                
            if not p.device_set in used_device_sets:
                used_device_sets.add(p.device_set)
                
            if not p.device in used_devices:
                used_devices.add(p.device)
        
        # Statistics 
        stats = Lib_Tool_Stats()
        
        # Iterate over all of the libraries referenced in the schematic. 
        
        for l in sch.libraries:
    
            # If the library is not referenced, remove it and continue.
            if not l in used_libraries:
                sch.libraries.remove(l)
                stats.libs_removed += 1
                continue 
    
            used_packages = set([])
            used_symbols = set([])
    
            # Iterate over the device sets in the library. 
            for ds in l.device_sets:
            
                if not ds in used_device_sets:
                    l.device_sets.remove(ds)
                    stats.device_sets_removed += 1
                    continue
                else:
                    for g in ds.gates:
                        if not g.symbol in used_symbols:
                            used_symbols.add(g.symbol)
                
                # Iterate over the devices in the device set.
                for d in ds.devices:
                
                    if not d in used_devices:
                        ds.devices.remove(d)
                        stats.devices_removed += 1
                    else:
                        if not d.package in used_packages:
                            used_packages.add(d.package)
                            
            # Iterate over all of the symbols in the library and remove unused.
            for s in l.symbols:
                if not s in used_symbols:
                    l.symbols.remove(s)
                    stats.symbols_removed += 1
                            
            # Now, iterate over all of the packages in the library and remove unused.
            for p in l.packages:
                if not p in used_packages:
                    l.packages.remove(p)
                    stats.packages_removed += 1
        
    if args.library_name != None:
        # All device sets, symbols, and packages will be combined into a single library. 
        # A library cannot contain duplicate names, however, so we must determine if duplicate
        # names exist and if so, make the names unique.
        
        # Get a dictionary whose key is a package name and whose value is a list of the corresponding
        # libraries and packages in the library with that name.
        packages = get_lib_and_package_for_package_name_dict(sch.libraries)
        # Update any duplicate package names and add each package to the library
        get_name_dict_and_append_item(packages, lib.packages)
        
        # Get a dictionary whose key is a symbol name and whose value is a list of the corresponding
        # libraries and symbols in the library with that name.
        symbols = get_lib_and_symbol_for_symbol_name_dict(sch.libraries)
        # Update any duplicate symbol names and add each symbol to the library
        get_name_dict_and_append_item(symbols, lib.symbols)
        
        # Get a dictionary whose key is a device set name and whose value is a list of corresponding
        # libraries and symbols in the library with that name.
        device_sets = get_lib_and_dev_set_for_dev_set_name_dict(sch.libraries)
        # Update any duplicate device set names and add each device set to the library
        get_name_dict_and_append_item(device_sets, lib.device_sets)
             
        # Replace all existing libraries with the new library
        sch.libraries = [lib]
        
        if args.input_brd_file != None:
            brd.libraries = [lib]
        
        # Update all the parts to reference the new library
        for p in sch.parts:
            p.library = lib

        # Update all the elements to reference the new library
        if args.input_brd_file != None:
            for e in brd.elements:
                e.library = lib

    # Save the files         
    e_sch.save(args.output_sch_file)
    
    if args.input_brd_file != None:
        e_brd.save(args.output_brd_file)
    
    # Save the library
    if args.output_lbr_file != None:
        # Create the drawing
        grid = eagle.Grid()
        layers = default_layers.get_layers()
        e_drawing = eagle.Drawing(settings = {}, grid = grid, layers = layers, document = lib)
        
        # Create the Eagle object
        e_lbr = eagle.Eagle(e_drawing)
        
        # Save the library file
        e_lbr.save(args.output_lbr_file)
        
    return stats
    
def _existing_file(path):
    """
    Returns the input argument if the path specifies an existing file, or raises an exception.
    
    :param path: The path to the file.
    
    :raises: An Exception, if path does not specify an existing file.
    
    :returns: path.
    
    """
    
    if os.path.isfile(path) == False:
        raise argparse.ArgumentError('File {0} does not exist.'.format(path))
    
    return path


class Lib_Tool_Args():
    def __init__(self, input_sch_file,
                 input_brd_file,
                 library_name,
                 output_sch_file,
                 output_brd_file,
                 output_lbr_file,
                 keep_unused):
        """
        Constructor.
        
        :param input_sch_file: The input schematic file name (required). 
        :param input_brd_file: The input board file name (may be None).
        :param library_name: The name of the library to create (may be None).
        :param output_sch_file: THe output schematic file name (required).
        :param output_brd_file: The output board file (may be None if input_brd_file is None).
        :param output_lbr_file: The output library file name (may be None).
        :param keep_unused: A Boolean value specifying whether to keep unused library items.
        """
        self.input_sch_file = input_sch_file
        self.input_brd_file = input_brd_file
        self.library_name = library_name
        self.output_sch_file = output_sch_file
        self.output_brd_file = output_brd_file
        self.output_lbr_file = output_lbr_file
        self.keep_unused = keep_unused
        
    @staticmethod
    def parse(input_args):
        SUFFIX = '_out'
        
        parser = argparse.ArgumentParser(description='Extract libraries from EAGLE files, and remove unused library items.')
    
        parser.add_argument('-s', type=_existing_file, required=True, help='The input schematic file.')
        parser.add_argument('-n', action='store_true', help='Do not output a board file.')
        parser.add_argument('-b', type=_existing_file, help='The input board file. (Default: <sch_name>.brd in the schematic directory.)')
        parser.add_argument('-l', type=str, help='The library name.')
        parser.add_argument('-u', action='store_true', help='Keep unused items. (Default: false.)')
        parser.add_argument('-S', type=str, help='The output schematic file. (Default: the input file with "_out" suffix.)')
        parser.add_argument('-B', type=str, help='The output board file. (Default: the input file with "_out" suffix.)')
        parser.add_argument('-L', type=str, help='The output library file. (Default: <lib_name>.lbr in the schematic directory.)')
        parser.add_argument('-o', action='store_true', help='Overwrite input files (do not add a suffix to the output file names).')
        args = parser.parse_args(input_args)
    
        if args.B != None and (args.b == None and args.n):
            raise parser.error('Output board file specified with no input board file specified. (The -B flag requires the -b flag.)')
    
        if args.b != None and args.n == True:
            raise parser.error('The -b and -n flags are mutually exclusive.')
        
        if args.L != None and args.l == None:
            raise parser.error('Output library file specified with no library name specified. (The -L flag requires the -l flag.)')
    
        if args.l == None and args.u:
            raise parser.error('Nothing to do--unused items will not be deleted and no library will be output.')
    
        input_sch_dir, input_sch_name_ext = os.path.split(args.s)
        input_sch_name = os.path.splitext(input_sch_name_ext)[0]
        input_sch_file = args.s
        
        library_name = args.l
        
        # Get the input board file
        if args.b != None:
            input_brd_file = args.b
            input_brd_dir, input_brd_name_ext = os.path.split(args.b)
            input_brd_name = os.path.splitext(input_brd_name_ext)[0]
        elif args.n == True:
            input_brd_file = None
        else:
            input_brd_file = input_sch_dir + os.path.sep + input_sch_name + '.brd'
            if os.path.isfile(input_brd_file) == False:
                raise parser.error('Input board file {0} does not exist.'.format(input_brd_file))
            input_brd_dir = input_sch_dir
            input_brd_name = input_sch_name
        
        # Get the output schematic file
        if args.S != None:
            output_sch_file = args.S
        elif args.o:
            output_sch_file = args.s
        else:
            output_sch_file = input_sch_dir + os.path.sep + input_sch_name + SUFFIX + '.sch'
        
        # Get the output board file
        if input_brd_file != None:
            if args.B != None:
                output_brd_file = args.B
            elif args.o:
                output_brd_file = input_brd_file
            else:
                if args.S != None:
                    output_sch_dir, output_sch_name_ext = os.path.split(args.S)
                    output_sch_name, = os.path.splitext(output_sch_name_ext)[0]
                    output_brd_file = output_sch_dir + os.path.sep + output_sch_name + SUFFIX + '.brd'
                else:
                    output_brd_file = input_brd_dir + os.path.sep + input_brd_name + SUFFIX + '.brd'
        else:
            output_brd_file = None
            
        # Get the output library file
        if args.l != None:
            if args.L != None:
                output_lbr_file = args.L
            elif args.o:
                output_lbr_file = input_sch_dir + os.path.sep + args.l + '.lbr'
            else:
                output_lbr_file = input_sch_dir + os.path.sep + args.l + SUFFIX + '.lbr'
        else:
            output_lbr_file = None
        
        return Lib_Tool_Args(input_sch_file, input_brd_file, library_name, output_sch_file, output_brd_file, output_lbr_file, args.u)
                
        lib_tool(args.s, input_brd_file, args.l, output_sch_file, output_brd_file, output_lbr_file, args.u)
        
if __name__ == '__main__':
    args = Lib_Tool_Args.parse(None)
    lib_tool(args)
    