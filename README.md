# 📡 VERSION TRACKER

---

**Version-Tracker** is a Python Flask project checking version of your services and check online if new version is available. 

## 🪪 Access

---

[http://localhost:5000/](http://localhost:5000/)


## 🏁 Docker-compose

---

````yaml
version: "3.5"
services:
  webnmap:
    image: xenetis/version-tracker:latest
    container_name: version-tracker
    restart: unless-stopped
    environment:
      - TZ=Europe/Paris
    ports:
      - "5000:5000"
    volumes:
      - ./config.yml:/app/config.yml:ro
````

@todo

Or find it here: https://github.com/xenetis/docker-compose-examples/tree/main/version-tracker

## 🛠 Local Setup

---

### Install requirement
````bash
pip3 install -r requirements.txt
````

### Local run
````bash
python3 app/app.py
````

## 🎓 Usage

---

Create your **config.yml** like this: 

````yaml
tools:
  Cadvisor:
    name: "Cadvisor"
    type: "cadvisor"
    endpoint: "https://cadvisor.example.com"
  Gitlab-ce:
    name: "Gitlab Community"
    type: "gitlab-ce"
    endpoint: "http://gitlab-ce.example.com"
    headers:
      Private-Token: "oBNyxu2hw9TCVk39LYX8"
  Gitlab-ee:
    name: "Gitlab Enterprise"
    type: "gitlab-ee"
    endpoint: "http://gitlab-ee.example.com"
    headers:
      Private-Token: "9TCVk3oBNyxu2hw9LYX8"
  Glpi:
    name: "Glpi"
    type: "glpi"
    endpoint: "https://glpi.example.com"
    headers:
      Authorization: "user_token: n5JyTGkXqTUBxlOykCO9SfqV0lZIffoFKgdBujI2"
      App-Token: "W11fkaVWVBffhUS1uszBPHD6dZxCYMWorqFVSiQX"
  Grafana:
    name: "Grafana"
    type: "grafana"
    endpoint: "https://grafana.example.com"
  Node_exporter:
    name: "Node Exporter"
    type: "node_exporter"
    endpoint: "https://node-exporter.example.com"
  Prometheus:
    name: "Prometheus"
    type: "prometheus"
    endpoint: "https://prometheus.example.com"
    headers:
      Authorization: "Basic am9obkBleGFtcGxlLmNvbTphYmMxMjM="
  Matomo:
    name: "Matomo"
    type: "matomo"
    endpoint: "https://matomo.example.com"
    token: "435c9cb65313227916daf23527078c6b"
````



## 🗃 Versions

---

### v0.1.0

- Flask framework
- Use config.yml
- Dockerfile
- Docker build
- Docker-compose
- Cadvisor Plugin
- Gitlab-ce Plugin
- Gitlab-ee Plugin
- Glpi Plugin
- Grafana Plugin
- Matomo Plugin
- Node-exporter Plugin
- Prometheus Plugin


## 🗺 Roadmap

---

- Add more plugins
- Refactor plugins structure
- Add Jquery Ajax 
- Add datatables
- Group tools
- Cache save for latest version
- Multiple language


## 🏗 Third Parts

---

- [Flask](https://palletsprojects.com/p/flask/)
- [Docker](https://www.docker.com/)
