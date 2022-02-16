from flask import Flask, render_template, request, url_for, redirect
#from SharedConsts import UI_CONSTS
#from utils import logger

app = Flask(__name__)


@app.route('/display_error/<error_text>')
def display_error(error_text):
    return render_template('error_page.html', error_text=error_text)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        organism_name = request.form.get('text', None)
        print(organism_name)
        if organism_name is None:
            #logger.warning(f'organism_name not available')
            return redirect(url_for('display_error', error_text=UI_CONSTS.ALERT_USER_TEXT_INVALID_MAIL)) #change
        email_address = request.form.get('email', None)
        if email_address is None:
            #logger.warning(f'email_address not available')
            return redirect(url_for('display_error', error_text=UI_CONSTS.ALERT_USER_TEXT_INVALID_MAIL))
        #logger.info(f'organism name = {organism_name}, email_address = {email_address}')
    return render_template('home.html')