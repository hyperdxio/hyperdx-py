# hyperdx-opentelemetry-python changelog

## [0.4.0] - 2026-07-27

### Enhancements

- Relax OpenTelemetry constraints to ranges (#41) — `opentelemetry-{api,sdk,exporter-otlp}` move from `==1.30.0` to `>=1.30.0,<2.0.0` and `opentelemetry-instrumentation` from `==0.51b0` to `>=0.51b0,<1.0.0`, so the distro can be co-installed with other OpenTelemetry-based libraries that require a newer core

### Fixes

- Repair smoke-test docker build and `pkg_resources` runtime error (#40)
- Pin `setuptools >= 78.1.1` (#37)

### Maintenance

- ci: move release job off retired ubuntu-20.04 runner (#43)
- ci: forward only required secrets to reusable workflows (#42)
- ci: add hyperdxio org-wide reusable workflow caller stubs (#42)
- ci: use ubuntu-latest instead of retired ubuntu-20.04 runner (#38)
- chore(deps): bump idna from 3.10 to 3.15 (#39)
- chore(deps): bump protobuf from 5.29.3 to 5.29.6 (#36)

Note: releases 0.3.0b0, 0.3.0, and 0.2.0 were published without changelog entries. This entry covers changes since 0.3.0 only.

## [0.2.1b0] - 2023-05-16

### Fixes

- Don't init HyperDXOptions on import (#134) | [@gaganpreet](https://github.com/gaganpreet)

### Maintenance

- maint(deps-dev): bump pylint from 2.17.2 to 2.17.3 (#132)
- maint(deps-dev): bump coverage from 7.2.3 to 7.2.5 (#133)
- maint(deps-dev): bump pytest from 7.3.0 to 7.3.1 (#130)

## [0.2.0b0] - 2023-04-11

### Maintenance

- maint: Update OTel packages to 1.17.0/0.38b0 (#127) | [@MikeGoldsmith](https://github.com/MikeGoldsmith)
- maint: Set opentelemetry to version 1.16.0 (#125) | [@guillemtrebol](https://github.com/guillemtrebol)
- maint: Use squash merge for dependabot auto-merge (#122) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: Update readme status (#121) | [@vreynolds](https://github.com/vreynolds)
- maint: Change experimental badge to active (#120) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: Improve ci time (#114) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: Add auto-merge dependabot workflow (#113) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint(deps-dev): bump pylint from 2.16.2 to 2.17.1 (#115)
- maint(deps-dev): bump pytest from 7.2.1 to 7.2.2 (#117)
- maint(deps-dev): bump coverage from 7.2.1 to 7.2.3 (#126)
- maint(deps-dev): bump importlib-metadata from 6.0.0 to 6.1.0 (#119)

## [0.1.2b0] - 2023-03-29

Initial beta release of HyperDX's OpenTelemetry distribution for Python!

### Maintenance

- ci: require smoke tests for publish steps (#107) | [@pkanal](https://github.com/pkanal)
- maint: drop poetry locks from example apps (#111) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: add tests for auto instrumentation (#110) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint(deps-dev): bump coverage from 6.5.0 to 7.2.1 (#104)

## [0.1.1a3] - 2023-03-07

### Enhancements

- feat: move away from a ParentBased sampling approach. (#96) | [@emilyashley](https://github.com/emilyashley)
- feat: allow HYPERDX_API_ENDPOINT as an Option parsed as an environment variable (#99) | [@emilyashley](https://github.com/emilyashley)

### Maintenance

- doc: clarify SDK configuration options (command vs function) and final developing.md & readme.md audits (#105) | [@emilyashley](https://github.com/emilyashley)
- maint: grpc smoke tests for hello-world-flask application (#102) | [@emilyashley](https://github.com/emilyashley)
- maint: Flask smoke tests for http and collector. (#101) | [@emilyashley](https://github.com/emilyashley)
- maint: dockerizing flask app (#83) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: smoke test python app (#91) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: add coverage report html to circleci artifacts (#93) | [@emilyashley](https://github.com/emilyashley)
- maint: enable linting step in CI  (#92) | [@emilyashley](https://github.com/emilyashley)
- doc: audit of docstrings for dev-friendliness & relevance (#85) | [@emilyashley](https://github.com/emilyashley)

## [0.1.1a2] - 2023-02-22

A very alpha release.
