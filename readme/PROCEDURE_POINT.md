## Procedure Point

Procedure Points are defined points along a SID, STAR, or IAP. This type
handles both user-defined and database-defined data and has no defaults.
As a result, the `Default` column (usually column 4) has been replaced by
`DB Only` for data that is generally only provided by the database. You
may enter data in this field, but doing so would require understanding
the CIFP/ARINC424 standard in depth.

The Procedure Point object has the following properties:

| Property         | Required | Type     | DB Only | Description                                                                                                  |
| ---------------- | -------- | -------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| `fix_id`         | \*       | `string` |         | A string representing the fix id.                                                                            |
| `fix_lat`        | \*       | `float`  |         | A float representing the fix latitude.                                                                       |
| `fix_lon`        | \*       | `float`  |         | A float representing the fix longitude.                                                                      |
| `fix_source`     |          | `string` | \*      | A string representing the source of the point (the table on which it is found).                              |
| `fix_type`       |          | `string` | \*      | A string representing the type of fix.                                                                       |
| `fix_mag_var`    |          | `float`  |         | A float representing the magnetic variation at that point.                                                   |
| `symbol_name`    |          | `string` |         | A string representing the [Symbol Type](#symbol-types).                                                      |
| `procedure_id`   |          | `string` |         | A string representing the procedure ID.                                                                      |
| `procedure_type` |          | `string` | \*      | A string representing the procedure type.                                                                    |
| `fac_sub_code`   |          | `string` | \*      | A string representing the facility subsection code.                                                          |
| `transition_id`  |          | `string` | \*      | A string representing the transition ID.                                                                     |
| `seq_no`         |          | `int`    | \*      | An integer representing the sequence number.                                                                 |
| `path_term`      |          | `string` | \*      | A string representing the path termination.                                                                  |
| `course`         |          | `float`  | \*      | A float representing the course.                                                                             |
| `center_fix`     |          | `string` | \*      | A string representing the fix used for a radius-to-fix leg.                                                  |
| `center_lat`     |          | `float`  | \*      | A float representing the latitude of the centerpoint for the radius.                                         |
| `center_lon`     |          | `float`  | \*      | A float representing the longitude of the centerpoint for the radius.                                        |
| `arc_radius`     |          | `float`  | \*      | A float representing the length of the radius.                                                               |
| `turn_direction` |          | `string` | \*      | A string representing the turn direction.                                                                    |
| `desc_code`      |          | `string` | \*      | A string representing the description code.                                                                  |
| `alt_desc`       |          | `string` |         | A string representing the altitude descriptor: `+` (above), `-` (below), `B` (both/between), `[blank]` (at). |
| `alt_1`          |          | `int`    |         | An integer representing the first altitude.                                                                  |
| `fl_1`           |          | `bool`   |         | A bool representing the first altitude as a FL.                                                              |
| `alt_2`          |          | `int`    |         | An integer representing the second altitude.                                                                 |
| `fl_2`           |          | `bool`   |         | A bool representing the second altitude as a FL.                                                             |
| `speed_desc`     |          | `string` |         | A string representing the speed descriptor: `+` (above), `-` (below), `[blank]` (at).                        |
| `speed_limit`    |          | `int`    |         | An integer representing the speed.                                                                           |

### Symbol Types

| Type         | Description                        |
| ------------ | ---------------------------------- |
| `FAF`        | Final Approach Fix (Maltese Cross) |
| `RNAV_POINT` | RNAV Point (Four-Point Star)       |
| `WAYPOINT`   | Waypoint (Triangle)                |
| `VORDME`     | VOR/DME (Hexagon with Box)         |
| `VORTAC`     | VORTAC (Hexagon with Box)          |
| `VOR`        | VOR (Hexagon)                      |
| `DME`        | DME (Box)                          |
| `NDB`        | NDB (Circle)                       |
