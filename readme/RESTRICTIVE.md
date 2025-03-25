## Restrictive

Restrictive airspace covers all airspace: Alert (A), Caution (C), Danger (D), Military Operations Area (M), Prohibited (P), Restricted (R), Training (T), and Warning (W).

The Restrictive object has the following properties:

| Property         | Required | Type     | Default                     | Description                                                        |
| ---------------- | -------- | -------- | --------------------------- | ------------------------------------------------------------------ |
| `restrictive_id` | \*       | `string` |                             | A string representing the identifier for the restrictive airspace. |
| `file_name`      |          | `string` | `{mapType}_{restrictiveId}` | A string representing the filename that the map will be saved to.  |

**NOTE**: Naming in the CIFP file is mostly standardized, but has some quirks, particularly for MOAs. It may be worth opening the CIFP file and searching for the entry. For example, Stumpy Point MOA appears in the file as `STUMPY PT`. If your program supports regex, you can search with `SUSAUR..M` and start typing the MOA name right after the `M` (e.g., `SUSAUR..MDEMO` for the DEMO MOA). For longer names, the name may actually be truncated. The Tombstone MOA, for example, is truncated as `TOMBSTON A`, `TOMBSTON B` and `TOMBSTON C`.

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
