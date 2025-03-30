from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import datetime
import sqlite3
import io
from io import BytesIO
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import random

app = Flask(__name__)

engine = sqlalchemy.create_engine("sqlite:///stadiums.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stadiums.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/css'
app.config['ALLOWED_EXTENSIONS'] = {'css'}
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')


stadiums_data = [
    {"name": "MetLife Stadions", "location": "East Rutherford, NJ", "capacity": 82500, "year_opened": 2010, "team": "New York Giants, New York Jets"},
    {"name": "Lambeau Laukums", "location": "Green Bay, WI", "capacity": 81441, "year_opened": 1957, "team": "Green Bay Packers"},
    {"name": "AT&T Stadions", "location": "Arlington, TX", "capacity": 80000, "year_opened": 2009, "team": "Dallas Cowboys"},
    {"name": "Mičiganas Stadions", "location": "Ann Arbor, MI", "capacity": 107601, "year_opened": 1927, "team": "Michigan Wolverines"},
    {"name": "Rožu Stadions", "location": "Pasadena, CA", "capacity": 88865, "year_opened": 1922, "team": "UCLA Bruins, Rose Bowl Game"},
    {"name": "Mercedes-Benz Stadions", "location": "Atlanta, GA", "capacity": 71000, "year_opened": 2017, "team": "Atlanta Falcons"},
    {"name": "SoFi Stadions", "location": "Inglewood, CA", "capacity": 70240, "year_opened": 2020, "team": "Los Angeles Rams, Los Angeles Chargers"},
    {"name": "Caesars Superdome", "location": "New Orleans, LA", "capacity": 73000, "year_opened": 1975, "team": "New Orleans Saints"},
    {"name": "Arrowhead Stadions", "location": "Kansas City, MO", "capacity": 76416, "year_opened": 1972, "team": "Kansas City Chiefs"},
    {"name": "Gillette Stadions", "location": "Foxborough, MA", "capacity": 65878, "year_opened": 2002, "team": "New England Patriots"},
    {"name": "Soldier Laukums", "location": "Chicago, IL", "capacity": 61500, "year_opened": 1924, "team": "Chicago Bears"},
    {"name": "Hard Rock Stadions", "location": "Miami Gardens, FL", "capacity": 65326, "year_opened": 1987, "team": "Miami Dolphins"},
    {"name": "FedExField", "location": "Landover, MD", "capacity": 82000, "year_opened": 1997, "team": "Washington Commanders"},
    {"name": "Levi's Stadions", "location": "Santa Clara, CA", "capacity": 68500, "year_opened": 2014, "team": "San Francisco 49ers"},
    {"name": "Bank of America Stadions", "location": "Charlotte, NC", "capacity": 74867, "year_opened": 1996, "team": "Carolina Panthers"},
    {"name": "Lincoln Financial Field", "location": "Philadelphia, PA", "capacity": 69296, "year_opened": 2003, "team": "Philadelphia Eagles"}
]


stadiums_df = pd.DataFrame(stadiums_data)


stadiums_df.to_sql("stadiums", engine, if_exists="replace", index=False)
    

@app.route('/stadiums')
def stadiums():
    loaded_df = pd.read_sql("SELECT * FROM stadiums", engine)
    return render_template('stadiums.html', stadiums=loaded_df)



@app.route('/popularity')
def popularity():
   return render_template('popularity.html', 
                         current_date=datetime.datetime.now())





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/cssfile')
def cssfile():
    css_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) 
               if f.endswith('.css')]
    return render_template('cssfile.html', css_files=css_files, current_date=datetime.datetime.now())

@app.route('/upload-css', methods=['GET', 'POST'])
def upload_css():
    if 'css_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['css_file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    
    return redirect(request.url)



@app.route('/activity')
def activity():
    dati = {
        'Nodarbību biežums': ['Regulāri', 'Reizēm', 'Reti', 'Pēc noskaņojuma', 'Daļēji', 'Nenodarbojas'],
        'Cilvēku skaits': [250, 180, 150, 200, 120, 100]  
    }

    df = pd.DataFrame(dati)

    
    plt.figure(figsize=(12, 6))
    sns.set_style('whitegrid')
    ax = sns.barplot(data=df, x='Nodarbību biežums', y='Cilvēku skaits', 
                    palette='viridis', edgecolor='black')
    
    plt.title('Sporta nodarbību biežums (1000 respondentu aptauja)', fontsize=16, pad=20)
    plt.xlabel('Nodarbību biežums', fontsize=12)
    plt.ylabel('Cilvēku skaits', fontsize=12)
    
    
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}", 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', 
                   xytext=(0, 10), 
                   textcoords='offset points',
                   fontsize=10)

    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    grafiks = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    
    return render_template('activity.html', 
                         grafiks=grafiks,
                         dati=df.to_dict('records'))
    
    
