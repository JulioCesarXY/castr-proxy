from flask import Flask, Response, request
import requests
import os

app = Flask(__name__)

HEADERS = {
    "Referer": "https://player.castr.com/",
    "Origin": "https://player.castr.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

BASE_URL = "https://stream.castr.com/5bc1431aaa00ea389fcfb163/live_c465a13052e111f1947233f0202499f0"

@app.route('/live.m3u8')
def proxy_master():
    url = f"{BASE_URL}/index.fmp4.m3u8"
    res = requests.get(url, headers=HEADERS)
    content = res.text
    content = content.replace("tracks-", f"https://{request.host}/tracks-")
    return Response(content, mimetype='application/x-mpegURL')

@app.route('/<path:subpath>')
def proxy_subtracks(subpath):
    url = f"{BASE_URL}/{subpath}"
    if subpath.endswith('.fmp4'):
        res = requests.get(url, headers=HEADERS, stream=True)
        return Response(res.iter_content(chunk_size=1024), content_type=res.headers.get('Content-Type'))
    
    res = requests.get(url, headers=HEADERS)
    content = res.text
    content = content.replace("seg-", f"https://{request.host}/{subpath.rsplit('/', 1)[0]}/seg-")
    return Response(content, mimetype='application/x-mpegURL')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
