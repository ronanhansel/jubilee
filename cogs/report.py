from discord.ext import commands
import os
from datetime import datetime, timedelta
import requests
import time
import json
from types import SimpleNamespace


class Report(commands.Cog):
    "Facebook page report"

    def __init__(self, client):
        self.client = client

    @commands.command(help="Report a field")
    async def report(self,
                     ctx,
                     field,
                     _type='line',
                     _bgcolour='white'):
        await ctx.send("'Aight gimme a sec...")
        try:
            week_delta = 691200
            today = int(time.time())
            params = {
                'access_token': os.getenv('fb_token'),
                'metric': field,
                'since': today - week_delta,
                'until': today
            }

            url = 'https://graph.facebook.com/v11.0/107368598286513/insights'

            r = requests.get(url=url, params=params).json()
            data = SimpleNamespace(**r)
            for i in data.data:
                data.data.pop()
                data.data.pop()
                dayval = SimpleNamespace(**i)
                values = []
                days = []
                d = 1

                for i in dayval.values:
                    values.append(i['value'])
                    days.append((datetime.today() - timedelta(days=d)).day)
                    d += 1
            days.reverse()
            values.reverse()
            # plotting the points
            quickchart_url = 'https://quickchart.io/chart/create'
            post_data = {
                "backgroundColor": _bgcolour,
                'chart': {
                    'type': _type,
                    'data': {
                        'labels': days,
                        'datasets': [{
                            'label': dayval.title,
                            'data': values
                        }]
                    }
                }
            }

            response = requests.post(
                quickchart_url,
                json=post_data,
            )

            if (response.status_code != 200):
                ctx.send('Error: ', response.text)
            else:
                chart_response = json.loads(response.text)
                await ctx.send(chart_response['url'])
                await ctx.send('Here you go!')
        except IndexError:
            today = int(time.time())
            params = {
                'access_token': os.getenv('fb_token'),
                'metric': field,
                'since': today - 86400 * 3,
                'until': today
            }
            url = 'https://graph.facebook.com/v11.0/107368598286513/insights'
            r = requests.get(url=url, params=params).json()
            data = SimpleNamespace(**r)
            dayval = SimpleNamespace(**data.data[-1])
            result = dayval.values[-1]
            value = result['value']
            _time = result['end_time']
            try:
                formatted = "\n".join(
                    [f'{key} \t  \t {value}' for key, value in sorted(value.items())])
                formatted += "\n Updated: " + f"{_time[:-14]}"
                await ctx.send("```" + formatted + "```")
            except Exception:
                await ctx.send(f"{value} \t Updated: " + f"{_time[:-14]}")


def setup(client):
    client.add_cog(Report(client))