def get_sports_data():
   
    data = {
        'Sportists': ['Jānis Bērziņš', 'Pēteris Kalniņš', 'Anna Ozola', 'Līga Liepiņa', 
                     'Māris Smirnovs', 'Elīna Jansone', 'Kristaps Freimanis', 
                     'Dace Krūmiņa', 'Andris Zariņš', 'Inga Pētersone'],
        'Vecums': [22, 25, 19, 30, 27, 23, 28, 21, 26, 24],
        'Treniņi': [5, 3, 6, 4, 5, 4, 3, 6, 4, 5],
        'Rezultāts': [85, 62, 78, 65, 72, 80, 58, 75, 68, 82],
        'Sporta_veids': ['Futbols', 'Basketbols', 'Peldēšana', 'Volejbols', 
                        'Futbols', 'Peldēšana', 'Basketbols', 'Volejbols', 
                        'Futbols', 'Peldēšana']
    }
    return pd.DataFrame(data)

def create_plot():
    df = get_sports_data()
    
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    
    scatter = sns.scatterplot(
        data=df,
        x='Treniņi',
        y='Rezultāts',
        hue='Sporta_veids',
        size='Vecums',
        sizes=(50, 200),
        palette='viridis',
        alpha=0.8
    )
    
    
    plt.title('Sportistu rezultātu atkarība no treniņu skaita', pad=20)
    plt.xlabel('Treniņu skaits nedēļā', labelpad=10)
    plt.ylabel('Rezultāts (punkti)', labelpad=10)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    
    for i in range(len(df)):
        scatter.text(
            df['Treniņi'][i] + 0.1,
            df['Rezultāts'][i],
            df['Sportists'][i],
            fontsize=8,
            ha='left'
        )
    
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plot_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close()
    
    return plot_data

@app.route('/statistics')
def statistics():
    plot = create_plot()
    data = get_sports_data().to_dict('records')
    return render_template('statistics.html', plot=plot, sports_data=data)



