# lkhamsurenl.github.io


## Generate new page

Run following command to convert any given ipynb to HTML page that's automatically indexed:

```{bash}
python convert.py assets/notebooks/glucose/2023-02-19-CGM.ipynb
```

## Test locally

```{bash}
(cd $HOME/development/lkhamsurenl.github.io && bundle exec jekyll serve)

```

If there was a chance in dependency, then run 

```{bash}
bundle install
```

You can also encrypt the page that you don't want publich with https://github.com/robinmoisson/staticrypt:

```{bash}
npx staticrypt _posts/2022-12-29-spendings.html PASSPHRASE
```
