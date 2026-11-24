# Git Basics (JD: "Version Control: Git basics")

### Q1. What is Git? Git vs GitHub?
**Answer:** Git is a **distributed version control system** that tracks changes to files. Every developer has the full history locally. GitHub, GitLab and Bitbucket are **hosting platforms** for Git repositories, with pull requests, issues and CI.
- **Example 1:** You can commit offline on your laptop (Git) and push to GitHub later.
- **Example 2:** A team reviews your RAG code via a pull request on GitHub or GitLab.

### Q2. What are working directory, staging area and repository?
**Answer:** **Working directory:** files you edit. **Staging area (index):** the changes you've selected for the next commit (`git add`). **Repository:** the committed history (`git commit`).
- **Example:** You changed 3 files but only want to commit 2: `git add a.py b.py` then `git commit`.

### Q3. Essential commands (know these cold)
```bash
git init                         # new repo
git clone <url>                  # copy remote repo
git status                       # what changed
git add file.py / git add .      # stage
git commit -m "Add NPA bucket logic"
git log --oneline --graph        # history
git diff / git diff --staged     # see changes
git branch feature/rag           # create branch
git switch feature/rag           # (or git checkout) move to branch
git switch -c feature/eval       # create + switch
git merge feature/rag            # merge into current branch
git pull                         # fetch + merge from remote
git push -u origin feature/rag   # publish branch
git stash / git stash pop        # park unfinished work
```

### Q4. What is a branch? Why use branches?
**Answer:** An independent line of development (a movable pointer to a commit). It lets you build features or fixes without breaking `main`.
- **Example 1:** `feature/text-to-sql` is developed and tested, then merged after review.
- **Example 2:** A `hotfix/recon-rounding` branch is created from main to fix a production bug quickly.

### Q5. git fetch vs git pull?
**Answer:** `fetch` downloads remote changes without changing your branch. `pull` = fetch + merge (or rebase) into the current branch.
- **Example:** `git fetch` then `git log origin/main` lets you look at teammates' changes before merging.

### Q6. Merge vs rebase?
**Answer:** **Merge** combines branches with a merge commit and preserves history as it happened. **Rebase** replays your commits on top of another branch for a linear history. Never rebase shared or public branches.
- **Example 1:** Merging a feature into main through a PR keeps a clear record.
- **Example 2:** `git rebase main` on your own local feature branch keeps it updated and clean before the PR.

### Q7. What is a merge conflict and how do you resolve it?
**Answer:** It happens when two branches change the same lines differently. Git marks the conflict:
```
<<<<<<< HEAD
NPA_DAYS = 90
=======
NPA_DAYS = 180
>>>>>>> feature/agri-rule
```
Edit the file to the correct final version, remove the markers, then `git add` and `git commit`. Talk to the teammate if you're unsure which is right.
- **Example 2:** Two people edit the same prompt template. Combine both improvements manually.

### Q8. How do you undo things?
| Situation | Command |
|---|---|
| Discard changes in a file | `git restore file.py` |
| Unstage a file | `git restore --staged file.py` |
| Fix the last commit message / add a forgotten file | `git commit --amend` (only if not pushed) |
| Undo a pushed commit safely | `git revert <hash>` (creates a new commit) |
| Move the branch back (local only) | `git reset --soft/--mixed/--hard <hash>` |
- **Example 1:** A bad commit is already on the shared main → `git revert`, not `reset`.
- **Example 2:** You committed locally to the wrong branch → `git reset --soft HEAD~1`, switch branch, commit again.

### Q9. What is .gitignore? What should go in it?
**Answer:** A list of files and patterns Git should not track: secrets, environments, large data, build outputs.
```
.env
.venv/
__pycache__/
*.pyc
data/raw/
chroma_db/
*.log
```
- **Example 1:** `.env` holds `ANTHROPIC_API_KEY`. It must never be committed.
- **Example 2:** Client data files must never go into Git, both for confidentiality and size.

### Q10. What is a pull request (PR) and code review?
**Answer:** A request to merge your branch, where teammates review the code, CI runs tests, and someone approves before the merge. It's maker-checker for code.
- **Example 1:** A PR "Add hybrid search to RAG" includes the evaluation results before and after.
- **Example 2:** The reviewer spots a hard-coded API key and blocks the merge.

### Q11. What makes a good commit?
**Answer:** Small, focused, with a meaningful message in the imperative mood: "Add SMA bucket classification", not "changes" or "final_final2".
- **Example:** Separate commits for "Refactor loader" and "Fix date parsing bug" make both easy to revert individually.

### Q12. What is a branching strategy?
**Answer:** **GitHub Flow:** main + short-lived feature branches + PRs. **Git Flow:** main, develop, feature, release, hotfix branches. Trunk-based development: frequent small merges to main behind feature flags.
- **Example:** An intern team uses GitHub Flow: branch → PR → review → merge → deploy.

### Q13. What is `git tag`? `git cherry-pick`?
- **tag:** marks a release point. `git tag v1.0` for the version delivered to a client.
- **cherry-pick:** applies one specific commit to another branch. Example: apply one bug-fix commit from develop to a release branch.

### Q14. What is CI/CD?
**Answer:** **Continuous Integration:** every push runs tests and linting automatically. **Continuous Delivery/Deployment:** automatically package and deploy.
- **Example 1:** A GitHub Actions workflow runs `pytest` (including the 50-question RAG eval) on every PR.
- **Example 2:** Merging to main builds a Docker image and deploys to a test server.
