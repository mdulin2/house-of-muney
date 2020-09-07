'''
Mmap LEAKLESS Chunk Overwrites 
;tldr: Rewrite symbol table of LibC to get code execution

Notes: 
- This POC should work on all versions of libc. But, the LibC 
  specific version for this is 2.31. 
- This technique only works if no or partial RELRO is used 
  with a dynamicly linked binary. 
- Full RELRO does not do LAZY dynamic symbol resolution so the technique
  does not work with full relro enabled. 


Steps in the code: 
- Buffer overflow (vulnerability) 
- Munmap LibC (.gnu.hash and .dynsym) 
- Allocate over LibC with mmap
- Rewrite string hashing and symbol table
- Pop shell :) 
'''

from pwn import * 
import os

mode = 'DEBUG' # Turn on gdb
libc_name = './2.31/libc-2.31.so' # Set LibC vesion
env = {}

# Binary setup
elf_name = './munmap_rewrite' 

elf = ELF(elf_name)
if libc_name != '': 
	libc = ELF(libc_name)
	env = {"LD_PRELOAD": libc.path}
	
# Process creation 
if mode == 'DEBUG': 
	p = process([ elf.path],env=env)

	# Set GDB to have source code debugging enabled
	gdb.attach(p, gdbscript='''
b 288
dir ./2.31
''')
else: 
	p = remote(domain, port) 

p.interactive()


