## ERAM VOR

The ERAM VOR object has the following properties:

| Property          | Required | Type     | Default | Description                                                                               |
| ----------------- | -------- | -------- | ------- | ----------------------------------------------------------------------------------------- |
| `vor_ids`         | \*       | `array`  |         | An array of string values representing the identifiers for the desired VORs.              |
| `draw_symbols`    |          | `bool`   | `true`  | A boolean value that tells the script to draw a symbol at the VOR location.               |
| `draw_text`       |          | `bool`   | `false` | A boolean value that tells the script to draw text next to the symbol.                    |
| `symbol_defaults` | \*\*     | `object` |         | A [Symbol Defaults](./SYMBOL_DEFAULTS.md) object. Required when `draw_symbols` is `true`. |
| `text_defaults`   | \*\*     | `object` |         | A [Text Defaults](./TEXT_DEFAULTS.md) object. Required when `draw_text` is `true`.        |
| `file_name`       | \*       | `string` |         | A string representing the filename that the map will be saved to (`"ZDC_VOR_ERAM"`).      |

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
