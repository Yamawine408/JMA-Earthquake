# JMA Earthquake

This Home Assistant integration is to obtain the latest earthquake
information from JMA (Japan Meteorological Agency, 気象庁). 

## Install using HACS
If you are using HACS (Home Assistant Community Store), go to HACS,
click on the three dots at the upper right corner, select `custom
repositories`, and then input
`https://github.com/Yamawine408/JMA-Earthquake` as an integration. 

Next, add the following lines into the configuration.yaml file;

```
sensor:
  - platform: japan_meteorological_agency
```

Then, restart your Home Assistant.

## Install manually

1. Create a directory `jma_earthquake` under the `config/custom_components` directory.
2. Go to 
`https://github.com/Yamawine408/JMA-Earthquake/tree/main/custom_components/jma_earthquake`,
and copy all files into the created directory.
3. Add the sensor configuration shown above into the
`configuration.yaml` file.
4. Restart your Home Assistant

## How to use

If succeeded, you will see the `sensor.latest_earthquake` entity with the
state holding the Japanese text of the latest earthquake information.

The entity also holds attributes about the location of the earthquake
(latitude, longitude and depth of the earthquake), as well as the time
of the event, so that the entity can be used with the lovelace map
card to display the latest earthquake on the map. The YAML
configuration of the map is shown below;

```
type: map
entities:
  - entity: zone.home
  - entity: sensor.latest_earthquake
    label_mode: attribute
    attribute: magstr
    focus: true
theme_mode: auto
hours_to_show: 0
default_zoom: 3
aspect_ratio: "1"
grid_options:
  columns: 12
  rows: 4
auto_fit: true
```

