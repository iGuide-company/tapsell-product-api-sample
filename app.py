import json
from fastapi import FastAPI
import requests

app = FastAPI()

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
            "id": item['id'],
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