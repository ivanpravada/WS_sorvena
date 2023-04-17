# WS_sorvena
HomeWork_WS_sorvena

RUN PROXY:
uvicorn main:app --reload --port XXXX

RUN WS_1:
uvicorn ws_1:app --reload --port YYYY

RUN WS_2:
uvicorn ws_2:app --reload --port ZZZZ
