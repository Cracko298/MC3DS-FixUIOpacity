# MC3DS-FixUIOpacity
- A tool that Changes Opacity in MC3DS Textures.

## Usage:
```
python FixUIOpacity.py MySuperCoolAndVeryAwesomeTextureExampleThatIForgotTheNameTo.3dst
```

## Building
- Building 'getTextureInfo.cpp'.
```
g++ -shared -o getTextureInfo.dll -Os -O3 -flto -s FormatFind.cpp
```
