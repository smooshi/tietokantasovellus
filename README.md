# Tietokantasovellus Kesä 2017
Motivational To Do thing database

Ideana on tehdä pieni tietokantaprojekti sellaisesta "motivationaalisesta" To Do-listasta nettiin. Työ tehdään Pythonilla ja käytetään Flaskia.

Dokumentaatio: https://github.com/smooshi/tietokantasovellus/blob/master/doc/TodoAppi.pdf

Host: https://todoappi.herokuapp.com

Käyttäjätunnukset ohjaajalle: username: tsoha , password: testi
Käyttäjän luominen toimii myös.

Toteutettu:
  - Sovelluksen pohja (18.5)
  - Login (19.5)
  - Notes, Todos, Focus, Goals ( 20.5 - 24.5.) kaikkia voi muokata/tuhota
  - Viikko2 huom: tietokantataulut pystytetään/dropataan samassa tiedostossa = schema.sql

Tehdyt sivut:

Ei vaadi kirjautumista:
  - index.html (Ennenkun login) -> https://todoappi.herokuapp.com/
  - login.html -> https://todoappi.herokuapp.com/login
  - create.html (Login, create user) -> https://todoappi.herokuapp.com/create
  
Vaatii kirjautumisen:
  - main.html (Kun logattu, pääsivu jolla suurin osa toiminnoista) -> https://todoappi.herokuapp.com/
  - profile.html (Käyttäjän profiili) + edit.html (käyttäjän editointi) -> Valikko (käyttäjänimi): Profile
  - Notes, Todos, Focus, Goals kaikilla on edit.html ja add.html -> Edit Mouseover hover ja Add titlen vierestä (+) 


![alt text](https://img.devrant.io/devrant/rant/r_587474_71JRh.jpg)
