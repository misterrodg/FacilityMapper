## ERAM Procedure

Procedures encompass SIDs, STARs, and IAPs. Each is made up of a core segment, along with leading, trailing, or both segments.
For example, a SID might have a leading segment of runway transitions to the core, the core itself, and then a trailing segment
of en route transitions. A STAR a leading segment of en route transitions, the core itself, and then a trailing segment of runway
transitions. An IAP has a leading segment of transitions, and the core itself.

The interpretation of the paths is still relatively limited. As such, more advanced draws like those on RTF legs are not yet supported.

The ERAM Procedure object has the following properties:

| Property               | Required | Type     | Default                               | Description                                                                                                                                                               |
| ---------------------- | -------- | -------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `airport_id`           | \*       | `string` |                                       | A string representing the ICAO identifier for the airport.                                                                                                                |
| `procedure_type`       | \*       | `string` |                                       | A string representing the procedure type: `"SID"`, `"STAR"` or `"IAP"`.                                                                                                   |
| `procedure_id`         | \*       | `string` |                                       | A string representing the computer code of the procedure. These aren't always straightforward. See [ICAO IAP Codes](#icao-iap-codes) for more detail.                     |
| `draw_names`           |          | `bool`   | `false`                               | A boolean value that tells the script to draw the name of the fix near the fix location.                                                                                  |
| `draw_altitudes`       |          | `bool`   | `false`                               | A boolean value that tells the script to draw the speed restriction (if present) for the fix near the fix location.                                                       |
| `draw_speeds`          |          | `bool`   | `false`                               | A boolean value that tells the script to draw the altitude restriction(s) (if present) for the fix near the fix location.                                                 |
| `draw_symbols`         |          | `bool`   | `false`                               | A boolean value that tells the script to draw a symbol at the fix location. The symbol is driven by the data in the .                                                     |
| `draw_lines`           |          | `bool`   | `true`                                | A boolean value that tells the script to draw lines along the procedure.                                                                                                  |
| `truncation`           |          | `float`  |                                       | A float value that tells the script to truncate lines around each point by the value in nautical miles. Generally only useful if using the solid line style with symbols. |
| `leading_transitions`  |          | `array`  |                                       | An array of strings representing the names of the transitions to include. `"ALL"` is available instead of writing each, individually.                                     |
| `suppress_core`        |          | `bool`   | `false`                               | A boolean value that tells the script to suppress the core segment.                                                                                                       |
| `trailing_transitions` |          | `array`  |                                       | An array of strings representing the names of the transitions to include. `"ALL"` is available instead of writing each, individually.                                     |
| `append_name`          |          | `string` |                                       | A string representing the location where the procedure name should be appended: `"leading"`, `"core"`, or `"trailing"`.                                                   |
| `line_defaults`        | \*\*     | `object` |                                       | A [Line Defaults](./LINE_DEFAULTS.md) object. Required when `draw_lines` is `true`. (Note that `draw_lines` is `true` by default.)                                        |
| `symbol_defaults`      | \*\*     | `object` |                                       | A [Symbol Defaults](./SYMBOL_DEFAULTS.md) object. Required when `draw_symbols` is `true`.                                                                                 |
| `text_defaults`        | \*\*     | `object` |                                       | A [Text Defaults](./TEXT_DEFAULTS.md) object. Required when `draw_names`, `draw_altitudes`, or `draw_speeds` is `true`.                                                   |
| `file_name`            |          | `string` | `{airportId}_{mapType}_{procedureId}` | A string representing the filename that the map will be saved to (`"KRDU_STAR_ALDAN"`).                                                                                   |

### ICAO IAP Codes

| Prefix | Type    | Example      |
| ------ | ------- | ------------ |
| B      | LOC/BC  | `B30L`       |
| D      | VOR/DME | `D25`        |
| F      | FMS     | _Deprecated_ |
| G      | IGS     | _Deprecated_ |
| H      | RNP     | `H21-Y`      |
| I      | ILS     | `I01R`       |
| J      | GNSS    | _Deprecated_ |
| L      | LOC     | `L17`        |
| M      | MLS     | _Deprecated_ |
| N      | NDB     | `N34`        |
| P      | GPS     | `P04`        |
| Q      | NDB/DME | `Q06R`       |
| R      | RNAV    | `R14`        |
| S      | VORTAC  | `S13`        |
| T      | TACAN   | _Deprecated_ |
| U      | SDF     | _Deprecated_ |
| V      | VOR     | `V22`        |
| W      | MLS-A   | _Deprecated_ |
| X      | LDA     | `X19-Y`      |
| Y      | MLS-B/C | _Deprecated_ |

...and because the CIFP is an FAA product, these additional oddities that seem to be specific to procedures not tied to a specific runway:

| Prefix | Type    | Example |
| ------ | ------- | ------- |
| GPS    | GPS     | `GPS-A` |
| LBC    | LOC/BC  | `LBC-A` |
| LDA    | LDA     | `LDA-A` |
| LOC    | LOC     | `LOC-A` |
| NDB    | NDB     | `NDB-A` |
| RNV    | RNAV    | `RNV-A` |
| VDM    | VOR/DME | `VDM-A` |
| VOR    | VOR     | `VOR-A` |

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
