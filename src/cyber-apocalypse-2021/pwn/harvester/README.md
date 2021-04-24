# Pwn - Harvester

This challenge is harder than the two others, first thing it's a PIEs.
And it's full of canaries, so if we find a buffer overflow we'll need to set it
to the correct value.

By exploring the binary we find two vulnerabilities.
* The first one is format string vulnerability inside the `fight` function.
* The second is a buffer overflow inside the `stare` function just large enough
  to overwrite one return address.

We can trigger the `fight` vulnerability when we want, but the `stare` one is
only available if we have a specific amount of pie on us.
Instead of farming pies, we found a logic bug inside the `inventory` function
that allows us to drop a negative amount of pies.

So first thing to do is to leak some values from the stack, for this we did this
function.

```python
{{#include attack.py:format_exploit_fn}}
```

The first thing we want to retrieve is the canary to not trigger the overflow
check failure.

```python
{{#include attack.py:retrieve_canary_fn}}
```

The second thing we need to retrieve is the libc base address. To do this we can
go through the stack to find return addresses, until we find the main return
address, we can continue and we see where does the main function returns inside
the `__libc_start_main` function. Meaning we've an address and can easily find
the offset so we know the libc base address.

```python
{{#include attack.py:retrieve_libc_base_address_fn}}
```

Now that we know the canary and the libc base address we need to prepare ourself
by having the right amount of pie.

```python
{{#include attack.py:drop_pie_fn}}

drop_pie('-11')
```

Finally we can do the overflow, the only problem is: where to return ? We can
only return to one address. For this,
[one_gadget](https://github.com/david942j/one_gadget) exists. If we provide the
libc we're using, it gives us a list of return address that can open a shell.

Now that we know one of this super duper cool addresses we can forge our
payload.

```python
{{#include attack.py:retrieve_shell_fn}}
```

Now, with a shell, all we need to do is to cat the flag!
