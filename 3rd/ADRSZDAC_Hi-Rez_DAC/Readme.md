# ADRSZDAC ラズパイハイレゾDAC説明書

### 初期セットアップ方法

 1. /boot/config.txtに、以下の行を追記します。  
dtparam=i2s=on  
dtoverlay=hifiberry-dacplus,24db_digital_gain  

 2. /boot/config.txtの以下の行をコメントアウト(先頭に#を付ける)します。  
dtparam=audio=on  
↓  
\#dtparam=audio=on  

コマンドラインによる音声再生・音量調節  

### 音声再生(wavのみ)
```sh
aplay --device=hw:0,0 ＜音声ファイル名.wav＞  
```
### 音声再生(mp3,etc...)
```sh
# sudo apt install mplayer
mplayer -quiet -ao alsa:device=hw=0.0 ＜音声ファイル名.mp3＞  
```
### 音量調節
```sh
amixer set 'Digital' ＜音量:パーセンテージ＞%
```
