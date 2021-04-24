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

To access this overflow we need to go through the report problem section of the
program.

This part is accessible if we somehow find an operation with two numbers below
or equal to `0x45` that gives us `65338`. If any of these two number is above
it gives us an error `"We cannot use these many resources at once"` and exits.

A scanf with the `"%d"` formatter is used to retrieve both numbers. This allows
us to pass negative numbers.

So here comes the hardest maths of the whole ctf (including the crypto
challenges).

We will use a multiplication and we need to find `a` and `b` both under `70`
that when multiplied together gives `65338` so here is our difficult computation
`-32669 * -2 = 65338`a.

Now that we answered this difficult math question, we navigate the menus until
we are asked for this payload.

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
