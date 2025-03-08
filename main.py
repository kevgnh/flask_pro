from flask import Flask, request,session,redirect,render_template,url_for
import hashlib
import sympy as sp
from sympy import limit,oo,sqrt
import sqlite3
from datetime import timedelta
import secrets  
import dotenv
from dotenv import load_dotenv
import re
import html
import os

pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
patter1=r'^[a-zA-Z]+[0-9]*{8,}$'

app=Flask(__name__)
app.config["SESSION_SECURE"]=True
app.config["SESSION_HTTPONLY"]=True
app.config["PERMANET_SESSION_LIFETIME"]=timedelta(days=900000)
app.config["SECRET_KEY"]=os.getenv("key")

def seldefine():
    op=secrets.token_hex()
    return op
    

def has(chaine):
    session.permanent=True
    hashobj=hashlib.sha256(chaine.encode())
    chainehash=hashobj.hexdigest()
    return str(chainehash)



@app.route("/sign-up")
def sin():
     if "idname" and "idpassword" in session:
        return redirect(url_for("main"))
     else:
         return render_template("signup.html")

@app.route("/trsign-up",methods=["post"])
def tr():
    
    conn=sqlite3.connect("data.db")
    curseur=conn.cursor()
    req="insert into users(name,Email,password,sel) values(?,?,?,?)"
    name=request.form.get("username")
    Email=request.form.get("Email")
    mdp=request.form.get('password')

    if re.match(pattern,Email):
        sel=seldefine()
        Mdp=mdp+sel 
        mdpsecure=has(Mdp)
        curseur.execute(req,(name,Email,mdpsecure,sel))
        conn.commit()
        conn.close() 
        Name=has(name)
        session["idname"]=Name
        session["idpassword"]=mdpsecure
        return render_template("main.html")
    else:
        return redirect(url_for('sin'))
    
    
    

    

@app.route("/")
def login():
    if 'idusername' and 'idpassword' in session:
        return redirect(url_for('main'))
    else:
        return render_template("login.html")
    
@app.route("/trlogin",methods=["post"])
def trlogin():
    Id=request.form.get('ID')
    mdp=request.form.get('password')
    conn=sqlite3.connect('data.db')
    curseur=conn.cursor()
    if re.match(pattern,Id):   
        req="select password,sel from users where Email=?"
        curseur.execute(req,(Id,))
        expr_final=curseur.fetchall()
        Answer=expr_final[0]
        m_dp=Answer[0]
        sel=Answer[1]
        Mdp=mdp+sel
        Mpd=has(Mdp)
        if Mpd==m_dp:
            return render_template("main.html")
        else: 
            return render_template("login.html")
    else:
        req="select password,sel from users where name=?"
        curseur.execute(req,(Id,))
        expr_final=curseur.fetchall()
        Answer=expr_final[0]
        m_dp=Answer[0]
        sel=Answer[1]
        Mdp=mdp+sel
        Mpd=has(Mdp)
        if Mpd==m_dp:
            return render_template("main.html")
        else: 
            return render_template("login.html")
    
@app.route("/main")
def main():
    return render_template("main.html") 

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/mainlim')
def mainlim():
    return render_template('mainlim.html')
@app.route('/trmainlim',methods=["post"])
def trmainlim():
    if request.form.get("action")=='racine_limite':
        expr=request.form.get('expressionlim')
        rcarré="\u221A()"
        Expre=expr+rcarré
        return render_template("mainlim.html",a=Expre)
    x,y=sp.symbols("x,y")
    
    expr=request.form.get("expressionlim")
    if "\u221A" in expr:
        expr_final=expr.replace("\u221A","sqrt")
        expr_final=sp.sympify(expr_final)
        variable=request.form.get("variable")
        valeur=request.form.get("valeur")
        Sens=request.form.get('sens')
        if Sens =='':
            limite=limit(expr_final,variable,valeur)
            Limite=str(limite)
            if "sqrt" in Limite:
                Limite=Limite.replace("sqrt","\u221A")
            return render_template('answers.html',an=Limite)
        else:
            limite=limit(expr_final,variable,valeur,Sens)
            return render_template("answers.html",an=limite)
    else:
        expr_not_racine=request.form.get("expressionlim")
        Expr_not_racine=sp.sympify(expr_not_racine)
        valeur_not_racine=request.form.get('valeur')
        sens_not_racine=request.form.get('sens')
        variable_not_racine=request.form.get("variable")
        if sens_not_racine=='':
            limite_not_racine=limit(Expr_not_racine,variable_not_racine,valeur_not_racine)
            limite_not_racine=str(limite_not_racine)
            if "sqrt" in limite_not_racine:
                Limite_not_racine=limite_not_racine.replace("sqrt","\u221A")
                return render_template("answers.html",a=Expr_not_racine,an=Limite_not_racine)

        else:
            if "sqrt" in limite_not_racine:
                Limite_not_racine=limite_not_racine.replace("sqrt","\u221A")
                return render_template("answers.html",a=Expr_not_racine,an=Limite_not_racine)
            limite_not_racine=limit(Expr_not_racine,variable_not_racine,valeur_not_racine,sens_not_racine)
            return render_template("answers.html",a=Expr_not_racine,an=Limite_not_racine)

@app.route("/main_derivation")
def derivation():
    return render_template("derivation.html")

@app.route("/trmain_derivation",methods=["post"])
def trmain_derivation():
    if request.form.get("action")=="racine_der":
        expr=request.form.get('der')
        rcarré="\u221A()"
        Expre=expr+rcarré
        return render_template("derivation.html",a=Expre)
    else:
        x,y=sp.symbols("x,y")
        expr=request.form.get("der")
        variable=request.form.get("variable")
        dr=sp.diff(expr,variable)
        return render_template("answers.html",an=dr)
app.run(debug=True)
    