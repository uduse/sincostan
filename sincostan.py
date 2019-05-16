# coding: utf-8
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from IPython import display
import nltk
from nltk.corpus import wordnet as wn

subscription_key = "your key here"
client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))

nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}

trigs = [
    ('sin', 'cos', 'tan'),
    ('cos', 'sin', 'cot'),
    ('cos', 'cot', 'sin'),
    ('sin', 'tan', 'cos')
]

def search_thumb(word):
    image_results = client.images.search(word, size='Medium')
    first_result = image_results.value[0]
    url = first_result.thumbnail_url
    response = requests.get(url)
    thumb = Image.open(BytesIO(response.content))
    thumb.thumbnail((130, 130), Image.ANTIALIAS)
    return thumb

def generate(upper, lower, thumb):
    font = ImageFont.truetype('A little sunshine.ttf', size=64)
    img = Image.open('background.png')
    draw = ImageDraw.Draw(img)
    draw.text((20, 150), upper, fill=(0, 0, 0), font=font)
    draw.line([(20, 220), (220, 220)], fill=(0, 0, 0), width=2)
    draw.text((20, 230), lower, fill=(0, 0, 0), font=font)
    draw.text((240, 190), "=", fill=(0, 0, 0), font=font)
    img.paste(thumb, (280, 180))
    return img

if __name__ == '__main__':
    for numer, denom, val in trigs:
        for word in nltk.corpus.words.words():
            if word.startswith(val) and len(word) >= 4:
                if word in nouns:
                    tail = word[len(val):]
                    upper = f"{numer}({tail})"
                    lower = f"{denom}({tail})"
                    thumb = search_thumb(word)
                    img = generate(upper, lower, thumb)
                    img.save(f"imgs/{upper}_{lower}_{word}.jpeg")
                    display.display(img)
