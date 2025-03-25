## Manifest

Manifest files define what maps are drawn for a specific purpose. This can be a "global" manifest file (a `manifest.json` file in the project root), or a "targeted" manifest file (a `{name}.json` file in the `./manifests` directory). For example, to make it easier to manage facilities one could set up manifest files in the `./manifests` directory with the names `pct.json` and `rdu.json`, each with the maps for their respective TRACONs. These can then be called as necessary by running `python3 main.py --manifest pct.json` and `python3 main.py --manifest rdu.json`.

All manifest files have the following property:

| Property | Required | Type    | Default | Description                                  |
| -------- | -------- | ------- | ------- | -------------------------------------------- |
| `maps`   | \*       | `array` |         | An array of [Map Objects](./MAP_OBJECTS.md). |

[Back to README](../README.md)
