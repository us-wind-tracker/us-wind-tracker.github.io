# U.S. Wind Tracker

A dated log of federal actions, litigation and lease buybacks affecting U.S. wind energy, onshore and offshore, with the DoD Siting Clearinghouse thread marked so it can be viewed alone.

**Read it:** https://us-wind-tracker.github.io/

Every entry is written from a public source, and each links to the source it rests on.

## How entries are added

A scheduled search looks for new developments each weekday and publishes them to `data/items.json` directly. After each run that publishes something, it comments on the [Publication log](../../issues/2) listing what went up.

## Getting notified

Click **Watch** at the top of this repository and choose **All activity**. GitHub will then email you each time the Publication log gets a new comment, and whenever an entry is removed.

## Removing an entry

Under each entry on the site there is a **Remove** link. It opens a pre-filled request on GitHub; add a reason if you like, and click **Create**. An automatic job then:

1. checks that you are a member of this organization (requests from anyone else are declined),
2. takes the entry out of `data/items.json`,
3. records it in `data/removed.json`, so the scheduled search does not add it again, and
4. replies on the request and closes it.

The entry disappears from the site within a few minutes. To restore one, move its line from `data/removed.json` back into `data/items.json`.

## Suggesting an item or a correction

Open an [issue](../../issues/new) with the date, what happened and a link to a public source. Members can also edit `data/items.json` directly in the browser.

## The data file

`data/items.json` is a list with one entry per line. Each entry has these fields:

| Field | Meaning |
|---|---|
| `id` | `YYYYMMDD-short-description`, unique |
| `date` | Date the event happened, `YYYY-MM-DD` |
| `summary` | One or two sentences: who did what, with the case name and court for litigation |
| `project` | Project or lease, or `All wind` |
| `type` | `Litigation`, `Lease buyback`, `Regulatory action`, `Legislation / policy`, `Congressional oversight`, `Research / analysis`, `Project milestone` or `State / local` |
| `clearinghouse` | `true` when DoD or Clearinghouse review, or a national-security or radar rationale, is directly at issue |
| `mission` | The mission-relevance angle when `clearinghouse` is true, otherwise empty |
| `status` | `Pending`, `Ongoing` or `Resolved` |
| `next` | The next expected milestone, if the source states one |
| `actor` | Agency or court |
| `developer` | Developer, if any |
| `region` | State or states, or `National` |
| `scope` | `Offshore`, `Onshore` or `Both` |
| `tier` | `Primary` (filing, agency release, Federal Register), `Legal analysis` or `Press` |
| `source`, `url` | Name of the source and its link |

When editing by hand, keep the file valid JSON: the first line is `[`, the last is `]`, entries are separated by commas, and the last entry has no trailing comma. If the site shows "could not be loaded" after an edit, the file has a syntax error.
