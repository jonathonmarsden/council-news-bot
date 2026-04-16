# Learnings from Project 2026: Naming Inconsistencies

**Date**: 23 January 2026
**Issue**: Mangled hashtags on Bluesky (e.g., `#OrangeCityOf`) and inconsistent naming standards.

## 🔍 The Problem
Specific NSW councils were configured in `states/nsw/councils.json` using the inverted official registry format:
- `"name": "Orange, City of"`
- `"name": "Blue Mountains, City of"`

Additionally, many councils were listed merely by their locality type without the full corporate suffix:
- `"name": "Ballina Shire"` (Official: "Ballina Shire Council")
- `"name": "Bega Valley Shire"` (Official: "Bega Valley Shire Council")

This caused:
1.  **Awkward Display**: "Orange, City of" or "Ballina Shire" appearing in post text.
2.  **Mangled Hashtags**: The hashtag generator blindly stripped spaces/punctuation, resulting in `#OrangeCityOf`.
3.  **Ambiguity**: `#BallinaShire` could refer to the geographic region, whereas `#BallinaShireCouncil` refers to the government entity.

## 🛠️ The Solution
We have standardized the naming convention across the NSW configuration to match the **Official LGNSW List** (as of Jan 2026).

A bulk fix script (`scripts/maintenance/align_nsw_names.py`) was executed to align 64+ councils.

**Transformation Examples:**
- "Orange, City of" -> **"Orange City Council"**
- "Ballina Shire" -> **"Ballina Shire Council"**
- "Mosman Council" -> **"Mosman Municipal Council"**
- "Queanbeyan–Palerang Regional Council" -> **"Queanbeyan-Palerang Regional Council"** (En-dash normalized)

## 📝 Policy Update
**Naming Convention for `councils.json`**:
1.  **Source of Truth**: We strictly follow the naming in the [LGNSW Council Directory](https://lgnsw.org.au/Public/public/NSW-Councils/NSW-Council-Links.aspx).
2.  **Format**: Most names take the form `[Name] [Type] Council`.
3.  **Exceptions**: We respect the official exceptions where "City of" is retained (e.g., "City of Sydney", "City of Parramatta Council").
4.  **Hashtag Generation**: The system derives hashtags from the `name` field. We accept `#CityOfSydney` as the correct hashtag for that entity.

## 🚨 Action Items
- [x] Fix NSW JSON naming (Inversions: Orange, Blue Mountains).
- [x] Align NSW JSON with LGNSW Official List (Added "Council" suffix, normalized special chars).
- [ ] Monitor next batch of posts for naming correctness.
- [ ] Verify other states (VIC/QLD/WA) for similar consistency (e.g., "City of Perth" vs "Perth City Council").

## 🆔 ID Unification & State Collision (2026-01-24)

**Date**: 24 January 2026
**Issue**: Duplicate IDs detected across states, making the `id` field unreliable as a global primary key.
**Action**: Enacted "Unify IDs" protocol.

### Detected Collisions
The following generic IDs appeared in multiple `states/<state>/councils.json` files:
1.  `central-highlands` (QLD, TAS)
2.  `flinders` (QLD, TAS)
    - Note: SA has `flinders-ranges`, avoiding collision.
3.  `latrobe` (VIC, TAS)

### Resolution
Renamed specific IDs to include state suffixes, ensuring global uniqueness:

| Original ID | State | New ID |
| :--- | :--- | :--- |
| `central-highlands` | QLD | `central-highlands-qld` |
| `central-highlands` | TAS | `central-highlands-tas` |
| `flinders` | QLD | `flinders-qld` |
| `flinders` | TAS | `flinders-tas` |
| `latrobe` | VIC | `latrobe-vic` |
| `latrobe` | TAS | `latrobe-tas` |

**Outcome**: Confirmed **538** unique IDs across all configuration files. The `id` field is now safe to use as a global Primary Key for database migrations.
