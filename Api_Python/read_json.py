import json
import csv
import typer

app=typer.Typer()


@app.command()
def read_json(file):
    with open(file,'r',encoding='utf-8') as j:
        data=json.load(j)
        for i in data['Meta Data']['2. Symbol']:
            print(i,end="")
        print()
        

if __name__=="__main__":
    app()
