#!/bin/bash
cd sessions/$1
java -jar ../../post_to_st.jar code.post 1> stdout 2> stderr

cat src-gen/* > code.st

cat stdout stderr > out
rm stdout stderr
