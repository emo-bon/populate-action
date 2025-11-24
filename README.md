# populate-action

Action to populate observatory crates with README and raw logsheets.

To give an example, the following workflow file will download the logsheets, convert them to csv format and commit the changes if relevant.

```
on:
  push:
jobs:
  job:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v3
      - name: populate-action
        uses: emo-bon/populate-action@main
      - name: git-auto-commit-action
        uses: stefanzweifel/git-auto-commit-action@v4
```
