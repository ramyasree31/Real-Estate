from http.client import responses

from flask import Flask, request, jsonify,render_template
import util
import os


app = Flask(
    __name__,
    template_folder=os.path.join(os.path.pardir, "client"),
    static_folder=os.path.join(os.path.pardir, "client")  # serve css & js from client
)

@app.route('/home_page')
def home_page():
    return render_template('app.html')


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({

        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    # 1️⃣ First check JSON body
    if request.is_json:
        data = request.get_json()
        sqft = float(data.get('sqft', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))

    # 2️⃣ If form-data (POST form submission)
    elif request.form:
        sqft = float(request.form.get('sqft', 0))
        location = request.form.get('location', '')
        bhk = int(request.form.get('bhk', 0))
        bath = int(request.form.get('bath', 0))

    # 3️⃣ If query params (GET ?total_sqft=1000&...)
    else:
        sqft = float(request.args.get('sqft', 0))
        location = request.args.get('location', '')
        bhk = int(request.args.get('bhk', 0))
        bath = int(request.args.get('bath', 0))

    # Call your util function
    estimated_price = util.get_estimated_price(location, sqft, bhk, bath)

    response = jsonify({
        'estimated_price': estimated_price
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()