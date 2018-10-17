# ADRSZDAC ラズパイハイレゾDAC説明書

## 初期セットアップ方法

 1. /boot/config.txtに、以下の行を追記します。  
dtparam=i2s=on  
dtoverlay=hifiberry-dacplus,24db_digital_gain  

 2. /boot/config.txtの以下の行をコメントアウト(先頭に#を付ける)します。  
dtparam=audio=on  
↓  
\#dtparam=audio=on  
## 再起動後、デバイス確認
```sh
aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: sndrpihifiberry [snd_rpi_hifiberry_dacplus], device 0: HiFiBerry DAC+ HiFi pcm512x-hifi-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
## コマンドラインによる音声再生・音量調節  

### 音声再生(wav)
```sh
aplay ＜音声ファイル名.wav＞  
```
### 音声再生(mp3,flac,etc...)
```sh
# sudo apt install mplayer
mplayer ＜音声ファイル名＞  
# sudo apt install vlc
vlc --play-and-exit ＜音声ファイル名＞  
```
### 音量調節
```sh
amixer set 'Digital' ＜音量:パーセンテージ＞%
```
