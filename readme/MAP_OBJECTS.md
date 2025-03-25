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

| Map Type                        | Description                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------- |
| [CENTERLINES](./CENTERLINES.md) | Creates a map of centerlines for a specific airport.                              |
| [CONTROLLED](./CONTROLLED.md)   | Creates a map of controlled airspace for a specific airport.                      |
| [IAP](./IAP.md)                 | Creates a map of a specific Instrument Approach Procedure.                        |
| [LABEL](./LABEL.md)             | Creates a map with labels at specific locations. (DEPRECATED)                     |
| [LABELS](./LABELS.md)           | Creates a map with multiline labels at specific locations.                        |
| [RESTRICTIVE](./RESTRICTIVE.md) | Creates a map of restrictive airspace (Restricted, MOA, Warning, etc.) by name.   |
| [RUNWAYS](./RUNWAYS.md)         | Creates a map of runway lines for the specified airports.                         |
| [SID](./SIDSTAR.md#sid)         | Creates a map of a specific (non-vector) Standard Instrument Departure procedure. |
| [VECTORSID](./VECTORSID.md)     | Creates a map of a specific vector SID.                                           |
| [STAR](./SIDSTAR.md#star)       | Creates a map of a specific Standard Terminal Arrival procedure.                  |
| [COMPOSITE](./COMPOSITE.md)     | Creates a combined map of existing maps.                                          |

[Back to README](../README.md)
