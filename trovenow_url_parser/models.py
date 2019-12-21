from newspaper import Article
import newspaper
import validators
import requests
import mimetypes
import json
from gensim.summarization import summarize


class ContentReader:
    @staticmethod
    def get_trending():
        url = ('https://newsapi.org/v2/top-headlines?'
        'country=us&'
        'apiKey=bcaaf0d008994d818672b2c1141be98b')
        response = requests.get(url)
        popular_articles = {'articles': json.loads(response.text).get('articles')}
        popular_url_topics = {'popular_urls': newspaper.popular_urls(), 'hot_topics': newspaper.hot()}
        return {**popular_articles, **popular_url_topics}

    @staticmethod
    def get_content(external_sites_url, summary=False):
        if not external_sites_url.startswith('http'):
            external_sites_url = 'http://'+external_sites_url
            r = requests.get(external_sites_url)
            external_sites_url = r.url
        if (validators.url(external_sites_url)):
            try:
                response = requests.get(external_sites_url)
                content_type = response.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                if ((extension is not None) and extension != ".htm"):
                    title = external_sites_url.split('/')[-1]
                    _type = title.split('.')[-1].lower()
                    image_list = ['jpeg', 'jpg', 'gif', 'png']
                    if (_type in image_list): 
                        _type='Image'
                        return {'code_content': 204, 'title': title, 'type': _type, 'top_image': external_sites_url, 'message:': "content is not html"}
                    elif (_type=='pdf'):_type="PDFs"
                    return {'code_content': 204, 'title': title, 'type': _type, 'message:': "content is not html"}
                article = Article(external_sites_url, keep_article_html=False)
                article.download()
                article.parse()
                new_keywords = []
                article_summary = ''
                if (summary):
                    article_summary = summarize(article.text, word_count=150)
                    for word in article.keywords:
                        if (len(word) > 5):
                            new_keywords.append(word)
                try:
                    _type = article.meta_data.get("og").get("type").lower()
                    if ('video' in _type): _type='Video'
                    elif (_type=='article'): _type="Article"
                    else: _type = "Website"       
                except:
                    _type = "Website"
                summary_flag = 1 if (len(article_summary)>130) else 0 
                return {'summary_flag': summary_flag, 'url':external_sites_url, 'code_content': 200, 'title': article.title, 'movies': article.movies, 'description': article.meta_description, 'type': _type, 'top_image': article.top_image, 'authors': article.authors, 'publish_date': article.publish_date, 'text': article.article_html, 'summary': article_summary, 'keywords': new_keywords}
            except Exception as e:

                # Slack webhook for tmp folder missing issue 
                if "tmp" in str(e):
                    response = requests.post('https://hooks.slack.com/services/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', headers={'Content-type': 'application/json',}, data=json.dumps({'text':'restart: '+external_sites_url}))
                return {'code_content': 500, 'error': str(e)}
        return {'code_content': 404, 'msg': 'malinformed URL'}


