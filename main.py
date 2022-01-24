import discord
import os
from keep_alive import keep_alive
from replit import db

import updateCrypto

client = discord.Client()

db["GreenAlert"] = False
db["RedAlert"] = False
db["Ready"] = False


def addApelido(message):
  apelido = message.content[9:]

  if "apelidoslower" not in db.keys():
    db["apelidoslower"] = []
  if apelido.lower not in db["apelidoslower"]:    
    if "apelidos" in db.keys():
      if apelido.lower() in db["apelidos"]:
        return 'Figurinha repetida não tem graça'
      else:
        apelidos = db["apelidos"]
        apelidos.append(apelido)
        db["apelidos"] = apelidos
        return f'Parabéns! "{apelido}" foi adicionado ao banco de dados!'
    else:
      db["apelidos"] = [apelido]
      return f'Parabéns! "{apelido}" foi adicionado ao banco de dados!'
  else:
    return 'Figurinha repetida não tem graça'
    

def delApelido(message):
  apelido = message.content[8:]
  if "apelidos" in db.keys():
    apelidos = db["apelidos"]
    if apelido in apelidos:
      apelidos.remove(apelido)
      db["apelidos"] = apelidos
      return f'Que pena! "{apelido}" foi removido do banco de dados'
    else:
      return f'Esse nome nem tinha sido inventado ainda...'
  else:
    return f'Por algum motivo o banco de dados inteiro foi deletado 🤔'


@client.event
async def on_ready():
  print(f'{client.user} is online')
  db["Ready"] = True


