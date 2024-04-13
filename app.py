from feature import FeatureExtraction
from flask import Flask, request, render_template
from urllib.parse import urlparse
import requests
import json
import numpy as np
import pickle
import warnings

warnings.filterwarnings('ignore')

file = open("pickle/model.pkl", "rb")
gbc = pickle.load(file)
file.close()

app = Flask(__name__)


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

        y_pred = gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0, 0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]

        domain_name = get_domain_name(url)
        result = requests.get("https://website-categorization.whoisxmlapi.com/api/v3?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge&domainName=" + domain_name)
        data = json.loads(result.content.decode('ascii'))
        categories = data.get('categories', [])
        print(data)
        print(categories)
        if 'code:422' in data:
            listCategories = [{"name": "Unavailable", "confidence": "Not Enough Content"}]
        else:
            listCategories = []

            for category in categories:
                name = category.get('name', '')
                confidence = category.get('confidence', 0)
                listCategories.append({"name": name, "confidence": int(confidence * 100)})

            print(listCategories)

        return render_template('index.html', xx=round(y_pro_non_phishing, 2), url=url, categories=categories)
    return render_template("index.html", xx=-1)


if __name__ == "__main__":
    app.run(debug=True)
