# This is a basic workflow to help you get started with Actions

name: Pre-Deployment Checks

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  pull_request:
    branches: [ master ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - name: Checkout master
    - uses: actions/checkout@v2
      with: 
        ref: master

    - name: Copy CSVs to /tmp
      run: cp test.csv /tmp/test-master.csv

    - name: Checkout testing
    - uses: actions/checkout@v2
      with: 
        ref: testing

    - name: Copy CSVs to /tmp
      run: cp test.csv /tmp/test-staged.csv

    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    # Runs a set of commands using the runners shell
    - name: Run a multi-line script
      run: |
        echo Comparing CSVs...
        python3 ./CI/check_csv.py
        cat /tmp/test-staged.csv
        cat /tmp/test-master.csv
