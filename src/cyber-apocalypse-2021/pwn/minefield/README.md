# Pwn - Minefield

For this challenge we don't have the libc so first thing we do is to
disassemble the program to know what it does.

This one doesn't do a lot, it's not a buffer overflow or something like this.
All it does is write what we want where we want.

First thing we need to do is navigate through the menus to plant the value
we want.

```python
{{#include attack.py:choose_menu}}
```

Here it asks us what type of mine we want to plant but in reality it's
where we want to set the value.
One good candidate is where is stored the function that runs destructors
at the end of the program, the value of this function is stored behind
the `__do_global_dtors_aux_fini_array_entry` symbol.

```python
{{#include attack.py:www_where}}
```

Next we need to set the value we want, so what we'll send is the address
of the function we wish to execute.
By disassembling the binary we can find a function named `_` that will
print the flag to us, so here's our win function.

```python
{{#include attack.py:www_what}}
```

Now the bomb as been planted and we've the flag!
