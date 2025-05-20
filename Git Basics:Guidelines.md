### Create a GitHub repository from a local project

1. to create a new Github repository in an existing (potentially not empty) folder, use the `git init` command from the command line.
2. then add files separately `git add filename` or all at once `git add -A`
3. now the changes need to be commited with `git commit -m 'commit message'`
4. Create a remote repository on GitHub
5. Now, push your existing repository: 
```
git remote add origin git@github.com:username/new_repo
git push -u origin master
```

### Branching Basics
Some important commands in this context:
- `git branch` shows a list of all branches, as well as the currently active branch.
- To create a new branch use 
