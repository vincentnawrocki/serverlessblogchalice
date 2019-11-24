from chalice import Chalice, Response
from pymongo import MongoClient
import os
import jinja2
import urllib
import slugify
import datetime

app = Chalice(app_name='helloworld')

client = MongoClient("mongodb+srv://username:password@blogs-3khlw.mongodb.net/test?retryWrites=true")
db = client.chaliceblog
posts = db.blog_posts

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./")).get_template(filename).render(context)

@app.route("/")
def index():
    current_blog = {
        "title": "No Posts Yet",
        "content": "",
        "create_date": ""
    }

    blog_posts = db.blog_posts.find({}).sort([("create_date", -1)])

    if blog_posts.count() != 0:
        current_blog = blog_posts[0]

    context = {
        "current_blog": current_blog,
        "blog_posts": blog_posts
    }
    template = render("chalicelib/templates/index.html", context)
    return Response(template, status_code=200, headers={"Content-Type": "text/html", "Access-Control-Allow-Origin": "*"})

@app.route("/blog/{blog_slug}")
def blog_view(blog_slug):
    blog_posts = db.blog_posts.find({}).sort([("create_date", -1)])
    current_blog = db.blog_posts.find_one({"slug": blog_slug})
    context = {
        "current_blog": current_blog,
        "blog_posts": blog_posts
    }
    template = render("chalicelib/templates/index.html", context)
    return Response(template, status_code=200, headers={
        "Content-Type": "text/html",
        "Access-Control-Allow-Origin": "*"
    })

@app.route("/admin")
def create_blog():
    template = render("chalicelib/templates/admin.html", {})
    return Response(template, status_code=200, headers={
        "Content-Type": "text/html",
        "Access-Control-Allow-Origin": "*"
    })

@app.route("/post-blog", methods=["POST"], content_types=["application/x-www-form-urlencoded"])
def post_blog():
    post_json = urllib.parse.parse_qs(app.current_request.__dict__.get("_body"))
    title = post_json["title"][0]
    content = post_json["content"][0]
    slug = slugify.slugify(title)
    blog_post = {
        "title": title,
        "content": content,
        "slug": slug,
        "create_date": datetime.datetime.now()
    }
    try:
        result = db.blog_posts.insert_one(blog_post)
    except Exception as e:
        context = {
            "notification": f"Something Went Wrong: {e}",
            "notification_color": "#f74435",
            "notification_border": "#88261e",
            "title": title,
            "content": content
        }
    else:
        context = {
            "notification": "Blog Post Successful",
            "notification_color": "#37da61",
            "notification_border": "#2ba74a",
            "title": "",
            "content": ""
        }
    template = render("chalicelib/templates/admin.html", context)
    return Response(template, status_code=200, headers={
        "Content-Type": "text/html",
        "Access-Control-Allow-Origin": "*"
    })
