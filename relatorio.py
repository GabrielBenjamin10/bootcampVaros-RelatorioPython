from dotenv import load_dotenv
import os
import pandas as pd
import datetime as dt
import yfinance as yf
import mplcyberpunk
from email.message import EmailMessage
from matplotlib import pyplot as plt
import smtplib


def decimaltoPct(value):
    Valor = round(value*100, 2)
    return Valor


ativos = ["^BVSP", "BRL=X"]
diaDeHoje = dt.datetime.now()
dataLimite = diaDeHoje - dt.timedelta(days=365)
dadosMercado = yf.download(ativos, dataLimite, diaDeHoje)

dadosFechamento = dadosMercado['Adj Close']
dadosFechamento.columns = ['Dolar', 'IBOVESPA']
dadosFechamento = dadosFechamento.dropna()

fechamentoMensal = dadosFechamento.resample('M').last()
fechamentoAnual = dadosFechamento.resample('Y').last()

retornopctAnual = fechamentoAnual.pct_change().dropna()
retornopctMensal = fechamentoMensal.pct_change().dropna()
retornopctDiario = dadosFechamento.pct_change().dropna()

retornoUltimoAnoDolar = retornopctAnual.iloc[-1, 0]
retornoUltimoAnoIbov = retornopctAnual.iloc[-1, 1]

retornoUltimoMesDolar = retornopctMensal.iloc[-1, 0]
retornoUltimoMesIbov = retornopctMensal.iloc[-1, 1]

retornoUltimoDiaDolar = retornopctDiario.iloc[-1, 0]
retornoUltimoDiaIbov = retornopctDiario.iloc[-1, 1]

retornoUltimoAnoDolar = decimaltoPct(retornoUltimoAnoDolar)
retornoUltimoAnoIbov = decimaltoPct(retornoUltimoAnoIbov)

retornoUltimoMesDolar = decimaltoPct(retornoUltimoMesDolar)
retornoUltimoMesIbov = decimaltoPct(retornoUltimoMesIbov)

retornoUltimoDiaDolar = decimaltoPct(retornoUltimoDiaDolar)
retornoUltimoDiaIbov = decimaltoPct(retornoUltimoDiaIbov)


plt.style.use('cyberpunk')

dadosFechamento.plot(y='IBOVESPA', use_index=True, legend=False)
plt.title('IBOVESPA')
# plt.savefig('ibov.png')

dadosFechamento.plot(y='Dolar', use_index=True, legend=False)
plt.title('DOLAR')
# plt.savefig('dolar.png')


load_dotenv()

senha = os.environ.get('password')
email = 'gabriel.gaspargbg@gmail.com'

msg = EmailMessage()
msg['subject'] = 'Relatório IBOV e Dolár com python'
msg['from'] = 'gabriel.gaspargbg@gmail.com'
msg['to'] = 'gustasbenjamin@gmail.com'
msg.set_content(f''' 
Prezados, segue relatório juntamente com gráficos em anexo

Dolar:

O dolar teve uma variação anual de {retornoUltimoAnoDolar}%
Uma variação mensal de {retornoUltimoMesDolar}%
No último dia útil {retornoUltimoDiaDolar}%

IBOV:

A IBOV teve uma variação anual de {retornoUltimoAnoIbov}
Uma variação mensal de {retornoUltimoMesIbov}
No último dia útil {retornoUltimoDiaIbov}

Atenciosamente,

Gabriel

''')


with open('ibov.png','rb') as content_files:
    content = content_files.read()
    msg.add_attachment(content,maintype='application',subtype='png', filename='ibov.png' )



with open('dolar.png','rb') as content_files:
    content = content_files.read()
    msg.add_attachment(content,maintype='application',subtype='png', filename='dolar.png' )


with smtplib.SMTP_SSL('SMTP.gmail.com',465) as smtp:
    smtp.login(email,senha)
    smtp.send_message(msg)
    