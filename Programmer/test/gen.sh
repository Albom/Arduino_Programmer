#!/bin/bash
dd if=/dev/urandom of=rand8.bin bs=1 count=1024
md5sum rand8.bin

dd if=/dev/urandom of=rand16.bin bs=1 count=2048
md5sum rand16.bin

dd if=/dev/urandom of=rand64.bin bs=1 count=8192
md5sum rand64.bin
