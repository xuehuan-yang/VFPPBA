#!/bin/bash
if [ $# -eq 0 ]
then 
	pushmessage=`date +%A-%d/%B/%Y-%H:%M:%S`
else
		pushmessage="$*"
fi
echo ${pushmessage}
git pull;
git status;
git add -A; 
git commit -m "${pushmessage}";
git push -u origin main
