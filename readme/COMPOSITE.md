## Composite

A Composite Map is a map made up of other maps. This is useful in cases where you would like to show several SIDs, or to display all controlled airspace on a single map. Any map that is created can be combined with another should you wish to do so.

As best practice, all Composites should be listed at the end of the manifest to ensure that the relevant maps are generated before trying to combine them.

The Composite object has the following properties:

| Property           | Required | Type     | Default | Description                                                                             |
| ------------------ | -------- | -------- | ------- | --------------------------------------------------------------------------------------- |
| `file_names`       | \*       | `string` |         | A string representing the filenames to combine into a single map.                       |
| `file_name`        | \*       | `string` |         | A string representing the filename that the map will be saved to.                       |
| `delete_originals` |          | `bool`   | `false` | A boolean value that tells the script to delete the original maps after combining them. |

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
