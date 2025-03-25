## Label

The Label object has the following properties:

| Property    | Required | Type     | Default | Description                                                       |
| ----------- | -------- | -------- | ------- | ----------------------------------------------------------------- |
| `labels`    | \*       | `array`  |         | An array of [Label Lines](#label-lines) objects.                  |
| `file_name` | \*       | `string` |         | A string representing the filename that the map will be saved to. |

### Label Lines

The Label Lines object has the following properties:

| Property      | Required | Type     | Default               | Description                                                                                                        |
| ------------- | -------- | -------- | --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `lines`       | \*       | `string` |                       | A text line of [supported characters](#supported-characters).                                                      |
| `lat`         | \*       | `float`  |                       | A float value representing the latitude.                                                                           |
| `lon`         | \*       | `float`  |                       | A float value representing the longitude.                                                                          |
| `x_offset`    |          | `float`  | `0`                   | A float value representing the lateral text offset in nautical miles (positive for East and negative for West).    |
| `y_offset`    |          | `float`  | `0`                   | A float value representing the vertical text offset in nautical miles (positive for North and negative for South). |
| `text_scale`  |          | `float`  | `1.0`                 | A float value representing the scale of the text.                                                                  |
| `line_height` |          | `float`  | `1.5` \* `text_scale` | A float value representing the line height of the text, used in spacing the fix name, altitude, and speed.         |

NOTE: The "origin" of the text is at the bottom left corner.

### Supported Characters

The following characters are currently supported:

| Type    | Supported                                                                                               |
| ------- | ------------------------------------------------------------------------------------------------------- |
| Numeric | `0`,`1`,`2`,`3`,`4`,`5`,`6`,`7`,`8`,`9`                                                                 |
| Alpha   | `A`,`B`,`C`,`D`,`E`,`F`,`G`,`H`,`I`,`J`,`K`,`L`,`M`,`N`,`O`,`P`,`Q`,`R`,`S`,`T`,`U`,`V`,`W`,`X`,`Y`,`Z` |
| Other   | `+`,`-`,`.`,`⎵` (space)                                                                                 |

What the characters look like is shown in [EXAMPLES](../examples/EXAMPLES.md#label-supported-characters).

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
