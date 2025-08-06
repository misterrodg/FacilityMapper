## Map Objects

Map Objects define the type of map to be drawn.

The map object has the following properties:

| Property           | Required | Type     | Default | Description                                                   |
| ------------------ | -------- | -------- | ------- | ------------------------------------------------------------- |
| `map_type`         | \*       | `string` |         | A string representing the [Map Type](#map-types).             |
| `definition`       | \*       | `object` |         | A Definition Object as defined by the [Map Type](#map-types). |
| `stars_definition` |          | `object` |         | A [STARS Definition Object](./STARS_DEFINITION_OBJECT.md).    |

### Map Types

The types are relatively straightforward. To view the Definition for the Map Type, click on the Map Type name.

| Map Type                                | Description                                                                     |
| --------------------------------------- | ------------------------------------------------------------------------------- |
| [CENTERLINES](./CENTERLINES.md)         | Creates a map of centerlines for a specific airport.                            |
| [CONTROLLED](./CONTROLLED.md)           | Creates a map of controlled airspace for a specific airport.                    |
| [ERAM PROCEDURE](./ERAM_PROCEDURE.md)   | Creates a map of a specific Procedure (SID, STAR, or IAP) as an ERAM map.       |
| [STARS PROCEDURE](./STARS_PROCEDURE.md) | Creates a map of a specific Procedure (SID, STAR, or IAP) as a STARS map.       |
| [LABEL](./LABEL.md)                     | Creates a map with labels at specific locations. (DEPRECATED)                   |
| [LABELS](./LABELS.md)                   | Creates a map with multiline labels at specific locations.                      |
| [ERAM VOR](./ERAM_VOR.md)               | Creates a map with the specified VORs.                                          |
| [PLACEHOLDER](./PLACEHOLDER.md)         | A placeholder "map" for use with STARS Definitions.                             |
| [RESTRICTIVE](./RESTRICTIVE.md)         | Creates a map of restrictive airspace (Restricted, MOA, Warning, etc.) by name. |
| [RUNWAYS](./RUNWAYS.md)                 | Creates a map of runway lines for the specified airports.                       |
| [VECTORSID](./VECTORSID.md)             | Creates a map of a specific vector SID.                                         |
| [COMPOSITE](./COMPOSITE.md)             | Creates a combined map of existing maps.                                        |

[Back to README](../README.md)
