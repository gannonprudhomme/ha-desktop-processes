[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

Integration to read from process volumes from Desktop Control Tablet Server and store it in an entity.

## Additional Configuration

You can add the integration through Home Assistant's UI.

Additional, you can add the following to your `configuration.yaml`:

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

[commits-shield]: https://img.shields.io/github/commit-activity/y/gannonprudhomme/ha-desktop-processes.svg?style=for-the-badge
[commits]: https://github.com/gannonprudhomme/ha-desktop-processes/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/gannonprudhomme/ha-desktop-processes.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/gannonprudhomme/ha-desktop-processes.svg?style=for-the-badge
[releases]: https://github.com/gannonprudhomme/ha-desktop-processes/releases
[user_profile]: https://github.com/gannonprudhomme
