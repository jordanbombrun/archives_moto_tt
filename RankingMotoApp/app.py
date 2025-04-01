from flask import Flask, render_template, request
import RankingMotoApp.views.parse_datas as parse_datas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ALESTREM2025.html')

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/render_rider_datas', methods=['POST'])
def render_rider_datas():
    rider_n = request.form['rider_number']
    ranking_url = request.form['ranking_url']    
    rider = parse_datas.process(rider_n, ranking_url)
    rider_positions = rider.format_positions_html()
    return render_template('rider_info.html', rider=rider, rider_positions=rider_positions) 
