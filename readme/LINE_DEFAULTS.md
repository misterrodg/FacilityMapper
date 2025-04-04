## Line Defaults

The Line Defaults object roughly follows the Properties object for the Line element in the
[vNAS Documentation](https://data-admin.vnas.vatsim.net/docs/#/video-maps?id=line).

The Line Defaults object has the following properties:

| Property    | Required | Type     | Default       | Description                                                                                               |
| ----------- | -------- | -------- | ------------- | --------------------------------------------------------------------------------------------------------- |
| `bcg`       | \*       | `int`    |               | An integer value representing the associated BCG.                                                         |
| `filters`   | \*       | `array`  |               | An array of integer values representing the associated filters.                                           |
| `style`     |          | `string` | `CRC Default` | A string representing the line type: `"solid"`, `"shortDashed"`, `"longDashed"`, or `"longDashShortDash"` |
| `thickness` |          | `int`    | `CRC Default` | An integer value representing the line thickness between `1` and `3`.                                     |

NOTE: `CRC Default` means that not providing the value will result in the default CRC behavior.

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
