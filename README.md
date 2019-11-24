# Serverless blog

First version created following [blog post on Medium](https://medium.com/richcontext-engineering/creating-a-serverless-blog-with-chalice-bdc39b835f75).

Credit to @TJBANEY (original repo can be found [here](https://github.com/TJBANEY/chalice_blog))

Simple but efficient, I will work on integrating more security and features to it in a near future.

## Quickstart

* Create a mongodb Database and collection.
* Edit file `app.py` to replace username & password accordingly.
* Create a virtual env, install chalice and run `chalice deploy`.

Note that you might encounter few errors if you try to run it with `chalice local`:

* Posting a message might require to .decode('utf-8') the body
* Links in html pages will not include "/api" prefix locally
