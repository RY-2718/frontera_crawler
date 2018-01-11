#!/bin/bash

percent=`df | grep "xvda1" | awk '{print $5}' | sed 's/[^0-9]//g'`
if [ $percent -gt 90 ] ; then
  ps alx | grep python | grep "PARTITION" | awk '{print $3}' | xargs kill
fi
