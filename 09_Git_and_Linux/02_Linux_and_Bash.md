# Linux Command Line & Bash (JD Good-to-have: "Shell Scripting: Bash, Linux command line")

### Q1. Essential commands
| Command | Purpose | Example |
|---|---|---|
| `pwd`, `ls -lah`, `cd` | Navigate | `cd /data/2026/10 && ls -lah` |
| `mkdir -p`, `cp -r`, `mv`, `rm -r` | Files/folders | `mkdir -p reports/q3` |
| `cat`, `less`, `head -n`, `tail -n`, `tail -f` | View files | `tail -f pipeline.log` (live logs) |
| `wc -l` | Count lines | `wc -l loans.csv` (row count check) |
| `grep -i -r -n` | Search text | `grep -n "ERROR" pipeline.log` |
| `find` | Find files | `find . -name "*.csv" -mtime -1` (changed in the last day) |
| `sort`, `uniq -c` | Sort/count | `cut -d, -f3 loans.csv \| sort \| uniq -c` (loans per branch) |
| `cut`, `awk`, `sed` | Columns, transform | `awk -F, 'NR>1 && $7>90' loans.csv` (DPD > 90 rows; col 7 = dpd) |
| `chmod`, `chown` | Permissions | `chmod +x run.sh` |
| `ps aux`, `top`, `kill` | Processes | `ps aux \| grep python` |
| `df -h`, `du -sh` | Disk usage | `du -sh data/*` |
| `ssh`, `scp` | Remote | `scp report.xlsx user@server:/reports/` |
| `curl`, `wget` | HTTP | `curl -s https://api.example.com/health` |
| `tar`, `zip`, `unzip` | Archives | `tar -czf backup.tgz data/` |
| `nohup`, `&`, `screen`/`tmux` | Long-running jobs | `nohup python index.py > out.log 2>&1 &` |

### Q2. What do pipes `|` and redirection `>`, `>>`, `2>&1` do?
**Answer:** A pipe sends one command's output to the next command. `>` overwrites a file, `>>` appends, and `2>&1` sends errors (stderr) to the same place as normal output (stdout).
- **Example 1:** Count errors by type: `grep ERROR app.log | awk '{print $4}' | sort | uniq -c | sort -nr`.
- **Example 2:** `python job.py >> job.log 2>&1` captures both output and errors in one log.

### Q3. Explain file permissions `rwxr-xr--` / `chmod 755`
**Answer:** There are three groups: owner, group, others. r=4, w=2, x=1. So 755 = owner rwx (7), group r-x (5), others r-x (5).
- **Example 1:** `chmod 600 .env` makes the secrets file readable only by you.
- **Example 2:** `chmod +x run_recon.sh` makes the script executable.

### Q4. Write a simple Bash script
```bash
#!/bin/bash
set -euo pipefail            # stop on errors, undefined vars, pipe failures

DATE=${1:-$(date +%Y-%m-%d)}  # first argument or today
IN_DIR="/data/incoming/$DATE"
LOG="/var/log/recon_$DATE.log"

if [ ! -d "$IN_DIR" ]; then
  echo "Input folder $IN_DIR missing" | tee -a "$LOG"
  exit 1
fi

for f in "$IN_DIR"/*.csv; do
  rows=$(($(wc -l < "$f") - 1))   # minus header
  echo "$(basename "$f"): $rows rows" | tee -a "$LOG"
done

python3 /opt/recon/run_recon.py --date "$DATE" >> "$LOG" 2>&1
echo "Done" | tee -a "$LOG"
```
- **Example 2:** Run it daily via cron: `0 7 * * * /opt/recon/run.sh`.

### Q5. Variables, conditionals and loops in Bash?
```bash
name="Fintellix"; echo "Hello $name"
if [ "$count" -gt 0 ]; then echo "has rows"; elif [ "$count" -eq 0 ]; then echo "empty"; else echo "?"; fi
for f in *.pdf; do echo "Processing $f"; done
while read -r line; do echo "$line"; done < accounts.txt
```
- **Example:** Loop over every PDF and run a Python extractor on each.

### Q6. What is an environment variable? How do you set it?
**Answer:** A key-value setting available to processes. `export ANTHROPIC_API_KEY=...` (for this session), or put it in `~/.bashrc`. Read it in Python with `os.environ`.
- **Example 1:** `echo $PATH` shows where the shell looks for programs.
- **Example 2:** `ENV=prod python app.py` sets the variable for that one command only.

### Q7. How do you check why a server job failed?
**Answer:** Check whether the process is running (`ps aux | grep`), read the logs (`tail -n 100 log`, `grep -i error`), check disk space (`df -h`) and memory (`free -h`), check permissions, and check whether the cron entry ran (`grep CRON /var/log/syslog`).
- **Example 1:** The job crashed because the disk was 100% full of old logs. Clean them up and add log rotation.
- **Example 2:** It failed with "Permission denied" on the output folder → fix ownership with `chown`.

### Q8. Quick CSV analysis without Python?
```bash
head -1 loans.csv                       # see header
wc -l loans.csv                         # row count
awk -F, 'NR>1 {sum+=$6} END {print sum}' loans.csv     # sum column 6
awk -F, 'NR>1 && $7>90' loans.csv | wc -l               # NPA count (col 7 = dpd)
```
(Simple awk breaks on quoted commas. Use Python or csvkit for real CSVs.)

### Q9. Absolute vs relative path? What are `~`, `.` and `..`?
**Answer:** An absolute path starts at `/`. A relative path starts from the current directory. `~` is home, `.` is the current directory, `..` is the parent.
- **Example:** In cron, always use absolute paths, because cron's working directory and PATH differ from your shell's.

### Q10. What is SSH? What are SSH keys?
**Answer:** SSH is a secure remote shell. Key-based authentication uses a private key (kept secret) and a public key (placed on the server), which is safer than passwords.
- **Example:** `ssh-keygen -t ed25519`, then add the public key to GitHub to push without a password.
