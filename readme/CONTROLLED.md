## Controlled

The Controlled object has the following properties:

| Property     | Required | Type     | Default                    | Description                                                       |
| ------------ | -------- | -------- | -------------------------- | ----------------------------------------------------------------- |
| `airport_id` | \*       | `string` |                            | A string representing the identifier for the controlled airspace. |
| `file_name`  |          | `string` | `{mapType}_{controlledId}` | A string representing the filename that the map will be saved to. |

**NOTE**: For most airspace, the `airport_id` is straightforward, but for certain areas within Class B, it might not be obvious. It may be worth opening the CIFP file and searching for the entry. If your program supports regex, you can search with `SUSAUC...{airportId}` to see if anything pops up. For Washington DC, the Class B is centered on `KDCA` (and not `KIAD` or `KBWI`), whereas for NY it is centered on `KJFK` (and not `KEWR` or `KLGA`).

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
