#!/bin/bash
cd sessions/$1
java -jar ../../post2st.jar code.post -l &> out
