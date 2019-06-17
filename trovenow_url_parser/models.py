from newspaper import Article
import validators
import requests
import mimetypes

class ContentReader:
    @staticmethod
    def get_content(external_sites_url):
        if (validators.url(external_sites_url)):
            try:
                response = requests.get(external_sites_url)
                content_type = response.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                if ((extension is not None) and extension != ".htm"):
                    return {'code_content': 204, 'title': external_sites_url.split('/')[-1], 'error:': "content is not html"}
                article = Article(external_sites_url, keep_article_html=True)
                article.download()
                article.parse()
                article.nlp()
                new_keywords = []
                for word in article.keywords:
                    if (len(word) > 5):
                        new_keywords.append(word)
                try:
                    _type = article.meta_data.get("og").get("type")
                except:
                    _type = None
                return {'code_content': 200, 'title': article.title, 'movies': article.movies, 'description': article.meta_description, 'type': _type, 'text': article.article_html, 'top_image': article.top_image, 'authors': article.authors, 'publish_date': article.publish_date, 'summary': article.summary, 'keywords': new_keywords}
            except Exception as e:
                return {'code_content': 500, 'error': str(e)}
        return {'code_content': 404, 'msg': 'malinformed URL'}