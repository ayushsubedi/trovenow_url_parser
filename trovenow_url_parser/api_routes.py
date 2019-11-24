from flask import render_template, request, jsonify
from trovenow_url_parser import application
from trovenow_url_parser.models import ContentReader

@application.route('/api/get_content', methods=['GET', 'POST'])
def get_content():
    if request.method == 'POST':
        url = request.form['url']
        summary = request.form.get('summary', 'no')
    else:
        url = request.args.get('url', None)
        summary = 'yes'
    result = ContentReader.get_content(url, summary=='yes')
    return jsonify(result)

@application.route('/api/get_trending', methods=['GET'])
def get_trending():
    result = ContentReader.get_trending()
    return jsonify(result)    