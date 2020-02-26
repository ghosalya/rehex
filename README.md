# TCGen

Trading Card Generator

## Installing

```
pip install -r requirements.txt
```

## Folder Structure

The code expects the current folder to have the following:

```
./data/
    somecards.json
./img/
    someimg.jpg
./layout/
    somelayout.png
```

## Generating Cards

1. cd `./examples/<name-of-game>`
2. run `tcgen generate`
3. result should be written in `./examples/<name-of-game>/res`