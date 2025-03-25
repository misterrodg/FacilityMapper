## Vector SID

Vectored SIDs don't have any specific path information, so it is being offered as a special type in cases where the map is still desired. Unlike the SID and STAR types, the Vector SID does not print any path information, and defaults to printing the symbols and names.

The Vector SID object has the following properties:

| Property       | Required | Type     | Default                               | Description                                                                                                                                           |
| -------------- | -------- | -------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `airport_id`   | \*       | `string` |                                       | A string representing the ICAO identifier for the airport.                                                                                            |
| `procedure_id` | \*       | `string` |                                       | A string representing the computer code of the procedure, in the format `"AAA#"` or `"AAAAA#"` (`"JCOBY#"`), where the `#` is the literal `#` symbol. |
| `draw_symbols` |          | `bool`   | `true`                                | A boolean value that tells the script to draw a symbol at the fix location. The symbol is driven by the data in the CIFP.                             |
| `symbol_scale` |          | `float`  | `1.0`                                 | A float value representing the scale of the symbols.                                                                                                  |
| `draw_names`   |          | `bool`   | `true`                                | A boolean value that tells the script to draw the name of the fix near the fix location.                                                              |
| `x_offset`     |          | `float`  | `0`                                   | A float value representing the lateral text offset in nautical miles (positive for East and negative for West).                                       |
| `y_offset`     |          | `float`  | `0`                                   | A float value representing the vertical text offset in nautical miles (positive for North and negative for South).                                    |
| `text_scale`   |          | `float`  | `1.0`                                 | A float value representing the scale of the text.                                                                                                     |
| `line_height`  |          | `float`  | `1.5` \* `text_scale`                 | A float value representing the line height of the text, used in spacing the fix name, altitude, and speed.                                            |
| `file_name`    |          | `string` | `{airportId}_{mapType}_{procedureId}` | A string representing the filename that the map will be saved to (`"003_CPTAL"`).                                                                     |

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
