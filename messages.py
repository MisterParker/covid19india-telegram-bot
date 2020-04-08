import json
import datetime

def get_data():
    with open('data.json') as f:
        data = json.load(f)
        return data
    return False


msg_start = """<b>Welcome to The India Covid-19 Tracker Bot! 🦠</b>
(<i>a crowdsouced initiative</i>)

The first telegram bot to help track the spread of COVID-19 (coronavirus disease 2019) based on a crowdsourced dataset for India.

<b><u>Commands:</u></b>

/count
Total cases identified COVID-19 cases in India.

/today
Cases identified as of today.

/statewise
List of statewise cases in India.

/about
Info about the bot and the source.


<i>Note:</i> Open source community generated bot for the people to stay informed. No legal obligation. Community generated data from covid19india.org

Government Updates on: @MyGovCoronaNewsdesk

Built by akigugale.me

Stay Home, Stay Safe! 🏡

"""



msg_about = """<b>This is the India Covid-19 Tracker Bot! 🦠 🇮🇳</b>
(<i>a crowdsouced initiative</i>)

The first telegram bot to help track the spread of COVID-19 (coronavirus disease 2019) based on a crowdsourced dataset for India.

Built by - <a href="https://twitter.com/akigugale">@akigugale</a>

Data from - https://covid19india.org

Official Indian Govt. Telegram Channel: @MyGovCoronaNewsdesk

Contribute at - https://github.com/akigugale/covid19india-telegram-bot

-----------------
<i>Made for public information, no legal obligation.</i>

Stay Home, Stay Safe! 🏡
"""

def pretty_date_time(date_time):
    date_time_obj = datetime.datetime.strptime(date_time, "%d/%m/%Y %H:%M:%S")
    formatted_date_time = date_time_obj.strftime("%d %b, %H:%M IST")
    return formatted_date_time


def get_lastupdated_msg():
    data = get_data()
    last_updated_time = data['statewise'][0]['lastupdatedtime']
    msg_lastupdated = """Last Updated on <b>{0}</b>""".format(pretty_date_time(last_updated_time))
    return msg_lastupdated


def get_footer(data):
    last_updated = pretty_date_time(data['statewise'][0]['lastupdatedtime'])
    footer = """\n Updated on {updated_on} \n Data from covid19india.org \n by akigugale.me""".format(updated_on = last_updated)
    return footer


def get_count_msg():
    data = get_data()
    total = data['statewise'][0]
    msg = """<b>Number of Covid-19 cases in India:</b>

😷 Confirmed: <b>{confirmed}</b>  [+{deltaconfirmed}]
🔴 Active: <b>{active}</b>
💚 Recovered: <b>{recovered}</b>  [+{deltarecovered}]
💀 Deceased: <b>{deaths}</b>  [+{deltadeaths}]

Updated on {updated_on}
    """.format(confirmed=total["confirmed"], deltaconfirmed=total["deltaconfirmed"], active=total['active'], recovered=total['recovered'], deltarecovered=total['deltarecovered'], deaths=total['deaths'], deltadeaths=total['deltadeaths'], updated_on=pretty_date_time(total['lastupdatedtime']))
    return msg


def get_today_msg():
    data = get_data()
    total = data['statewise'][0]
    updated_on=pretty_date_time(total['lastupdatedtime'])
    msg = """<b>New Covid-19 cases in India on {date} till {time}:</b>

😷 Confirmed: +{deltaconfirmed}
💚 Recovered: +{deltarecovered}
💀 Deceased:  +{deltadeaths}
    """.format(deltaconfirmed=total["deltaconfirmed"], deltarecovered=total['deltarecovered'], deltadeaths=total['deltadeaths'],updated_on=updated_on , date=updated_on[0:6], time=updated_on[-9:])
    msg += get_footer(data)
    return msg


def get_statewise_msg():
    data = get_data()
    statewise_data = data['statewise']
    statewise_msg = """<b>Statewise data for COVID-19.</b>

    😷 - Confirmed cases
    💚 - Recovered
    💀 - Deaths
    <code>"""
    for state in statewise_data[1:]:
        formatted_state_data = "\n {state_name}: 😷 {confirmed}   💚 {recovered}   💀 {deaths}".format(state_name=state['statecode'], confirmed=state['confirmed'], recovered=state['recovered'], deaths=state['deaths'])
        statewise_msg += formatted_state_data
    # TODO: add last updated for each state and delta values?

    statewise_msg += """\n------------------------ \n <b>{state_name}: 😷{confirmed}  💚{recovered}  💀{deaths}</b> </code>\n\n""".format(state_name=statewise_data[0]['state'], confirmed=statewise_data[0]['confirmed'], recovered=statewise_data[0]['recovered'], deaths=statewise_data[0]['deaths'])
    statewise_msg += get_footer(data)

    return statewise_msg