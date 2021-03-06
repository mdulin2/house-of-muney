#!/bin/bash 

# Deals with the elf patching and versioning for us

version=( 2.31 )
file_name=munmap_rewrite

echo "Compile: munmap_rewrite"

# Compile the code for non-leakless technique
$(gcc $file_name.c -o $file_name -ggdb) 

loader=$(realpath $(pwd)/$version/ld-$version.so)

echo "Set loader to version $version at $loader" 
patchelf --set-interpreter $loader ./$file_name
