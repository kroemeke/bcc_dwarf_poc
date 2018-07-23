#!/usr/bin/env python
import sys
import pprint
from elftools.common.py3compat import bytes2str
from elftools.elf.elffile import ELFFile
from elftools.dwarf.locationlists import LocationEntry
import elftools.dwarf.compileunit
from elftools.dwarf.descriptions import (
    describe_DWARF_expr, set_global_machine_arch)




def offset_to_die(cu,offset):
    top_DIE = cu.get_top_DIE()
    for die in cu.iter_DIEs():
        if die.offset == offset:
            return die 
    return None


# recursive pretty printer of each DIE
def die_info_rec(die,search_var):
    if die.attributes.has_key('DW_AT_name'):
      if die.attributes['DW_AT_name'].value == search_var:
        if die.attributes.has_key('DW_AT_data_member_location'):
          return int(die.attributes['DW_AT_data_member_location'].value)
    for child in die.iter_children():
        x = die_info_rec(child,search_var)
        if x: return x

def die_info_struct(die,search,search_var):
  if die.tag == 'DW_TAG_structure_type':
    if die.attributes.has_key('DW_AT_name'):
      if die.attributes['DW_AT_name'].value == search:
        x = die_info_rec(die,search_var)
        return x
       
  for child in die.iter_children():
    x = die_info_struct(child,search,search_var)
    if x: return x

def show_struct_offset(path,cu,struct,var):
  print('Searching for compile unit %s in file %s struct %s variable %s' % (cu,path,struct,var))
  with open(path, 'rb') as f:
    elffile = ELFFile(f)
    dwarfinfo = elffile.get_dwarf_info()
    # iterate over all "compile units" - foo.c egg.c etc...
    for CU in dwarfinfo.iter_CUs():
      top_DIE = CU.get_top_DIE()
      if (top_DIE.attributes['DW_AT_name'].value == cu):
        x = die_info_struct(top_DIE,struct,var)
        if x: return x


if __name__ == '__main__':
  offset = show_struct_offset(sys.argv[1],'minimal.c','dupa_s','buf')
  print(offset)
