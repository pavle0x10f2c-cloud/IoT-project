# Hand LED Controller

Control an LED strip with your hand using a webcam — no touch required. Hover your index finger over the circles on screen to set the brightness level, which gets sent to an ESP32 over UDP.

## Requirements

- Linux + webcam
- ESP32 in Access Point mode on `192.168.4.1`, UDP port `8888`
- Python 3.10+

## Setup
```bash
git clone https://github.com/pavle0x10f2c-cloud/IoT-project.git
cd IoT-project
cp .env.example .env
pip3 install -r requirements.txt --break-system-packages
cd app
python3 main.py
```

## Controls

| Key | Action |
|-----|--------|
| `Q` | Quit |
| `Y` | Show hand skeleton |
| `N` | Hide hand skeleton |

## Run with Docker (Linux only)
```bash
xhost +local:docker
docker compose up --build
```

To stop:
```bash
docker compose down
```

## Troubleshooting

**mediapipe has no attribute 'solutions'** → `pip3 install mediapipe==0.10.18 --break-system-packages --force-reinstall`

**NumPy crash** → `pip3 install "numpy<2" --break-system-packages --force-reinstall`

**ESP not available** → make sure you're connected to the ESP's WiFi network

**If your webcam is not at `/dev/video0`, check with:
```bash
ls /dev/video*
```
Then update `docker-compose.yml` accordingly
