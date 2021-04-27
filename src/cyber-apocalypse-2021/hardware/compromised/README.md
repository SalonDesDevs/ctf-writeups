# Hw - compromised
For this challenge, we have again a Saleae Logic project. There are 2 channels:
![dump_logic](https://i.imgur.com/OQz980v.png)

This is a I²C communication with channel 0 being SDA and channel 1 SCL, the clock.
We can add a I²C analyzer on logic and extract the analysis to `dump.txt`.
```
{{#include dump.txt:1:10}}
```
Then we will use a python script to find the flag. 
```python
{{#include script.py:loading}}
```