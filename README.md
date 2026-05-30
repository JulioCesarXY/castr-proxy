# 📺 Castr HLS IPTV Proxy

[![Deploy to Render](https://render.com/images/deploy-to-render.svg)](https://render.com)

Um servidor proxy leve desenvolvido em **Python (Flask)** para contornar restrições de CORS, referer e travas da CDN Akamai em transmissões ao vivo da plataforma **Castr**. Ele converte streams HLS protegidos em links limpos e compatíveis com qualquer player de IPTV convencional.

---

## 🚀 Como o Projeto Funciona

Grandes plataformas de streaming utilizam proteções de cabeçalho (`Referer` e `Origin`) e tokens de CDN (como Akamai Edgesuite) para impedir que seus links sejam reproduzidos fora do player oficial. 

Este proxy atua como um intermediário em nuvem:
1. O seu player de IPTV faz uma requisição padrão para este Proxy.
2. O Proxy intercepta o pedido, injeta os cabeçalhos de segurança corretos e faz o download dos manifestos (`.m3u8`) e segmentos (`.fmp4`).
3. O Proxy reescreve as rotas internas e entrega o sinal "mastigado" e limpo de travas para o seu player.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Flask** (Micro-framework web)
* **Requests** (Para manipulação e injeção de cabeçalhos HTTP)
* **Gunicorn** (Servidor WSGI para produção)

---

## 📦 Como Instalar e Rodar Localmente

Se quiser rodar o projeto na sua própria máquina antes de subir para a nuvem:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   cd NOME_DO_REPOSITORIO
