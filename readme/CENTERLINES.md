## Centerlines

The Centerlines Map Type allows you to draw one or multiple centerlines in a single map as a way to create maps for specific runway configurations.

The Centerlines object has the following properties:

| Property      | Required | Type     | Default | Description                                                       |
| ------------- | -------- | -------- | ------- | ----------------------------------------------------------------- |
| `airport_id`  | \*       | `string` |         | A string representing the identifier for the airport.             |
| `centerlines` | \*       | `array`  |         | An array of [Centerline](#centerline) objects.                    |
| `file_name`   | \*       | `string` |         | A string representing the filename that the map will be saved to. |

### Centerline

The Centerline object defines how a specific centerline is drawn. Centerline draws have various oddities that are noted here:

- A basic centerline can be drawn simply by specifying a `runway_id`, which will draw a `10.0` nautical mile centerline along the runway bearing.
  - The default length can be overridden with `length`.
- Specifying a `selected_iap` will add crossbars for any fixes between the IF and the runway.
  - If the IF is further than the default or manually specified length, the length will be overridden to accommodate the distance to the IF.
- Specifying a `selected_transition` will add crossbars for any fix from that transition (IAF) to the IF.
  - If the IAF is further than the default or manually specified length, the length will be overridden to accommodate the distance to the IAF.
  - Only select transitions that are along the localizer course, otherwise you will have lines off of the centerline.
- Specifying a `selected_loc` is an option to draw a basic centerline along the specified localizer course.
  - Use this option only if you want a basic centerline that follows a localizer offset, and don't need crossbars.
  - The FAA data has up to two associated LOC arrays (usually 1 if there is an IAP, rarely 2), which can be selected by specifying `1` or `2`.

The Centerline object has the following properties:

| Property              | Required | Type     | Default | Description                                                                                     |
| --------------------- | -------- | -------- | ------- | ----------------------------------------------------------------------------------------------- |
| `runway_id`           | \*       | `string` |         | A string value representing the runway id.                                                      |
| `length`              |          | `float`  | `10.0`  | A float value representing the length of the centerline in nautical miles.                      |
| `crossbar_scale`      |          | `float`  | `0.5`   | A float value representing the width of the crossbars in nautical miles.                        |
| `selected_iap`        |          | `string` |         | A string value representing the selected Instrument Approach Procedure used to draw crossbars.  |
| `selected_transition` |          | `string` |         | A string value representing the selected IAP transition used to draw crossbars.                 |
| `selected_loc`        |          | `int`    |         | An integer value of `1` or `2` representing the selected LOC array used to draw the centerline. |

[Back to Map Objects](./MAP_OBJECTS.md)

[Back to README](../README.md)
