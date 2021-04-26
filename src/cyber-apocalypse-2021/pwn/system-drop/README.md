# Pwn - System dROP

The name of this challenge gives us a big hint. It's talking about a ROP.
Unfortunately for the price of this hint we don't know which libc is being
used, so returning on a specific function of the libc is going to be hard.

By analysing the binary we find a main function which does a buffer overflow and
then returns 1.
This is really useful because it means when we'll start the rop, 1 will be
loaded inside the `rax` register.
And this is great because we can find a function named `_syscall` that
finishes with a `syscall` instruction then a `ret`.
Because the `rax` register will be set to `1`, we can do a write syscall.

This will allow us to leak got entries.

```python
{{#include attack.py:fn_leak_got}}
```

Now that we can leak entries from the got table, we will leak two functions
this way we can determine which libc is being used.

```python
{{#include attack.py:leak_got}}
```

Once we've the address of `__libc_start_main` and `read` we can use a website
like [libc.blukat.me](https://libc.blukat.me) to find the libc currenly used.
This gives us the following libc.
All we know need is to set its base address using symbols we leaked.

```python
{{#include attack.py:set_base}}
```

Finally we'll retrieve a shell, for this a simple rop to load the "/bin/sh"
string inside the `rdi` register and then return to the system function.

```python
{{#include attack.py:retrieve_shell}}
```

Now that we have a shell, all we need is to cat the flag!

```python
{{#include attack.py:cat_flag}}
```
