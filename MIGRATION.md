# Migration from 1.x to 2.0

Version 2.0 updates `FacilityMapper` to work with `cifparse` v2 and streamlines the procedure handling in STARS maps.

## Steps to Update

- Upgrade `cifparse` with `pip install --upgrade cifparse`.
- Update this repository with `git pull`.
- Find all of your existing maps with map types `IAP`, `SID`, and `STAR`.
- Copy this type into the definition of the map as a `"procedure_type"` field.
- Change all of these map types to `STARS PROCEDURE`.

### Example

Change the following:

```json
{
  "map_type": "SID",
  "definition": {
    "airport_id": "KDCA",
    "procedure_id": "AMEEE#",
    "file_name": "PCT_DCA_SID_AMEEE"
  }
}
```

...to:

```json
{
  "map_type": "STARS PROCEDURE",
  "definition": {
    "airport_id": "KDCA",
    "procedure_type": "SID",
    "procedure_id": "AMEEE#",
    "file_name": "PCT_DCA_SID_AMEEE"
  }
}
```
