## Controlled

The Controlled object has the following properties:

| Property     | Required | Type     | Default                    | Description                                                       |
| ------------ | -------- | -------- | -------------------------- | ----------------------------------------------------------------- |
| `airport_id` | \*       | `string` |                            | A string representing the identifier for the controlled airspace. |
| `file_name`  |          | `string` | `{mapType}_{controlledId}` | A string representing the filename that the map will be saved to. |

**NOTE**: For most airspace, the `airport_id` is straightforward, but for certain areas within Class B, it might not be obvious.
Consider using the [FIND](./FIND.md) function if you are unsure.

**NOTE**: Some airports have conditional Class C airspace, which means that the airport will have both Class C and Class D airspace records.
If both types are found for a specific airport, the script will generate one file with the specified file name adding a suffix of `_C`,
and another with the specified file name adding a suffix of `_D`.

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
