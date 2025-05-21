### Create a GitHub repository from a local project

1. to create a new Github repository in an existing (potentially not empty) folder, use the `git init` command from the command line.
2. then add files separately `git add filename` or all at once `git add -A`
3. now the changes need to be commited with `git commit -m 'commit message'`
4. Create a remote repository on GitHub
5. Now, push your existing repository: 

```bash
git remote add origin git@github.com:username/new_repo
git push -u origin master
```

### Branching Basics
Some important commands in this context:

- `git branch` shows a list of all branches, as well as the currently active branch.
- To create a new branch use `git branch new-branch-name`.
- To change the active branch use `git switch branch-name`
- to merge the currently active branch with another one (lets say `hotfix`), use `git merge issue02`. If the two branches have not diverged, the merge becomes a simple fast forward, i.e. the branch pointer of main is moved to the same commit as `hotfix`.
- once a branch is no longer needed it can be deleted with `git branch -d hotfix`

### Restoring Files

To restore a file use to a previous version use:

```bash
git restore --source=<commit> path/to/file
```

To restore it to the version in a different branch use:

```bash
git restore --source=branch path/to/file
```