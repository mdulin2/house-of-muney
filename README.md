# House of Muney
Code execution via corrupting mmap malloc chunks with ASLR bypass

## Intro
Are you tired of ASLR getting in your way? Annoyed by how unexploitable mmap chunks feel in GLibC malloc?   
Well, today is your lucky day! This is a full explanation on how a **leakless** heap exploitation technique that gives you **code execution**, that is 100% deterministic
What is this, the year 2000!?  
  
This technique IN FULL is described at https://maxwelldulin.com/BlogPost?post=6967456768 and was first used in a Qualysis exploit at https://www.qualys.com/2020/05/19/cve-2005-1513/remote-code-execution-qmail.txt

## But How? 
At a high level, this technique rewrites the lazy dynamic symbol resolution process of a library. You are probably thinking: *this is black magic*.  
And that's because this is, but I hope that this repository (and blog post alongside this) can help out with that. 

<ol>
<li>
Overwrite GLibC Malloc mmap chunk <i>size</i> or <i>prev_size</i>
</li>
<li>Free the mmap chunk (with munmap) to small amount of memory mapping of part of LibC (<code>.gnu.hash, .dynsym</code>)</li>
<li>Get mmap chunk over the top of LibC region</li>
<li>Rewrite <code>.gnu.hash</code> and <code>.dynsym</code> sections of LibC ELF</li>
<li>Call previously uncalled function for code execution</li>
</ol>

## When Is this Possible? 
Of course, there are a few drawbacks. But, most of these are just knowledge about how the program *exactly* works, rather than a complete destroyer of the technique (besides the first one).
<ol>
<li>Full RELRO or a static binary would prevent this attack from being successful because all symbols are loaded prior to the program running (no lazy symbol resolution)</li>
<li>Known <b>relative</b> location of the overwritten chunk. In some scenarios, this may need to be brute forced</li>
<li>The LibC (or other library) being attacked must be known or brute forced in order to have the offsets work properly</li>
<li>Fairly good control over the size of allocations in order to get mmap chunks in the proper locations</li>
</ol>
