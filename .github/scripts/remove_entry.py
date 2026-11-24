"""Remove one entry from data/items.json in response to a "Remove: <id>" issue.

The entry is recorded in data/removed.json so the scheduled search does not add
it again. Only users with write access to the repository may remove entries.
"""
import datetime
import json
import os
import re
import subprocess
import sys

REPO = os.environ["REPO"]
NUMBER = os.environ["ISSUE_NUMBER"]
TITLE = os.environ.get("ISSUE_TITLE", "")
BODY = os.environ.get("ISSUE_BODY", "") or ""
USER = os.environ["ISSUE_USER"]
ITEMS = "data/items.json"
REMOVED = "data/removed.json"


def run(*args, check=True):
    return subprocess.run(args, check=check, text=True, capture_output=True)


def reply_and_close(message, reason="completed"):
    run("gh", "issue", "comment", NUMBER, "--repo", REPO, "--body", message)
    run("gh", "issue", "close", NUMBER, "--repo", REPO, "--reason", reason)


def write_list(path, entries):
    with open(path, "w", encoding="utf-8") as f:
        f.write("[\n" + ",\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + "\n]\n")


def main():
    perm = run("gh", "api", f"repos/{REPO}/collaborators/{USER}/permission", "--jq", ".permission", check=False)
    if perm.returncode != 0 or perm.stdout.strip() not in ("admin", "maintain", "write"):
        reply_and_close(
            "Only members of this organization can remove entries, so nothing was changed. "
            "If you think this entry is wrong, open a new issue describing the problem and a member will look at it.",
            reason="not planned",
        )
        return

    entry_id = TITLE.split(":", 1)[1].strip()
    if not re.fullmatch(r"\d{8}-[a-z0-9-]+", entry_id):
        reply_and_close(f"`{entry_id}` is not an entry id, so nothing was changed. Use the Remove link under the entry on the site.", reason="not planned")
        return

    with open(ITEMS, encoding="utf-8") as f:
        items = json.load(f)
    match = [x for x in items if x.get("id") == entry_id]
    if not match:
        reply_and_close(f"No entry with id `{entry_id}` is on the tracker; it may already have been removed. Nothing was changed.", reason="not planned")
        return

    entry = match[0]
    items = [x for x in items if x.get("id") != entry_id]
    with open(REMOVED, encoding="utf-8") as f:
        removed = json.load(f)
    reason = BODY.split("Reason:", 1)[1].strip()[:500] if "Reason:" in BODY else ""
    removed.insert(0, {
        "id": entry_id,
        "date": entry.get("date", ""),
        "summary": entry.get("summary", ""),
        "url": entry.get("url", ""),
        "removed_on": datetime.date.today().isoformat(),
        "removed_by": USER,
        "reason": reason,
        "issue": int(NUMBER),
    })
    write_list(ITEMS, items)
    write_list(REMOVED, removed)

    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "add", ITEMS, REMOVED)
    run("git", "commit", "-m", f"Remove {entry_id} (requested in #{NUMBER} by {USER})")
    for attempt in range(3):
        if run("git", "push", check=False).returncode == 0:
            break
        run("git", "pull", "--rebase", check=False)
    else:
        reply_and_close("The entry could not be removed because the data file changed at the same moment. Please use the Remove link again.", reason="not planned")
        sys.exit(1)

    run("gh", "api", "-X", "POST", f"repos/{REPO}/pages/builds", check=False)
    reply_and_close(
        f"Removed `{entry_id}` ({entry.get('date', '')}): {entry.get('summary', '')}\n\n"
        "It disappears from the site within a few minutes and is listed in `data/removed.json`, "
        "so the scheduled search will not add it again. To restore it, move its line back into `data/items.json`."
    )


if __name__ == "__main__":
    main()
