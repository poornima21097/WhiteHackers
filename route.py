from flask import Flask, render_template, request
import hack_code


app = Flask(__name__,template_folder='./')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/output', methods=['get'])
def output():
    email=request.args.get('email')
    #email="pio"
    name=request.args.get('names')
    if(name=="samyukta"):
        #url="https://www.instagram.com/p/BqHsWSslHjT/"
        url="https://www.instagram.com/p/Beah81GnUPn/"
    else:
        url="https://www.instagram.com/p/Bme9HdylVDh/"
    negative=hack_code.scrape(url,email)
    return render_template('result.html',negative=negative)


@app.route('/result.html')
def result():
    return render_template("result.html")



app.run(debug=True)
