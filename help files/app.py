from typing import Union

from base import Arena
from instrument import Instrument
from flask import Flask, render_template, request, redirect, Response

app = Flask(__name__)

heroes = {}

arena = Arena()


@app.route("/")
def menu_page() -> str:
    return render_template('index.html')


@app.route("/fight/")
def start_fight() -> str:
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template('fight.html', heroes=heroes,
                           result=arena.result, battle_result=arena.battle_result)


@app.route("/fight/hit")
def hit() -> str:
    if not arena.game_is_running:
        return redirect('/fight/end-fight')
    arena.player_hit()
    return render_template('fight.html', heroes=heroes,
                           result=arena.result, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill() -> str:
    if not arena.game_is_running:
        return redirect('/fight/end-fight')
    arena.player_use_skill()
    return render_template('fight.html', heroes=heroes,
                           result=arena.result, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn() -> Union[str, Response]:
    if not arena.game_is_running:
        return redirect('/fight/end-fight')
    arena.next_turn()
    return render_template('fight.html', heroes=heroes,
                           result=arena.result, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight() -> Response:
    return redirect('/')


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero() -> Union[str, Response]:
    if request.method == 'POST':
        heroes['player'] = Instrument.request_info_player(request)
        return redirect('/choose-enemy/')
    if request.method == 'GET':
        return render_template('hero_choosing.html', result=Instrument.result_hero())


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy() -> Union[str, Response]:
    if request.method == 'POST':
        heroes['enemy'] = Instrument.request_info_enemy(request)
        return redirect('/fight/')
    if request.method == 'GET':
        return render_template('hero_choosing.html', result=Instrument.result_enemy())


if __name__ == "__main__":
    app.run()
