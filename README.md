# lkhamsurenl.github.io


## Generate new page

Run following command to turn a notebook into a Markdown post in `_posts/`, with its charts in
`assets/images/<slug>/`. The date and title come from the file name and the first `# ` heading;
`python convert.py --help` lists the overrides.

```{bash}
python convert.py assets/notebooks/glucose/2023-02-19-CGM.ipynb
```

Add `--no-execute` to use the outputs saved in the notebook instead of rerunning it.

## Test locally

Requires the Ruby version in `.ruby-version` (chruby switches to it automatically).

```{bash}
(cd $HOME/development/lkhamsurenl.github.io && bundle exec jekyll serve)

```

If there was a change in dependency, then run 

```{bash}
bundle install
```

## Checks

Every push and pull request builds the site and checks its internal links, including links into
`/books/` and `/restaurant/`; a broken link fails the build before anything deploys. Dependabot
opens one grouped PR a month for gem and GitHub Actions updates.
