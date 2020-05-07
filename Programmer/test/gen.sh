#!/bin/bash
dd if=/dev/urandom of=rand8.bin bs=1 count=1024
dd if=/dev/urandom of=rand16.bin bs=1 count=2048
dd if=/dev/urandom of=rand64.bin bs=1 count=8192
