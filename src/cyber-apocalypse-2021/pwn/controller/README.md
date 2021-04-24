# Pwn - Controller

The challenge gives us a file named `controller` and the libc used. So we tell
pwntools to load them.

```python
{{#include attack.py:loading}}
```

We need to find a vulnerability, so first thing we do is disassemble the
`controller` executable and search for any weird code.
Inside the `calculator` function we can find the usage of a scanf using the
"%s" formatter to some address on the stack. This means that we can write as
much data as we want, this allows us to rewrite the stack frames to execute
the functions we want.

To access the overflow we need to find an operation that gives `65338`, for
this we will do `-32669 * -2`, we navigate the menus until we are asked for
the payload.

```python
{{#include attack.py:fn_prepare_overflow}}
```

The scanf starts at [rbp - 0x28] so we need to fill the start of the payload
with 0x28 garbage bytes.

```python
{{#include attack.py:offset_overflow}}
```

The first thing we need to do is to retrieve to libc base address. This allows
us to return to any function on the libc (ret2libc). This means that we can
return to a function such as `system` and execute a shell.

```python
{{#include attack.py:fn_retrieve_libc_base}}
```

Now that we know the libc base address, we need to open a shell to be able to
print the flag.

```python
{{#include attack.py:fn_retrieve_shell}}
```

And finally, let's put all of this together and cat this flag!

```python
{{#include attack.py:cat_flag}}
```
