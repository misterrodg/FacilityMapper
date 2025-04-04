## Symbol Defaults

The Symbol Defaults object roughly follows the Properties object for the Symbol element in the
[vNAS Documentation](https://data-admin.vnas.vatsim.net/docs/#/video-maps?id=symbol).

The Symbol Defaults object has the following properties:

| Property  | Required | Type     | Default       | Description                                                                                                                                                                                                                                                                                              |
| --------- | -------- | -------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bcg`     | \*       | `int`    |               | An integer value representing the associated BCG.                                                                                                                                                                                                                                                        |
| `filters` | \*       | `array`  |               | An array of integer values representing the associated filters.                                                                                                                                                                                                                                          |
| `size`    |          | `int`    | `CRC Default` | An integer value representing the symbol size between `1` and `4`.                                                                                                                                                                                                                                       |
| `style`   |          | `string` | `CRC Default` | A string representing the symbol type: `"obstruction1"`, `"obstruction2"`, `"heliport"`, `"nuclear"`, `"emergencyAirport"`, `"radar"`, `"iaf"`, `"rnavOnlyWaypoint"`, `"rnav"`, `"airwayIntersections"`, `"ndb"`, `"vor"`, `"otherWaypoints"`, `"airport"`, `"satelliteAirport"`, `"tacan"`, or `"dme"`. |

NOTE: `CRC Default` means that not providing the value will result in the default CRC behavior.

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
