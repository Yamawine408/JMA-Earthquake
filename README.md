# JMA Earthquake

This Home Assistant integration is to obtain latest earthquake information from JMA (Japan Meteorological Agency).

## Install using HACS
If you are using HACS (Home Assistant Community Store), go to HACS,
click on the three dots at the upper right corner, select 'custom
repositories,' and then input
'https://github.com/Yamawine408/JMA-Earthquake' as an integration. 

Next, add the following lines into the configuration.yaml file;

```sensor:
  - platform: jma_earthquake
```

Then, reatsrt your Home Assistant.

If succeeded, you will have 'sensor.latest_earthquake' entity with the
state holding the Japanese text of the latest earthquake information.

The entity also holds the location of the earthquake (latitude,
longitude and depth of the earthquake), and the entity can be used
with the lovelace map card to display the latest earthquake, shown as
below;

```type: map
entities:
  - entity: zone.home
  - entity: sensor.latest_earthquake_2
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

