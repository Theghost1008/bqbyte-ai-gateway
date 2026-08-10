#!/bin/bash

git add .

if [ $? -ne 0 ]; then
    echo "Git add failed"
    exit 1
fi

echo "Enter commit message: "
read commit_msg

if [ -z "$commit_msg" ]; then
    echo "Commit message cannot be empty"
    exit 1
fi

git commit -m"$commit_msg"

if [ $? -ne 0 ]; then
    echo "Commit failed"
    exit 1
fi

git push origin "$(git branch --show-current)"

if [ $? -ne 0 ]; then    
    echo "Push Failed"
    exit 1
fi

echo "Changes committed and pushed successfully"
