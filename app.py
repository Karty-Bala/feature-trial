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

    webCatURL = ("https://website-categorization.whoisxmlapi.com/api/v3?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge"
                 "&domainName=")
    geoLocURL = "https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge&domain="
    domRepURL = "https://domain-reputation.whoisxmlapi.com/api/v2?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge&domainName="

    if request.method == "POST":
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

        y_pred = gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0, 0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]

        domain_name = get_domain_name(url)

        webCatResult = requests.get(webCatURL + domain_name)
        geoLocResult = requests.get(geoLocURL + domain_name)
        domRepResult = requests.get(domRepURL + domain_name)

        webCat_data = json.loads(webCatResult.content.decode('ascii'))
        geoLoc_data = json.loads(geoLocResult.content.decode('ascii'))
        domRep_data = json.loads(domRepResult.content.decode('ascii'))

        # webCat INFO
        categories = webCat_data.get('categories', [])
        if 'code:422' in webCat_data:
            listCategories = [{"name": "", "confidence": "Not Enough Content"}]
        else:
            listCategories = []
            for category in categories:
                name = category.get('name', '')
                confidence = category.get('confidence', 0)
                listCategories.append({"name": name, "confidence": int(confidence * 100)})

        #geoloc INFO
        country = geoLoc_data["location"]["country"]
        region = geoLoc_data["location"]["region"]

        #domRep INFO
        warning_descriptions = []
        domRepScore = domRep_data["reputationScore"]
        for index, result in enumerate(domRep_data["testResults"]):
            if result["test"] == "SSL vulnerabilities":
                for warning in result["warnings"]:
                    warning_descriptions.append(warning["warningDescription"])
                break
        print(listCategories)
        print("Country:", country)
        print("Region:", region)
        print("Domain Reputation Score:", domRepScore)
        for warns in warning_descriptions:
            print(warns)
        return render_template('index.html', xx=round(y_pro_non_phishing, 2), url=url, listCategories=listCategories, country=country, region=region, domRepScore=domRepScore, warning_descriptions=warning_descriptions)
    return render_template("index.html", xx=-1)


if __name__ == "__main__":
    app.run(debug=True)
