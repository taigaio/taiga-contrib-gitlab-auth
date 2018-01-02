Taiga contrib gitlab auth
=========================

[![Kaleidos Project](http://kaleidos.net/static/img/badge.png)](https://github.com/kaleidos "Kaleidos Project")
[![Managed with Taiga.io](https://img.shields.io/badge/managed%20with-TAIGA.io-709f14.svg)](https://tree.taiga.io/project/taiga/ "Managed with Taiga.io")

The Taiga plugin for gitlab authentication (Ported from official gitlab auth).

Installation
------------
### Production env

#### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-gitlab-auth-official` with:

```bash
  pip install taiga-contrib-gitlab-auth-official
```

Modify your `settings/local.py` and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_gitlab_auth"]

  # Get these from Admin -> Applications
  GITLAB_API_CLIENT_ID = "YOUR-GITLAB-CLIENT-ID"
  GITLAB_API_CLIENT_SECRET = "YOUR-GITLAB-CLIENT-SECRET"
  GITLAB_URL="YOUR-GITLAB-URL"
```

#### Taiga Front

Download in your `dist/plugins/` directory of Taiga front the `taiga-contrib-gitlab-auth` compiled code (you need subversion in your system):

```bash
  cd dist/
  mkdir -p plugins
  cd plugins
  svn export "https://github.com/taigaio/taiga-contrib-gitlab-auth/tags/$(pip show taiga-contrib-gitlab-auth-official | awk '/^Version: /{print $2}')/front/dist"  "gitlab-auth"
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/gitlab-auth/gitlab-auth.json"`:

```json
...
    "gitLabClientId": "YOUR-GITLAB-CLIENT-ID",
    "gitLabUrl": "YOUR-GITLAB-URL",
    "contribPlugins": [
        (...)
        "/plugins/gitlab-auth/gitlab-auth.json"
    ]
...
```

### Dev env

#### Taiga Back

Clone the repo and

```bash
  cd taiga-contrib-gitlab-auth/back
  workon taiga
  pip install -e .
```

Modify `taiga-back/settings/local.py` and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_gitlab_auth"]

  # Get these from Admin -> Applications
  GITHUB_API_CLIENT_ID = "YOUR-GITLAB-CLIENT-ID"
  GITHUB_API_CLIENT_SECRET = "YOUR-GITLAB-CLIENT-SECRET"
  GITLAB_URL="YOUR-GITLAB-URL"

```

#### Taiga Front

After clone the repo link `dist` in `taiga-front` plugins directory:

```bash
  cd taiga-front/dist
  mkdir -p plugins
  cd plugins
  ln -s ../../../taiga-contrib-gitlab-auth/front/dist gitlab-auth
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/gitlab-auth/gitlab-auth.json"`:

```json
...
    "gitLabClientId": "YOUR-GITLAB-CLIENT-ID",
    "gitLabUrl": "YOUR-GITLAB-URL",
    "contribPlugins": [
        (...)
        "/plugins/gitlab-auth/gitlab-auth.json"
    ]
...
```

In the plugin source dir `taiga-contrib-gitlab-auth/front` run

```bash
npm install
```
and use:

- `gulp` to regenerate the source and watch for changes.
- `gulp build` to only regenerate the source.

Running tests
-------------

We only have backend tests, you have to add your `taiga-back` directory to the
PYTHONPATH environment variable, and run py.test, for example:

```bash
  cd back
  add2virtualenv /home/taiga/taiga-back/
  py.test
```
