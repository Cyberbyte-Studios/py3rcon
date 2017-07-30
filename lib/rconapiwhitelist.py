import logging

import requests


class RconApiWhitelist(object):
    def __init__(self, rcon, config):
        self.config = config
        self.rcon = rcon
        self.whitelist = []

    def fetchPlayers(self):
        self.rcon.sendCommand('players')

    def check_player(self, player):
        try:
            if self.api_check(player):
                logging.debug('Player {name}({guid}) is whitelisted'
                              .format(name=player.name, guid=player.guid))
                return
        except Exception:
            logging.exception('Failed to check whitelist api')

        logging.info('Player {name}({guid}) not whitelisted - Sent kick command'
                     .format(name=player.name, guid=player.guid))
        self.rcon.sendCommand('kick {player} "{message}"'
                              .format(player=player.number,
                                      message=self.config['kick_message']))

    def api_check(self, player):
        response = requests.get(
            self.config['url'].format(guid=player.guid)).json()
        if response['result'] != True:
            return False
        # if len(self.fetchPlayers() > 95)
        return True

    # def OnPlayers(self, playerList):
    #     for x in playerList:
    #         self.check_player(x)

    def OnPlayerConnect(self, player):
        self.check_player(player)
