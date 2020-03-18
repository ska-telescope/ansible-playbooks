## 1.1.0

* Version bump to ES v6.7.
* Replaced register with handler for restart.
* Added better log4j2 defaults and slowlogs.
* Added optional symlink of logs dir to `/var/log/elasticsearch`.
* Changed default heap size to be dynamic.

## 1.0.0

BACKWARDS INCOMPATIBILITIES / NOTES:

* Reworked to use the official ES 6 docker images. In order to avoid having to
manage plugins and geoip config at this time, only the files managed by this
role are mounted into the container.  Previously the entire `config` folder was
mounted.
