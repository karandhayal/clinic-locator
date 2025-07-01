# app.py
from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Load clinic data from CSV
clinics = []
with open('data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        clinics.append(row)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    search_pin = search_city = ""
    if request.method == 'POST':
        search_pin = request.form['pincode'].strip()
        search_city = request.form['city'].strip().lower()
        pin_matches = [clinic for clinic in clinics if clinic['Pin Code'] == search_pin]
        city_matches = []
        if search_city:
            city_matches = [clinic for clinic in clinics if clinic['City'].lower() == search_city and clinic not in pin_matches]
        results = pin_matches + city_matches

    return render_template('index.html', results=results, pin=search_pin, city=search_city)

@app.route('/clinic/<name>')
def clinic_detail(name):
    clinic = next((c for c in clinics if c['Clinic Name'] == name), None)
    return render_template('clinic_detail.html', clinic=clinic)

if __name__ == '__main__':
    app.run(debug=True)
