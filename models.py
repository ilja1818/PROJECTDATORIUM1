import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from matplotlib.ticker import FuncFormatter


style.use('seaborn-v0_8-darkgrid')


def create_and_populate_database():
    conn = sqlite3.connect('sports_popularity.db')
    cursor = conn.cursor()
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS sports 
                      (id INTEGER PRIMARY KEY, name TEXT, popularity INTEGER, year INTEGER)''')
    
    
    cursor.execute("SELECT COUNT(*) FROM sports")
    if cursor.fetchone()[0] == 0:
        
        sports_data = [
            ('Futbols', 85, 2023),
            ('Basketbols', 60, 2023),
            ('Krikets', 55, 2023),
            ('Teniss', 50, 2023),
            ('Volejbols', 45, 2023),
            ('Peldēšana', 42, 2023),
            ('Golfs', 40, 2023),
            ('Beisbols', 38, 2023),
            ('Regbijs', 35, 2023),
            ('Hokejs', 33, 2023),
            ('Bokss', 30, 2023),
            ('Badmintons', 28, 2023),
            ('Vieglatlētika', 27, 2023),
            ('Riteņbraukšana', 25, 2023),
            ('Rokasbumba', 22, 2023),
            ('Skvošs', 20, 2023),
            ('Galda teniss', 18, 2023),
            ('Cīņas sports', 15, 2023),
            ('Svarcelšana', 12, 2023),
            ('Paukotāja sports', 10, 2023)
        ]
        
        
        cursor.executemany("INSERT INTO sports (name, popularity, year) VALUES (?, ?, ?)", sports_data)
        conn.commit()
    
    conn.close()


def get_sports_data():
    conn = sqlite3.connect('sports_popularity.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, popularity FROM sports ORDER BY popularity DESC")
    data = cursor.fetchall()
    
    conn.close()
    return data


def popularity_formatter(x, pos):
    return f'{int(x)}%'


def create_popularity_chart():
    data = get_sports_data()
    sports = [item[0] for item in data]
    popularity = [item[1] for item in data]
    
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(sports)))
    
    
    plt.figure(figsize=(14, 8))
    
   
    bars = plt.barh(sports, popularity, color=colors)
    
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1, bar.get_y() + bar.get_height()/2, 
                 f'{width}%', 
                 va='center', ha='left', fontsize=10)
    
   
    plt.title('Sporta veidu popularitāte 2023. gadā', fontsize=16, pad=20)
    plt.xlabel('Popularitātes līmenis (%)', fontsize=12)
    plt.ylabel('Sporta veids', fontsize=12)
    plt.xlim(0, 100)
    
    
    plt.gca().xaxis.set_major_formatter(FuncFormatter(popularity_formatter))
    
   
    plt.tight_layout()
    
    
    plt.text(0.95, 0.02, 'Avots: aptuveni dati', 
             transform=plt.gcf().transFigure, 
             fontsize=9, color='gray', ha='right', va='bottom', alpha=0.7)
    
    
    plt.savefig('sports_popularity.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    create_and_populate_database()
    create_popularity_chart()