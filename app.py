from chalice import Chalice, Response
import jinja2
import os 
import uuid
import time
app = Chalice(app_name='blog')
import sqlite3
import json



#conn.execute('DROP TABLE blog')
# conn.execute('''CREATE TABLE blog
#         (ID VARCHAR(100) PRIMARY KEY     NOT NULL,
#         NAME             TEXT    NOT NULL,
#         TIME             INT     NOT NULL,
#         CONTENT          VARCHAR(1000000),
#         IMAGE            VARCHAR(1000000))''')






def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or      "./")).get_template(filename).render(context)



@app.route("/")
def index():
    conn = sqlite3.connect('blog.db')
    
    cursor = conn.execute("SELECT * from blog")
    
    dict_post = {}
    for row in cursor:
        print(row)
        dict_post[row[0]] = {"name":row[1], "content":row[3],"image":row[4]}

    template = render("templates/index.html", {"blog_posts":dict_post})
    conn.close()
    return Response(template, status_code=200, headers={
        "Content-Type": "text/html",
        "Access-Control-Allow-Origin": "*"
    })

@app.route("/create")
def create():
    current_blog = []
    blog_posts = []
    context = {
        "current_blog": current_blog,
        "blog_posts": blog_posts
    }
    template = render("templates/create.html", context)
    return Response(template, status_code=200, headers={
        "Content-Type": "text/html",
        "Access-Control-Allow-Origin": "*"
    })

@app.route("/create_post", methods=['POST'] , content_types=['application/json'])
def create_post():
    conn = sqlite3.connect('blog.db')
    request_body = app.current_request.raw_body.decode()
    json_data = json.loads(request_body)

    name=json_data['name']
    content=json_data['content']
    image=json_data['image']
    conn.execute(f"""INSERT INTO blog (ID,NAME,TIME,CONTENT,IMAGE) VALUES ("{uuid.uuid4().int}", "{name}", "{time.time()}", "{content}","{image}")""")
    conn.commit()
    conn.close()
    return request_body

