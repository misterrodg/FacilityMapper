## STARS Definition Objects

When managing larger facilities, the map list can exceed the available display area. In these circumstances,
it is necessary to provide a map list to controllers by other means. Additionally, this method helps in adding
or auditing the list in Data Admin.

NOTE: This definition only sets the creation of a textual map list for controllers. STARS Video Maps must be configured in Data Admin.

The STARS Definition object has the following properties:

| Property              | Required | Type     | Default           | Description                                                     |
| --------------------- | -------- | -------- | ----------------- | --------------------------------------------------------------- |
| `name`                | \*       | `string` |                   | A string value representing the Map Name.                       |
| `map_id`              |          | `int`    | `{last_used + 1}` | An integer value representing the Map ID.                       |
| `short_name`          |          | `string` | `{name}`          | A string value representing the Short Map Name (for STARS DCB). |
| `brightness_category` |          | `char`   | `A`               | A character value representing the STARS Brightness Category.   |
| `tdm_only`            |          | `bool`   | `False`           | A boolean value that restricts the map visibility to TDM only.  |
| `always_visible`      |          | `bool`   | `False`           | A boolean value that forces TDM maps to be always visible.      |
| `note`                |          | `string` | `""`              | A string value representing a note to controllers.              |

NOTE: For the `map_id` values, be sure you are providing unique IDs. There is no verification of uniqueness in the code.
If no `map_id`s are provided, then the code will assign them in the order they are provided in the manifest.
If only the first `map_id` is provided, then the code will start at that ID and increment by one from there.
If all maps have `map_id`s, the code will use those IDs exactly as provided.
If providing only some map IDs, use care to ensure the maps are ordered properly. If not, the code will not properly handle the IDs.

The following **example of what not to do** would cause the Map IDs to be `201, 202, 200, 201`:

```json
    ...
    "stars_definition": {
        "map_id": 201,
        "short_name": "CAPSS",
        "name": "DCA STAR CAPSS"
    },
    ...
    "stars_definition": {
        "short_name": "CLIPR",
        "name": "DCA STAR CLIPR"
    },
    ...
    "stars_definition": {
        "map_id": 200,
        "short_name": "TIKEE",
        "name": "DCA STAR TIKEE"
    },
    ...
    "stars_definition": {
        "short_name": "TRUPS",
        "name": "DCA STAR TRUPS",
    }
```

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
