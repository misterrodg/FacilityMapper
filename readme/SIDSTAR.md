## SID and STAR

### SID

The SID object has the following properties:

| Property                   | Required | Type     | Default                               | Description                                                                                                                                                                                                                                |
| -------------------------- | -------- | -------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `airport_id`               | \*       | `string` |                                       | A string representing the ICAO identifier for the airport.                                                                                                                                                                                 |
| `procedure_id`             | \*       | `string` |                                       | A string representing the computer code of the procedure, in the format `"AAA#"` or `"AAAAA#"` (`"JCOBY#"`), where the `#` is the literal `#` symbol.                                                                                      |
| `line_type`                |          | `string` | `"solid"`                             | A string representing the line type that should be drawn. Supported line types are: `"solid"`, `"longDashed"`, `"shortDashed"`, `"longDashShortDash"`, `"arrows"`, and `"none"`.                                                           |
| `draw_symbols`             |          | `bool`   | `false`                               | A boolean value that tells the script to draw a symbol at the fix location. The symbol is driven by the data in the CIFP, and clips the line around the point.                                                                             |
| `symbol_scale`             |          | `float`  | `1.0`                                 | A float value representing the scale of the symbols.                                                                                                                                                                                       |
| `draw_altitudes`           |          | `bool`   | `false`                               | A boolean value that tells the script to draw the altitude restriction(s) (if present) for the fix near the fix location.                                                                                                                  |
| `draw_speeds`              |          | `bool`   | `false`                               | A boolean value that tells the script to draw the speed restriction(s) (if present) for the fix near the fix location.                                                                                                                     |
| `draw_names`               |          | `bool`   | `false`                               | A boolean value that tells the script to draw the name of the fix near the fix location.                                                                                                                                                   |
| `x_offset`                 |          | `float`  | `0`                                   | A float value representing the lateral text offset in nautical miles (positive for East and negative for West).                                                                                                                            |
| `y_offset`                 |          | `float`  | `0`                                   | A float value representing the vertical text offset in nautical miles (positive for North and negative for South).                                                                                                                         |
| `text_scale`               |          | `float`  | `1.0`                                 | A float value representing the scale of the text.                                                                                                                                                                                          |
| `line_height`              |          | `float`  | `1.5` \* `text_scale`                 | A float value representing the line height of the text, used in spacing the fix name, altitude, and speed.                                                                                                                                 |
| `draw_enroute_transitions` |          | `bool`   | `true`                                | A boolean value that tells the script to draw the enroute transitions.                                                                                                                                                                     |
| `draw_runway_transitions`  |          | `bool`   | `false`                               | A boolean value that tells the script to draw the runway transitions. NOTE: Many SID runway transitions have performance/altitude-based points. These are not currently supported, so the line draws might be odd in this segment for now. |
| `file_name`                |          | `string` | `{airportId}_{mapType}_{procedureId}` | A string representing the filename that the map will be saved to (`"003_JCOBY"`).                                                                                                                                                          |

### STAR

The STAR object is defined using the same properties as [SID](#sid). |

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
