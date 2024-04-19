#!/bin/bash
mv "$(echo $ENVFILE | sed s/\\\'//g)" .