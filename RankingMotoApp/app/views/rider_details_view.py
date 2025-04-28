from flask import render_template, request
from services.rider_service import get_race_details


def race_details():
    # lecture formulaire
    rider_n = request.form['rider_number']
    ranking_url = request.form['ranking_url']  

    # appel service : get rider & race
    get_race_details(rider_n, ranking_url)

    # return templace avec infos
    
    return render_template('ALESTREM2025.html')