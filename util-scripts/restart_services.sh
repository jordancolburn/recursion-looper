#!/bin/bash
sudo systemctl daemon-reload
sudo systemctl stop recursionlooperled
sudo systemctl stop recursionlooperalsa
sudo systemctl stop recursionlooperbutton

sudo systemctl start recursionlooperled
sudo systemctl start recursionlooperalsa
sudo systemctl start recursionlooperbutton
