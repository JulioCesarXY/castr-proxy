from flask import Flask, Response, request
import requests
import os

app = Flask(__name__)

# Cabeçalhos obrigatórios para burlar as travas da Castr/Akamai
HEADERS = {
    "Referer": "https://player.castr.com/",
    "Origin": "https://player.castr.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

BASE_URL = "https://stream.castr.com/5bc1431aaa00ea389fcfb163/live_c465a13052e111f1947233f0202499f0"

@app.route('/live.m3u8')
def proxy_master():
    """Rota principal: Pega a Master Playlist e reescreve os caminhos"""
    url = f"{BASE_URL}/index.fmp4.m3u8"
    res = requests.get(url, headers=HEADERS)
    content = res.text
    content = content.replace("tracks-", f"https://{request.host}/tracks-")
    
    response = Response(content, mimetype='application/x-mpegURL')
    response.headers["Access-Control-Allow-Origin"] = "*"  # Libera o CORS para navegadores
    return response

@app.route('/<path:subpath>')
def proxy_subtracks(subpath):
    """Rota secundária: Trata sub-playlists e faz streaming dos blocos de vídeo .fmp4"""
    url = f"{BASE_URL}/{subpath}"
    
    # Se for um pedaço de vídeo bruto (.fmp4), faz streaming dos bytes
    if subpath.endswith('.fmp4'):
        res = requests.get(url, headers=HEADERS, stream=True)
        response = Response(res.iter_content(chunk_size=1024), content_type=res.headers.get('Content-Type'))
        response.headers["Access-Control-Allow-Origin"] = "*"  # Libera o CORS para o vídeo
        return response
    
    # Se for uma sub-playlist interna, reescreve o caminho dos segmentos
    res = requests.get(url, headers=HEADERS)
    content = res.text
    content = content.replace("seg-", f"https://{request.host}/{subpath.rsplit('/', 1)[0]}/seg-")
    
    response = Response(content, mimetype='application/x-mpegURL')
    response.headers["Access-Control-Allow-Origin"] = "*"  # Libera o CORS para a playlist interna
    return response

if __name__ == '__main__':
    # Configuração de porta dinâmica exigida pelo Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
