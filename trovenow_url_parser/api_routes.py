from flask import render_template, request, jsonify
from trovenow_url_parser import application
from trovenow_url_parser.models import ContentReader

@application.route('/api/get_content', methods=['GET', 'POST'])
def get_content():
    if request.method == 'POST':
        url = request.form['url']
    else:
        url = request.args.get('url', None)
    result = ContentReader.get_content(url)
    return jsonify(result)