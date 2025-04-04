## Text Defaults

The Text Defaults object roughly follows the Properties object for the Text element in the
[vNAS Documentation](https://data-admin.vnas.vatsim.net/docs/#/video-maps?id=text).

The Text Defaults object has the following properties:

| Property    | Required | Type    | Default       | Description                                                      |
| ----------- | -------- | ------- | ------------- | ---------------------------------------------------------------- |
| `bcg`       | \*       | `int`   |               | An integer value representing the associated BCG.                |
| `filters`   | \*       | `array` |               | An array of integer values representing the associated filters.  |
| `text`      |          | `array` | `CRC Default` | An array of string values representing the default text value.   |
| `size`      |          | `int`   | `CRC Default` | An integer value representing the text size between `0` and `5`. |
| `underline` |          | `bool`  | `CRC Default` | A boolean value that toggles an underline of the text.           |
| `x_offset`  |          | `int`   | `CRC Default` | An integer value representing the x offset.                      |
| `y_offset`  |          | `int`   | `CRC Default` | An integer value representing the y offset.                      |
| `opaque`    |          | `bool`  | `CRC Default` | A boolean value that toggles an opaque background for the text.  |

NOTE: `CRC Default` means that not providing the value will result in the default CRC behavior.

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
