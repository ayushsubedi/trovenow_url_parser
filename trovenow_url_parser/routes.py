from flask import render_template
from trovenow_url_parser import application
from trovenow_url_parser.forms import TroveForm
from trovenow_url_parser.models import ContentReader

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    form = TroveForm()
    url = form.url.data
    if url is None:
        url = "https://trovenow.com/"
    result = ContentReader.get_content(url)
    print (result)
    return render_template('demo.html', form=form, result=result)
