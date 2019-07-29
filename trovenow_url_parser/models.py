from newspaper import Article
import validators
import requests
import mimetypes

class ContentReader:
    @staticmethod
    def get_content(external_sites_url):
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
                    if (_type in image_list): _type='Image'
                    elif (_type=='pdf'):_type="PDFs"
                    return {'code_content': 204, 'title': title, 'type': _type, 'error:': "content is not html"}
                article = Article(external_sites_url, keep_article_html=False)
                article.download()
                article.parse()
                try:
                    _type = article.meta_data.get("og").get("type").lower()
                    if ('video' in _type): _type='Video'
                    elif (_type=='article'): _type="Article"       
                except:
                    _type = None
                return {'code_content': 200, 'title': article.title, 'movies': article.movies, 'description': article.meta_description, 'type': _type, 'top_image': article.top_image, 'authors': article.authors, 'publish_date': article.publish_date}
            except Exception as e:
                return {'code_content': 500, 'error': str(e)}
        return {'code_content': 404, 'msg': 'malinformed URL'}