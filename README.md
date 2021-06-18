# Homie - static homepage for all of your services

A simple single static site that gives you an overview of all of your services.

## Demo
![](https://github.com/M0r13n/homie/blob/master/img/img.png)

You can find a [demo here](https://leonmortenrichter.de/homie/)

## Why?

I wanted a simple static site, that comes without any databases, Javascript and other bloat. I wanted plain old HTML and CSS. Therefore, the generated
site is perfectly suited to be used in with GitHub/GitLab pages.

The site was loosely inspired by [homer](https://github.com/bastienwirtz/homer) - but without the need of Docker, NPM, Vue. etc.

## How to use?

### Install the module

```bash
# Clone the repository (currently not on PyPi)
$ git clone https://github.com/M0r13n/homie
# Navigate into the module directory
$ cd homie
# Install homie and it's dependencies
$ pip install .
# Verify
$ which homie
```

### Prepare your dashboard definition
Create a new file named `dashboard.yml`. See [this](https://github.com/M0r13n/homie/blob/master/example/dashboard.yaml) file for a real world example.

The YAML file is structured as follows:

```yaml
  
title: 'Services Dashboard' # Title of the dashboard
categories: 
  # List of categories
  # Each category has a name and a set of hosts
  - title: "Dev tools"
    hosts:
      # A list of hosts
      # Each hosts can have: name, host, note, icon and a badge
      - name: "GitLab"              # Name of the host
        host: "www.gitlab.com"      # Domain of the host
        note: "Source Control"      # A short note about the host
        icon: "gitlab.svg"          # An icon (can be PNG or SVG)
        badge: "legacy"             # A badge that is displayed next to the note

      - name: "Jenkins"
        host: "www.jenkins.com"
        note: "Build Pipelines"
        icon: "jenkins.svg"

      - ...

  - title: "Misc"
    hosts:
      ...
```

Icons should to be stored in a directory `icons` in the same folder as the `dashboard.yml`.
Icons can be either `.png` or `.svg`.

### Build
```
# Build the page
$ homie build

# Serve
$ homie server
Serving on http://127.0.0.1:5000

```

### Deploy
Because the generated site is completely static, it can be hosted anywhere. Just copy the `build` dir into a publicly accessible directory on your server.

Or, you can use [GitHub Pages](https://pages.github.com/). Create a file called `.github/workflows/gh-pages.yml`:


```yaml
name: github pages

on:
  push:
    branches:
      - master  # Set a branch name to trigger deployment
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-18.04
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v1
        with:
          python-version: '3.7'
          
      - name: Clone homie
        run: git clone https://github.com/M0r13n/homie

      - name: Install requirements
        run: cd homie && pip install .

      - name: Build
        run: homie build -d example

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        if: github.ref == 'refs/heads/master'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build

```
 
## Attribution
- https://andybrewer.github.io/mvp/
