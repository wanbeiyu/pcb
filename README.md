# PCB

## 3rd_party libraries

<table>
<tr><th>Part Number</th><th>Download Link</th></tr>
<tr><td>2171790001</td><td>

[ul_2171790001.zip](https://app.ultralibrarian.com/details/b6ea985d-a10c-11eb-9033-0a34d6323d74/Molex-Connector-Corporation/2171790001)

<dl>
<dt>Symbol</dt><dd>Normal View, 2171790001 1</dd>
<dt>Footprint</dt><dd>Basic View, 2171790001_MOL</dd>
<dt>Select Your CAD Format</dt><dd>3D CAD Model: STEP, KiCAD v6+</dd>
<dt>Symbol Pin Ordering</dt><dd>Sequential</dd>
<dt>Footprint Units</dt><dd>English (mil)</dd>
</dl>
</td></tr>
<tr><td>AD8403ARUZ1-REEL</td><td>

[LIB_AD8403ARUZ1-REEL.zip](https://componentsearchengine.com/part-view/AD8403ARUZ1-REEL/Analog%20Devices)

</td></tr>
<tr><td>ADG801BRTZ-REEL7</td><td>

[LIB_ADG801BRTZ-REEL7.zip](https://componentsearchengine.com/part-view/ADG801BRTZ-REEL7/Analog%20Devices)

</td></tr>
<tr><td>AWSCR-12.00CELA-C33-T3</td><td>

[LIB_AWSCR-12.00CELA-C33-T3.zip](https://componentsearchengine.com/part-view/AWSCR-12.00CELA-C33-T3/ABRACON)

</td></tr>
<tr><td>BSS138</td><td>

[LIB_BSS138.zip](https://componentsearchengine.com/part-view/BSS138/onsemi)

</td></tr>
<tr><td>DS4424N+T&R</td><td>

[LIB_DS4424N+T&R.zip](https://componentsearchengine.com/part-view/DS4424N%2BT%26R/Analog%20Devices)

</td></tr>
<tr><td>MCP659-E_ML</td><td>

[LIB_MCP659-E_ML.zip](https://componentsearchengine.com/part-view/MCP659-E%2FML/Microchip)

</td></tr>
<tr><td>NCP167AMX330TBG</td><td>

[ul_NCP167AMX330TBG.zip](https://app.ultralibrarian.com/details/5d94e4bf-e68c-11ea-b55a-0a34d6323d74/onsemi/NCP167AMX330TBG)

<dl>
<dt>Symbol</dt><dd>Normal View, NCP167AMX330TBG 1</dd>
<dt>Footprint</dt><dd>Basic View, XDFN4_1X1_711AJ_ONS</dd>
<dt>Select Your CAD Format</dt><dd>KiCAD v6+</dd>
<dt>Symbol Pin Ordering</dt><dd>Sequential</dd>
<dt>Footprint Units</dt><dd>English (mil)</dd>
</dl>
</td></tr>
<tr><td>SK6805-EC15</td><td>

[LIB_SK6805-EC15.zip](https://componentsearchengine.com/part-view/SK6805-EC15/Shenzhen%20Normand%20Electronic)

</td></tr>
<tr><td>TC42X-2-102E</td><td>

[LIB_TC42X-2-102E.zip](https://componentsearchengine.com/part-view/TC42X-2-102E/Bourns)

</td></tr>
<tr><td>W25Q16JVUXIQ</td><td>

[LIB_W25Q16JVUXIQ.zip](https://componentsearchengine.com/part-view/W25Q16JVUXIQ/Winbond)

</td></tr>
<tr><td>XCL103D503CR-G</td><td>

[LIB_XCL103D503CR-G.zip](https://componentsearchengine.com/part-view/XCL103D503CR-G/Torex)

</td></tr>
</table>

## 部品選定メモ

### 電源

New 3DS LLには5V以上の電源を引き出せるTPはない（電源接続時4.38V、バッテリー駆動時3.92V、消耗時は3.1V程度まで低下）。5Vに昇圧→3.3Vに降圧する。

特にコイル一体型のICが実装面積が小さくなる。XCL103のI<sub>LIM</sub>で十分と判断した。

<table>
<tr>
<th>品番</th>
<th>詳細</th>
</tr>
<tr>
<td>XCL103D503CR-G</td>
<td>

- PWM/PFM自動切替制御
- Complete Output Disconnect
- Output Voltage: 5.0V
- I<sub>LIM</sub>: 1.3A

</td>
</tr>
<tr>
<td>XCL105A501H2-G</td>
<td>

- PWM/PFM制御
- Complete Output Disconnect
  - A・Dから選択で、Aしか在庫がない<br>https://www.digikey.jp/short/0qb0394h<br>https://mou.sr/4bJGSOZ
- Output Voltage: 5.0V
- I<sub>LIM</sub>: 2.42A

</td>
</tr>
</table>

以前はRaspberry Pi Debug Probeを参考に[AP2112K-3.3TRG1](https://www.digikey.jp/ja/products/detail/diodes-incorporated/AP2112K-3-3TRG1/4470746)を使用していた。

| 機能                     | 値         |
| ------------------------ | ---------- |
| 出力構成                 | ポジティブ |
| 出力タイプ               | 固定       |
| 電圧 - 出力（最小/固定） | 3.3V       |
| 電流 - 出力              | 600mA      |

600mA以上出ていればどれでもよさそうだ。[NCP167AMX330TBG](https://www.digikey.jp/ja/products/detail/onsemi/NCP167AMX330TBG/9169759)が十分小さい。

### 発振回路

[AEL X12M000000S096](https://abracon.com/datasheets/AEL-Crystals/PN/X12M000000S096.pdf)が元の水晶[^1]。

[^1]: https://forums.raspberrypi.com/viewtopic.php?t=349741

- 12MHz
- ESR：50Ωに寄せる
- 内蔵コンデンサ
- セラミックタイプ

[検索結果](https://www.digikey.jp/short/p5qp35qr)

Operating Temperature（`CELA`は85度まで、`CELB`は125度まで）、静電容量（33pF／10pF）を選択する。[Hardware design with RP2040](https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf)では27pFを使っているので、より近い33pFを選択する。

[AWSCR-12.00CELA-C33-T3](https://www.digikey.jp/short/5r7mjdv3)

## フルカラーLED

いわゆるNeoPixel、WS2812BとSK6812（12mA：たぶんより明るい）/SK6805（5mA）は同じものらしい[^2]。前者がオリジナル、後者がクローン。

[^2]: https://romly.com/blog/neopixel_variation/

SK6805-EC15が1.5mm角。
