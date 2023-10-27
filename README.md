# Desktop Processes Integration

Home Assistant custom integration for retrieving and controlling process volumes for a PC.
 Built to communicate with the [Desktop Control Tablet Server](https://github.com/gannonprudhomme/Desktop-Control-Tablet-Server).

## Installation (via HACS)

0. The project is added as a custom repository from [HACS](https://hacs.xyz/), so make sure you have that installed first.

1. Add it as a custom repository in HACS:

    a. Go to HACS panel -> Integrations

    b. In the dropdown on the top right, click `Custom repositories`

    c. In the `Add custom repository URL` field, enter `https://github.com/gannonprudhomme/ha-desktop-processes`
    and for `category` enter `Integration`.

    d. The repository should appear as a `New repository` on the `Integration` screen. If it doesn't,
    go to `+ Explore & Add Repositories` then search for it. You'll then need to restart HA.

    e. Then click `Install` to install it into `config/custom_components`

2. Add it to Home Assistant as you would any other integration, and enter the desktop's URL
during the config flow.

3. You can optionally add an ignore list and prioritize the sorting of certain processes in the
below Configuration step.

## Configuration

You can add the integration through Home Assistant's UI.

Additionally, you can add the following to your `configuration.yaml`:

```yaml
desktop_processes:
  scanning_interval: 5 # in seconds, defaults to 10
  ignore: # The display names of the programs you want to be ignored
    - svchost
    - nvcontainer
    - NVIDIA Broadcast

  # Determines sort priority, descending
  priority:
    - name: Spotify
      priority: 2
    - name: Discord
      priority: 1
    - name: chrome
      priority: -1
```

## Development

Due to Docker not allowing host networking on Windows, you must install Home Assistant manually
(`pip install wheel`, `pip install homeassistant`, `hass -c config/`) and put this repo
in the `config/` folder.
