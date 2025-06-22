## STARS Procedure

Procedures encompass SIDs, STARs, and IAPs. Each is made up of a core segment, along with leading, trailing, or both segments.
For example, a SID might have a leading segment of runway transitions to the core, the core itself, and then a trailing segment
of en route transitions. A STAR a leading segment of en route transitions, the core itself, and then a trailing segment of runway
transitions. An IAP has a leading segment of transitions, and the core itself.

The interpretation of the paths is still relatively limited. As such, more advanced draws like those on RTF legs are not yet supported.

The STARS Procedure object has the following properties:

| Property               | Required | Type     | Default                               | Description                                                                                                                                                          |
| ---------------------- | -------- | -------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `airport_id`           | \*       | `string` |                                       | A string representing the ICAO identifier for the airport.                                                                                                           |
| `procedure_type`       | \*       | `string` |                                       | A string representing the procedure type: `"SID"`, `"STAR"` or `"IAP"`.                                                                                              |
| `procedure_id`         | \*       | `string` |                                       | A string representing the computer code of the procedure. These aren't always straightforward. See [ICAO IAP Codes](#icao-iap-codes) for more detail.                |
| `draw_names`           |          | `bool`   | `false`                               | A boolean value that tells the script to draw the name of the fix near the fix location.                                                                             |
| `draw_altitudes`       |          | `bool`   | `false`                               | A boolean value that tells the script to draw the speed restriction (if present) for the fix near the fix location.                                                  |
| `draw_speeds`          |          | `bool`   | `false`                               | A boolean value that tells the script to draw the altitude restriction(s) (if present) for the fix near the fix location.                                            |
| `draw_symbols`         |          | `bool`   | `false`                               | A boolean value that tells the script to draw a symbol at the fix location. The symbol is driven by the data in the .                                                |
| `line_type`            |          | `string` | `"solid"`                             | A string representing the line type that should be drawn. Supported line types are: `"solid"`, `"longDashed"`, `"shortDashed"`, `"longDashShortDash"`, and `"none"`. |
| `x_offset`             |          | `float`  | `0`                                   | A float value representing the lateral text offset in nautical miles (positive for East and negative for West).                                                      |
| `y_offset`             |          | `float`  | `0`                                   | A float value representing the vertical text offset in nautical miles (positive for North and negative for South).                                                   |
| `symbol_scale`         |          | `float`  | `1.0`                                 | A float value representing the scale of the symbols.                                                                                                                 |
| `text_scale`           |          | `float`  | `1.0`                                 | A float value representing the scale of the text.                                                                                                                    |
| `line_height`          |          | `float`  | `1.5` \* `text_scale`                 | A float value representing the line height of the text, used in spacing the fix name, altitude, and speed.                                                           |
| `leading_transitions`  |          | `array`  |                                       | An array of strings representing the names of the transitions to include. `"ALL"` is available instead of writing each, individually.                                |
| `trailing_transitions` |          | `array`  |                                       | An array of strings representing the names of the transitions to include. `"ALL"` is available instead of writing each, individually.                                |
| `draw_missed`          |          | `bool`   | `false`                               | A boolean value that tells the script to draw the missed approach. (Generally functional but not recommended for use.)                                               |
| `file_name`            |          | `string` | `{airportId}_{mapType}_{procedureId}` | A string representing the filename that the map will be saved to (`"KRDU_STAR_ALDAN"`).                                                                              |

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
