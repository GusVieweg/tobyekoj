# Work with Python 3.6
import discord
import operator
import requests

TOKEN = 'NDgwMDg5MTE0MzgxNjQ3OTEy.Dl5aeA.5LGEgNJyc36GX5692Rgg2REI6-U'

client = discord.Client()
debug = False

def get_emoji_data():
    emojiURL = "https://api.myjson.com/bins/ot0bs"
    if(debug):
        emojiURL = 'https://api.myjson.com/bins/1500r4'
    return requests.get(emojiURL).json()

def sum_up_emoji_totals(data, individual):
    emojiTotals = {}
    for emoji in data:
        emojiTotals[emoji] = 0
        if(individual == "all"):
            for person in data[emoji]:
                try:
                    emojiTotals[emoji] += data[emoji][person]
                except:
                    print("Skipping " + str(emoji))
        else:
            try:
                emojiTotals[emoji] += data[emoji][individual]
            except:
                print("Skipping " + str(emoji))
    emojiTotals_s = sorted(emojiTotals.items(), key=operator.itemgetter(1), reverse=True)
    return emojiTotals_s

@client.event
async def on_message(message):
    people = ['gus', 'walker', 'carter', 'patrick', 'alex', 'stefan', 'chris']

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!test') and message.channel.name=='bot-test':
        msg = 'Hello {0.author.mention}, you have summoned a test.'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!customemoji'):
        emojiData = get_emoji_data()
        if len(message.content.split(' ')) == 1:
            sorted_sum_data = sum_up_emoji_totals(emojiData, 'all')
            top3 = 'TOP 3 CUSTOM EMOJIS\n'
            for datum in range(0, 3):
                top3 += str(sorted_sum_data[datum][0]) + ": " + str(sorted_sum_data[datum][1]) + "\n"
            await client.send_message(message.channel, top3)

        elif message.content.split(' ')[1] in people:
            person = message.content.split(' ')[1]
            sorted_person_data = sum_up_emoji_totals(emojiData, person)
            top3 = 'TOP 3 CUSTOM EMOJIS FOR ' + person.upper() + "\n"
            for datum in range(0, 3):
                top3 += str(sorted_person_data[datum][0]) + ": " + str(sorted_person_data[datum][1]) + "\n"
            await client.send_message(message.channel, top3)

    if message.content == '!help':
        helpmsg = "Hello! It seems you have requested help for the !customemoji event.\n\nCurrent functionality supports:\n!customemoji will display the top three custom emojis for the server since August 24, 2018.\n!customemoji [name] will show the top 3 custom emojis for the named individual since August 24, 2018.\n\nCurrent names to reference are: gus, walker, alex, carter, patrick, chris, stefan.\n\nJokeyBotv1.0.0."
        await client.send_message(message.channel, helpmsg)

def get_emoji_name(emoji):
    try:
        emojiString = str(emoji)
        print(emojiString)
        firstColonIndex = emojiString.index(":")
        emojiString = emojiString[firstColonIndex+1:]
        secondColonIndex = emojiString.index(":")
        return emojiString[0:secondColonIndex]
    except ValueError:
        return "NotCustom"

def myjsonPutRequest(endpoint, data):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
    requests.put(endpoint, json=data, headers=headers)

def save_emoji_data(emoji, user, server):
    emojiURL = "https://api.myjson.com/bins/ot0bs"
    if(debug):
        emojiURL = 'https://api.myjson.com/bins/1500r4'
    people_ids = {
        '93444464122527744':'stefan',
        '452220283881914382':'gus',
        '387138104932171776':'carter',
        '130926733124829185':'walker',
        '393578567826407424':'chris',
        '424366594345402370':'patrick',
        '453425660816523274':'alex'
    }
    person = people_ids[user.id]

    data = requests.get(emojiURL).json()
    try:
        data[emoji][person]+=1
    except:
        data[emoji] = {'stefan':0,'gus':0,'carter':0,'walker':0,'chris':0,'patty':0,'alex':0}
        data[emoji][person]+=1

    myjsonPutRequest(emojiURL, data)

@client.event
async def on_reaction_add(reaction, user):
    emojiUsed = get_emoji_name(reaction.emoji)
    if(emojiUsed == "NotCustom"):
        return
    server = list(client.servers)[0]
    if(reaction.message.channel.name!='bot-test' and (debug == False)):
        save_emoji_data(emojiUsed, user, server)
    if(reaction.message.channel.name=='bot-test' and debug):
        save_emoji_data(emojiUsed, user, server)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)