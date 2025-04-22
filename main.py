from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/astroseek", methods=["GET"])
def get_astro_data():
    nome = request.args.get("nome")
    data = request.args.get("data")
    ora = request.args.get("ora")
    luogo = request.args.get("luogo")

    if not all([nome, data, ora, luogo]):
        return jsonify({"error": "Missing parameters"}), 400

    giorno, mese, anno = data.split("-")[2], data.split("-")[1], data.split("-")[0]
    ora_h, ora_m = ora.split(":")

    url = "https://it.astro-seek.com/tema-natale-calcolo-oroscopo-online"

    payload = {
        "narozeni_den": giorno,
        "narozeni_mesic": mese,
        "narozeni_rok": anno,
        "narozeni_hodina": ora_h,
        "narozeni_minuta": ora_m,
        "narozeni_misto": luogo,
        "send_calculation": "1"
    }

    session = requests.Session()
    res = session.post(url, data=payload)
    if res.status_code != 200:
        return jsonify({"error": "AstroSeek unreachable"}), 500

    soup = BeautifulSoup(res.text, "html.parser")
    result = {}

    try:
        asc = soup.find("div", class_="zodiacSignAscendant").text.strip()
        result["ascendente"] = asc
    except:
        result["ascendente"] = "Non trovato"

    try:
        luna = soup.find("td", string="Luna").find_next_sibling("td").text.strip()
        result["luna"] = luna
    except:
        result["luna"] = "Non trovata"

    try:
        sole = soup.find("td", string="Sole").find_next_sibling("td").text.strip()
        result["sole"] = sole
    except:
        result["sole"] = "Non trovato"

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)