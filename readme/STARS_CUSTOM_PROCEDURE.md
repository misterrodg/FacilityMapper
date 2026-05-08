## STARS Custom Procedure

STARS Custom Procedures are a variation of [STARS Procedure](./STARS_PROCEDURE.md).
While [STARS Procedure](./STARS_PROCEDURE.md) builds SIDs, STARs, and IAPs from the
database, STARS Custom Procedure is a "manual" draw of a given procedure, useful in
cases where a military, or proprietary procedure is not in the FAA CIFP data.

Just like [STARS Procedure](./STARS_PROCEDURE.md), the procedure has leading and
trailing segments, along with a core segment. The core itself is an array of type
[Procedure Point](./PROCEDURE_POINT.md). Because the leading and trailing segments
may have multiple segments, the leading and trailing segments are an array of an
array of [Procedure Point](./PROCEDURE_POINT.md). Points must be provided in
sequential order.

While the CIFP/ARINC424 standard defines each transition fully on its own, this is
not required in a custom procedure. Simply define it until the transition joins an
existing defined path.

NOTE: If you're looking at a NACO/FAA Chart, the core is the bold line style, and
transitions are all a thin line style.

The STARS Custom Procedure object has the following properties:

| Property            | Required | Type     | Default               | Description                                                                                                                                                          |
| ------------------- | -------- | -------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `procedure_type`    | \*       | `string` |                       | A string representing the procedure type: `"SID"`, `"STAR"` or `"IAP"`.                                                                                              |
| `draw_names`        |          | `bool`   | `false`               | A boolean value that tells the script to draw the name of the fix near the fix location.                                                                             |
| `draw_altitudes`    |          | `bool`   | `false`               | A boolean value that tells the script to draw the altitude restriction(s) (if present) for the fix near the fix location.                                            |
| `draw_speeds`       |          | `bool`   | `false`               | A boolean value that tells the script to draw the speed restriction (if present) for the fix near the fix location.                                                  |
| `draw_symbols`      |          | `bool`   | `false`               | A boolean value that tells the script to draw a symbol at the fix location.                                                                                          |
| `line_type`         |          | `string` | `"solid"`             | A string representing the line type that should be drawn. Supported line types are: `"solid"`, `"longDashed"`, `"shortDashed"`, `"longDashShortDash"`, and `"none"`. |
| `x_offset`          |          | `float`  | `0`                   | A float value representing the lateral text offset in nautical miles (positive for East and negative for West).                                                      |
| `y_offset`          |          | `float`  | `0`                   | A float value representing the vertical text offset in nautical miles (positive for North and negative for South).                                                   |
| `symbol_scale`      |          | `float`  | `1.0`                 | A float value representing the scale of the symbols.                                                                                                                 |
| `text_scale`        |          | `float`  | `1.0`                 | A float value representing the scale of the text.                                                                                                                    |
| `line_height`       |          | `float`  | `1.5` \* `text_scale` | A float value representing the line height of the text, used in spacing the fix name, altitude, and speed.                                                           |
| `leading_segments`  |          | `array`  |                       | An array of arrays of [Procedure Point](./PROCEDURE_POINT.md) objects.                                                                                               |
| `core_segment`      | \*       | `array`  |                       | An array of [Procedure Point](./PROCEDURE_POINT.md) objects.                                                                                                         |
| `trailing_segments` |          | `array`  |                       | An array of arrays of [Procedure Point](./PROCEDURE_POINT.md) objects.                                                                                               |
| `append_name`       |          | `string` |                       | SID/STAR only: Append the procedure name to fix labels in the `"leading"`, `"core"`, or `"trailing"` segment.                                                        |
| `vector_length`     |          | `float`  | `2.5`                 | A float value representing the length of the vector line drawn at the end of a procedure leg in nautical miles.                                                      |
| `file_name`         | \*       | `string` |                       | A string representing the filename that the map will be saved to (`"KRDU_STAR_ALDAN"`).                                                                              |

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
