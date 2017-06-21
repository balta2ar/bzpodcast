#!/bin/bash

#sudo /usr/bin/twistd -n web --path . -p 80
#sudo /usr/bin/twistd -n web --path . --port=80
sudo /usr/bin/twistd -n web --path . --port=tcp:80
