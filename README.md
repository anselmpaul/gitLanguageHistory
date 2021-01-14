# gitLanguageHistory

A small hacky script to create a csv file containing the history of languages used in a repository using [github-linguist](https://github.com/github/linguist/). 

Merge Commits are disregarded. Depending on the size of your repository and the amount of commits, this script can take quite a while. `linguist` takes 3-15 seconds per commit on my machine. A small repo with 15 commits, and a few files takes ~45s, in a big repo with +100 commits and lots of files, it can take multiple hours. 

**Caution**: If the script crashes or you stop it, it will leave your repository in `detached HEAD state`. You can fix this by simply running `git checkout main`.