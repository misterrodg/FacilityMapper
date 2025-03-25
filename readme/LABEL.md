## Label

The Label object has the following properties:

| Property    | Required | Type     | Default | Description                                                       |
| ----------- | -------- | -------- | ------- | ----------------------------------------------------------------- |
| `lines`     | \*       | `array`  |         | An array of [Label Line](#label-line) objects.                    |
| `file_name` | \*       | `string` |         | A string representing the filename that the map will be saved to. |

### Label Line

The Label Line object has the following properties:

| Property     | Required | Type     | Default | Description                                                   |
| ------------ | -------- | -------- | ------- | ------------------------------------------------------------- |
| `line`       | \*       | `string` |         | A text line of [supported characters](#supported-characters). |
| `lat`        | \*       | `float`  |         | A float value representing the latitude.                      |
| `lon`        | \*       | `float`  |         | A float value representing the longitude.                     |
| `text_scale` |          | `float`  | `1.0`   | A float value representing the scale of the text.             |

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