sporta_viktorina = [
    {
        "jautajums": "Kura valstība uzvarēja 2018. gada FIFA Pasaules kausā?",
        "atbildes": ["Francija", "Horvātija", "Beļģija", "Anglija"],
        "pareiza": "Francija"
    },
    {
        "jautajums": "Kurš basketbolists ir visvairāk punktu guvis NBA vēsturē?",
        "atbildes": ["LeBrons Džeimss", "Kārlis Malons", "Kobe Braients", "Maikls Džordāns"],
        "pareiza": "LeBrons Džeimss"
    },
    {
        "jautajums": "Kāds ir olimpiskā rekorda laiks 100 metru skriešanā vīriešiem?",
        "atbildes": ["9.63 sekundes", "9.58 sekundes", "9.69 sekundes", "9.81 sekundes"],
        "pareiza": "9.63 sekundes"
    },
    {
        "jautajums": "Kurš tenisists ir uzvarējis visvairāk Grand Slam turnīros?",
        "atbildes": ["Rodžers Federers", "Novaks Džokovičs", "Rafael Nadals", "Pīts Samprass"],
        "pareiza": "Novaks Džokovičs"
    },
    {
        "jautajums": "Kura Latvijas hokeja komanda spēlē Kontinentālajā hokeja līgā (KHL)?",
        "atbildes": ["Dinamo Rīga", "HK Kurbads", "HK Liepāja", "HK Zemgale"],
        "pareiza": "Dinamo Rīga"
    },
    {
        "jautajums": "Kurā gadā Rīga organizēja Eiropas olimpiskos festivālu?",
        "atbildes": ["2015", "2013", "2017", "2019"],
        "pareiza": "2015"
    },
    {
        "jautajums": "Kāds ir olimpiskā rekorda rezultāts sieviešu vesera metienā?",
        "atbildes": ["82,29 m", "78,18 m", "80,85 m", "76,34 m"],
        "pareiza": "82,29 m"
    },
    {
        "jautajums": "Cik reizes Latvijas futbola izlase ir kvalificējusies Eiropas čempionātam?",
        "atbildes": ["1", "0", "2", "3"],
        "pareiza": "1"
    },
    {
        "jautajums": "Kurš futbolists ir visvairāk vārtu guvis FIFA Pasaules kausa finālturnīros?",
        "atbildes": ["Miroslavs Klose", "Ronaldo", "Gerds Millers", "Justs Fontēns"],
        "pareiza": "Miroslavs Klose"
    },
    {
        "jautajums": "Kurš latviešu basketbolists ir spēlējis NBA Visu Zvaigžņu spēlē?",
        "atbildes": ["Kristaps Porziņģis", "Dāvis Bertāns", "Rodions Kurucs", "Andris Biedriņš"],
        "pareiza": "Kristaps Porziņģis"
    },
    {
        "jautajums": "Kā sauc NBA čempionu titulu iegūstošo trofeju?",
        "atbildes": ["Larri O'Braiena balva", "NBA kauss", "Zelta bumba", "Čempionu gredzens"],
        "pareiza": "Larri O'Braiena balva"
    },
    {
        "jautajums": "Kurš no šiem tenisistiem ir uzvarējis visvairāk Wimbledonā?",
        "atbildes": ["Rodžers Federers", "Novaks Džokovičs", "Pīts Samprass", "Rafael Nadals"],
        "pareiza": "Rodžers Federers"
    },
    {
        "jautajums": "Kādu nosaukumu nes Latvijas tenisa čempionāta galvenā balva?",
        "atbildes": ["Vitolīna kauss", "Lielais Kristaps", "Rīgas balva", "Baltijas zvaigzne"],
        "pareiza": "Vitolīna kauss"
    },
    {
        "jautajums": "Kurā gadā Latvijas hokeja izlase pirmo reizi kvalificējās Olimpiskajām spēlēm?",
        "atbildes": ["2002", "2006", "2010", "2014"],
        "pareiza": "2002"
    },
    {
        "jautajums": "Cik ilga ir standarta hokeja spēles periods?",
        "atbildes": ["20 minūtes", "15 minūtes", "25 minūtes", "30 minūtes"],
        "pareiza": "20 minūtes"
    },
    {
        "jautajums": "Kā sauc sporta veidu, kurā sacenšas ar suņiem vilktām ragaviņām?",
        "atbildes": ["Suņu pajūgs", "Suņu braukšana", "Ziemeļu suņu sports", "Visi iepriekš minētie"],
        "pareiza": "Visi iepriekš minētie"
    },
    {
        "jautajums": "Kurā Latvijas pilsētā notiek ikgadējais 'Pasaules kauss velosipēdu polo'?",
        "atbildes": ["Rīga", "Liepāja", "Daugavpils", "Valmiera"],
        "pareiza": "Liepāja"
    },
    {
        "jautajums": "Kurš bija pirmais latviešu olimpietis?",
        "atbildes": ["Harijs Lūsis", "Jānis Daliņš", "Alfrēds Krūkliņš", "Pāvels Švecovs"],
        "pareiza": "Alfrēds Krūkliņš"
    },
    {
        "jautajums": "Kurā gadā Latvija pirmo reizi piedalījās ziemas olimpiskajās spēlēs?",
        "atbildes": ["1924", "1936", "1928", "1932"],
        "pareiza": "1924"
    },
    {
        "jautajums": "Kurš no šiem sportistiem ir uzstādījis pasaules rekordu 2023. gadā?",
        "atbildes": ["Arnis Rumbenieks (vesera mešana)", "Līna Mūze (augstlēkšana)", "Jānis Strenga (bobslejs)", "Dagnis Iļjins (daiļlēkšana)"],
        "pareiza": "Līna Mūze (augstlēkšana)"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Pārbaudām atbildi
        lietotaja_atbilde = request.form.get('atbilde')
        pareiza_atbilde = request.form.get('pareiza_atbilde')
        
        if lietotaja_atbilde == pareiza_atbilde:
            rezultats = "Pareizi! ✅"
        else:
            rezultats = f"Nepareizi! ❌ Pareizā atbilde: {pareiza_atbilde}"
        
        return render_template('quiz.html', 
                            rezultats=rezultats,
                            jauns_jautajums=True)
    
    # Ja GET pieprasījums, rādām jaunu jautājumu
    jautajums = random.choice(sporta_viktorina)
    atbildes = jautajums["atbildes"].copy()
    random.shuffle(atbildes)  
    
    return render_template('quiz.html',
                         jautajums=jautajums["jautajums"],
                         atbildes=atbildes,
                         pareiza_atbilde=jautajums["pareiza"],
                         rezultats=None)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Paroles nesakrīt!', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Lietotājvārds jau aizņemts', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('E-pasts jau reģistrēts', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Reģistrācija veiksmīga! Lūdzu, pierakstieties.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Pieteikšanās veiksmīga!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Nepareizs lietotājvārds vai parole', 'error')

    return render_template('auth/login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Jūs esat veiksmīgi izrakstījies', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        app.run(debug=True, port=5000)
