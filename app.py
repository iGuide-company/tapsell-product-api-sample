import json
from fastapi import FastAPI
import requests
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    # 'http://127.0.0.1:8003',
    # 'http://localhost:8003',
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",response_class=HTMLResponse)
def index():
    return f'''
<html>
    <head>
        <link rel="stylesheet" href="https://iguide-backend.darkube.app/public/bc567adc-67a8-4064-a8d1-a16eacc69ed9/assets/index-f884a369.css" /> 
        <title>Tapsell sample use iguide</title>
    </head>
    <body>
        <div style="position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:300px;text-align:center;"><h1>Hi Dear.</h1> <p>Wellcome to iGuide for use this tools for answer to your question about tapsell open chatbox.</p></div>
        <div id="shoper-root"></div>
        <script src="https://iguide-backend.darkube.app/public/bc567adc-67a8-4064-a8d1-a16eacc69ed9/assets/index-51bf4707.js"></script>
    </body>
</html>
'''

@app.get("/products")
def getData():
    response = requests.get("https://college.tapsell.ir/wp-json/wp/v2/categories").json()
    categories = {}
    for category in response:
        print(category)
        categories[category['id']] = category['name']

    response = requests.get("https://college.tapsell.ir/wp-json/wp/v2/posts?categories=90,112&per_page=100")
    result = []
    for item in response.json():
        result.append({
            "id": str(item['id']),
            "title": item['title']['rendered'],
            "attr": [
                {
                    "key": "excerpt",
                    "value": item['excerpt']['rendered']
                },
                {
                    "key": "category",
                    "value": categories[item['categories'][0]]
                }
            ]
        })

    return result


@app.get("/products/{id}")
def getData(id:str):
    response = requests.get(f"https://college.tapsell.ir/wp-json/wp/v2/posts/{id}")
    return response.json()
