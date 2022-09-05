# Wait for CI Checks

Hello! This action is intended to be used in workflows where you need to wait
for a certain type of job to finish.

We all have been there before, and we banged our heads against the wall to come
up with a solution (or use someone else solution) to bypass this weird behavior
that GitHub has with the `workflow_*` events. If you're like me and you need
this action for some weird case in your pipeline, then please, feel free to use
it (and contribute if you find any bugs or improvements).

## Action Inputs

| Input Name      | Description                                                                                                                                                                 | Default value                 |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `token`         | The GitHub token to use for making API requests.                                                                                                                            | `${{ github.token }}`         |
| `ref`           | The Git ref of the commit you want to poll for a passing check.                                                                                                             | `${{ github.sha }}`           |
| `repository`    | The name of the GitHub repository (with owner) you want to poll for a passing check. Example: r0x0d/wait-for-ci-checks.                                                     | `${{ github.repository }}`    |
| `checkNames`    | The name of the GitHub check to wait for. For example, `build` or `deploy`. A list can be used in the following format: `build;deploy;other-workflow``                      | empty, **required from user** |
| `allowedStates` | The name of the states to validate against the GitHub check. For example, `completed` or `in_progress`. A list can be used in the following format: `completed;in_progress` | completed                     |
| `interval`      | The number of seconds to wait between API calls.                                                                                                                            | 20                            |
| `maxWaitTime`   | The number of seconds to wait for the check to complete.                                                                                                                    | 720                           |

## Action Outputs

| Input Name | Description                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------------ |
| `status`   | A status determining if the run workflow ended successfully or not. The output can be either: `succes` or `failed` |

## Getting started

First of, to use this action you will need to place it as a job in your workflow
file, let's get a example here real quick:

```yaml
name: Deploy
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  wait_build_to_finish:
    runs-on: ubuntu-latest
    steps:
      - name: Wait for build process to finish
        uses: r0x0d/wait-for-ci-checks@v0.2.0
        with:
          # If you're running this on a pull request from a fork
          ref: ${{ github.event.pull_request.head.sha }}
          checkNames: "super-long-build"

  delpoy_your_awesome_app:
    needs: [wait_build_to_finish]
    runs-on: ubuntu-latest
    steps:
      ...
```

And that's it. Really simple, huh?

If you want have more than one workflow that you would like to wait for
completion, you can do so by extending the `checkNames` property this way:

```yaml
name: Deploy
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  wait_build_to_finish:
    runs-on: ubuntu-latest
    steps:
      - name: Wait for build process to finish
        uses: r0x0d/wait-for-ci-checks@v0.2.0
        with:
          # If you're running this on a pull request from a fork
          ref: ${{ github.event.pull_request.head.sha }}
          checkNames: "super-long-build;super-long-docs-build;sanity-check;really-another-sanity-check"

  delpoy_your_awesome_app:
    needs: [wait_build_to_finish]
    runs-on: ubuntu-latest
    steps:
      ...
```

## Contributing

If you find any bugs or you want to improve the way this action works, just send
a issue asking for the specific implementation you have in mind, or if you're
confident enough to come up with a pull request, please do so as well.

Also, don't be shy! Every idea, request and suggestion will be treated with kind
and respect.
