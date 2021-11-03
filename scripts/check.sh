#!/bin/bash

IP="$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
curl $IP:8080