@client.event
async def on_message(message):
  if message.author == client.user:
      return # Se o bot que enviou a mesagem, fazer nada


  elif message.content.startswith('gostosa'):
      await message.channel.send('Eu sei')

  elif message.content.startswith('quem sou eu'):
      await message.channel.send(f'{message.author.display_name}')
      print(message.author.id)

  elif 'quem te criou' in message.content.lower():
    await message.channel.send('Em 14/06/2020 Catvt me concebeu, mas apenas em 2022 ganhei consciência')
  
  elif message.content.startswith('!ajuda') or message.content.startswith('!ragazza'):
    myEmbed = discord.Embed(title="Converse comigo!", description="Aqui estao os principais comandos:", color=0x900AA2)
    myEmbed.set_image(url="https://wallpapercave.com/wp/wp6309878.jpg")
    myEmbed.add_field(name="!ajuda", value="teste")
    myEmbed.add_field(name="!gonçajuda", value="veja os goncomandos")
    myEmbed.add_field(name="!crypto", value="seja um cryptokid")
    await message.channel.send(embed=myEmbed)

  elif message.content.startswith('!gonçajuda'):
    myEmbed = discord.Embed(title="Nos ajude nessa causa universal!", description="Nosso banco de nickapelidos sempre aceita ajudas.", color=0x86A709)
    # myEmbed.set_image(url="colocar nick gravido")
    myEmbed.add_field(name="!gonçall", value="Te mostro tudo que temos até agora")
    myEmbed.add_field(name="!gonçadd", value="Adiciono sua ideia")
    myEmbed.add_field(name="!gondel", value="Deleto um nome", inline=False)
    myEmbed.set_footer(text="nenhum nicholas foi ferido no processo")
    await message.channel.send(embed=myEmbed)

  elif message.content.startswith('!crypto'):
    myEmbed = discord.Embed(title="API de cryptomoedas", description="A qualquer momento pode me perguntar sobre o mercado crypto!", color=0x0D4F88)
    myEmbed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/cryptocoins/227/ETH-512.png")
    myEmbed.add_field(name="Moedas:", value="Bitcoin, Ethereum & Thetan Coin")
    myEmbed.add_field(name="Comandos básicos:", value="!btc !eth !thc")
    myEmbed.add_field(name="Comandos avançados:", value="Digite !avançado para conhecê-los", inline=False)
    await message.channel.send(embed=myEmbed)
  
  elif message.content.startswith('!avançado'):
    myEmbed = discord.Embed(title="Comandos disponíveis", description="Utilize !moeda comandoAvançado. Ex: !btc percent_change_24h", color=0x0D4F88)
    myEmbed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/cryptocoins/227/ETH-512.png")
    myEmbed.set_footer(text="Dados coletados do CoinMarketCap.")
    myEmbed.add_field(name="Moedas:", value="!btc !eth !thc !thg")
    myEmbed.add_field(name="Preço:", value="price")
    myEmbed.add_field(name="Volume Diário:", value="volume_24h", inline=False)
    myEmbed.add_field(name="Variação do volume hoje:", value="volume_change_24h")
    myEmbed.add_field(name="Variação de preço 1h:", value="percent_change_1h", inline=False)
    myEmbed.add_field(name="Variação de preço 24h:", value="percent_change_24h")
    myEmbed.add_field(name="Variação de preço 7d:", value="percent_change_7d", inline=False)
    myEmbed.add_field(name="Variação de preço 30d:", value="percent_change_30d")
    myEmbed.add_field(name="Capitalização de mercado: :", value="market_cap", inline=False)
    myEmbed.add_field(name="Dominância de capitalização de mercado:", value="market_cap_dominance")
    myEmbed.add_field(name="Capitalização de mercado diluída:",value="fully_diluted_market_cap", inline=False)
    myEmbed.add_field(name="Última atualização:",value="!last_updated")
    await message.channel.send(embed=myEmbed)
  
  elif message.content.startswith('!gonçadd'):
    resposta = addApelido(message)
    await message.channel.send(resposta)
    if resposta[0] == 'F':
      await message.add_reaction("👎")
    print(db["apelidos"])

  elif message.content.startswith('!gondel'):
    resposta = delApelido(message)
    await message.channel.send(resposta)
    print(db["apelidos"])
  
  elif message.content.startswith('!gonçall'):
    if "apelidos" in db.keys():
      resposta = f'Até o momento, alcançamos {len(db["apelidos"])} dados colaborativos!'
      for i, name in enumerate(db["apelidos"]):
        resposta += f'\n{i+1}- {name}'
      await message.channel.send(resposta)
      print(db["apelidos"])

  cryptoChat = client.get_guild(130408666439352320).get_channel(935293610432290827)
  if (message.channel == cryptoChat):
    if message.content.startswith('!thc'):
      if len(message.content) <= 5:
        print(message.content)
        await message.channel.send(f'THC price: ${db["THCDATA"]["price"]}')
      else:
        param = message.content[5:]
        await message.channel.send(f'THC {param}: ${db["THCDATA"][param]}')
    
    elif message.content.startswith('!thg'):
      if len(message.content) <= 5:
        print(message.content)
        await message.channel.send(f'THG price: ${db["THGDATA"]["price"]}')
        print(message.channel)
      else:
        param = message.content[5:]
        await message.channel.send(f'THG {param}: {db["THGDATA"][param]}')

    elif message.content.startswith('!btc'):
      if len(message.content) <= 5:
        await message.channel.send(f'BTC price: ${db["BTCDATA"]["price"]}')
      else:
        param = message.content[5:]
        await message.channel.send(f'BTC {param}: {db["BTCDATA"][param]}')
    
    elif message.content.startswith('!eth'):
      if len(message.content) <= 5:
        await message.channel.send(f'THC price: ${db["ETHDATA"]["price"]}')
      else:
        param = message.content[5:]
        await message.channel.send(f'ETH {param}: {db["ETHDATA"][param]}')
    elif message.content.startswith('!last_updated'):
      await message.channel.send(f'{db["lastUpdate"]}')

  if message.author.display_name == 'JP_Regazzi':
    #await message.add_reaction("👏")
    if message.content.startswith('!delDB'):
      del db["apelidos"]

  
async def fireAlarm():
  while True:
    try:
      await updateCrypto.asyncio.sleep(20)
      print(f'Tried to fire the alarm\nGreen Alert: {db["GreenAlert"]}\nRed Alert: {db["RedAlert"]}\n')
      chatchannel = client.get_guild(130408666439352320).get_channel(935293610432290827)
      if db["GreenAlert"]:
        await chatchannel.send('<@&863661861114740788>')
        await chatchannel.send(f'DEU BOM TIME:\nTHC: ${db["THCDATA"]["price"]} \nTHG: ${db["THGDATA"]["price"]}')
        await updateCrypto.asyncio.sleep(36000)
      if db["RedAlert"]:
        await chatchannel.send('<@&863661861114740788>')
        await chatchannel.send(f'FUDEU GALERA:\nTHC: ${db["THCDATA"]["price"]}\nTHG: ${db["THGDATA"]["price"]}')
        await updateCrypto.asyncio.sleep(36000)
    except Exception as e:
      print(e)
    await updateCrypto.asyncio.sleep(200)
  

client.loop.create_task(updateCrypto.looping())
client.loop.create_task(fireAlarm())

keep_alive()
client.run(os.environ['TOKEN'])