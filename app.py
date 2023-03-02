import datetime
import json
import secrets
import smtplib
import time
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_extendable_graph as deg
import dash_extensions as de
import mysql.connector
import paho.mqtt.client as mqtt
import pytz
from dash import Input, Output, State, callback, dash_table, dcc, html
from flask import Flask
from flask_login import (LoginManager, UserMixin, current_user, login_user,
                         logout_user)
from pandas import *

# IoT Protocol with cloud broker, port no like TCP/IP or Websocket, connecting time in ms
mqttc = mqtt.Client()
mqttc.connect("broker.emqx.io", 1883, 18060)
# CSV Read
global Flt_No
data = read_csv('assets/data/Fault_12.csv')
Flt_No = data['Fault_Name'].tolist()


# A particular Topic, from where we can access our cloud data
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttc.subscribe("Sim/Dyna")


Prv_Sts = int
Pre_Sts1 = int
x = int
t=0


# Reading data based on name from Cloud
def on_message(client, userdata, msg):
    global IP_Speed, IP_Torque, IP_Power, LH_Speed, LH_Torque, LH_Power, RH_Speed, RH_Torque, RH_Power, Gear_Ratio, Running_Gear_Id, Target_Gear_Id, Status_CMD, Fault_No, Flt_No, F
    global Running_Step, Present_Step, Sequence_On, Trial_No, Bench_Status, Mode_Of_Bench, Oil_Temperature, Serial_No, iptrq, lhtrq, rhtrq, lhspd, rhspd, grr, A, Prv_Sts, Pre_Sts1, t, res, x, Prc
    global S_IP_Spd, S_IP_Trq, S_LH_Spd, S_LH_Trq, S_RH_Spd, S_RH_Trq, Fault_d, ip_spd, oil_temp,ip_pwr, lh_pwr, rh_pwr, s_spd, s_trq, s_l_spd, s_l_trq, s_r_spd, s_r_trq
    mydb = mysql.connector.connect(
        host="rgdyna-ci-mysql-test.mysql.database.azure.com",
        user="Dyna_Software",
        password="DiS3#4344",
        database="test"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT mailid FROM emailid")

    myresult = mycursor.fetchall()
    global res
    res = [x for xs in myresult for x in xs]
    # print(res)
    mydb.commit()

    mycursor1 = mydb.cursor()

    mycursor1.execute("SELECT mailid FROM selectedemailid")

    myresult1 = mycursor1.fetchall()
    global res1
    res1 = [x for xs in myresult1 for x in xs]
    res2=','.join(map(str, res1))
    res3 = res2.split(',')
    #res3 = list(''.join, res2)
    #print(res3)
    mydb.commit()

    value = str(msg.payload.decode())
    my_dict = json.loads(value)

    IP_Speed = my_dict['IP_Speed']
    ip_spd = ('%i' % IP_Speed)

    iptrq = my_dict['IP_Torque']
    IP_Torque = ('%i' % iptrq)

    IP_Power = my_dict['IP_Power']
    ip_pwr = ('%.1f' % IP_Power)

    lhspd = my_dict['LH_Speed']
    LH_Speed = ('%i' % lhspd)

    lhtrq = my_dict['LH_Torque']
    LH_Torque = ("%i" % lhtrq)

    LH_Power = my_dict['LH_Power']
    lh_pwr = ('%.1f' % LH_Power)

    rhspd = my_dict['RH_Speed']
    RH_Speed = ('%i' % rhspd)

    rhtrq = my_dict['RH_Torque']
    RH_Torque = ('%i' % rhtrq)

    RH_Power = my_dict['RH_Power']
    rh_pwr = ('%.1f' % RH_Power)

    grr = my_dict['Gear_Ratio']
    Gear_Ratio = ('%.2f' % grr)

    Running_Gear_Id = my_dict['Running_Gear_Id']
    Target_Gear_Id = my_dict['Target_Gear_Id']
    if Running_Gear_Id == 6:
        Target_Gear_Id = 0
    else:
        Target_Gear_Id += 1

    Running_Step = my_dict['Running_Step']

    Present_Step = my_dict['Present_Step']

    Sequence_On = my_dict['Sequence_On']

    Trial_No = my_dict['Trial_No']

    Bench_Status = my_dict['Bench_Status']

    Mode_Of_Bench = my_dict['Mode_Of_Bench']

    Oil_Temperature = my_dict['Oil_Temperature']
    oil_temp = ('%.1f' % Oil_Temperature)
    Status_CMD = my_dict['Status_cmd']
    A = my_dict['Serial_No']
    Serial_No = ('%i' % A)
    F = my_dict['Fault_No']
    Fault_No = int(F)
    S_IP_Spd = my_dict['S_ip_Spd']
    s_spd = ('%i' % S_IP_Spd)
    S_IP_Trq = my_dict['S_ip_Trq']
    s_trq = ('%i' % S_IP_Trq)
    S_LH_Spd = my_dict['S_lh_Spd']
    s_l_spd = ('%i' % S_LH_Spd)
    S_LH_Trq = my_dict['S_lh_Trq']
    s_l_trq = ('%i' % S_LH_Trq)
    S_RH_Spd = my_dict['S_rh_Spd']
    s_r_spd= ('%i' % S_RH_Spd)
    S_RH_Trq = my_dict['S_rh_Trq']
    s_r_trq = ('%i' % S_RH_Trq)



    if Bench_Status == 0 and Bench_Status != Prv_Sts:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("iiot4.0robot@gmail.com", "pzvlmittbpgcagwb")
        recepients = res3
        SUBJECT = "Avtech Sim-machine Status"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, "Running...!")
        # s.sendmail("iiot4.0robot@gmail.com", recepients, message)
        Prv_Sts = Bench_Status
        Pre_Sts1 = int
        t = 0


    if Bench_Status == 1 and Bench_Status != Prv_Sts:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("iiot4.0robot@gmail.com", "pzvlmittbpgcagwb")
        recepients = res3
        SUBJECT = "Avtech Sim-machine Status"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, "Idle....!")
       # s.sendmail("iiot4.0robot@gmail.com", recepients, message)
        Prv_Sts = Bench_Status
        Pre_Sts1 = int
        t = 0


    if Bench_Status == 2 and Bench_Status != Pre_Sts1:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("iiot4.0robot@gmail.com", "pzvlmittbpgcagwb")
        recepients = res3
        SUBJECT = "Avtech Sim-machine Status"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, Flt_No[Fault_No])
        # s.sendmail("iiot4.0robot@gmail.com", recepients, message)
        Prv_Sts = int
        Pre_Sts1 = Bench_Status


    if Pre_Sts1 == Bench_Status:
        t = t + 1
        #print(t)
        if t == 3600:
            Pre_Sts1 = int
            t = 0


mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_start()

# Exposing the Flask Server to enable configuring it for logging in
server1 = Flask(__name__)
dash_app = dash.Dash(__name__, server=server1,
                     title='Dynaspede 4.0',
                     update_title='Loading...',
                     suppress_callback_exceptions=True)
app = dash_app.server
# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
server1.config.update(SECRET_KEY=secrets.token_hex(16))

# Login manager object will be used to log in / logout users
login_manager = LoginManager()
login_manager.init_app(server1)


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """ This function loads the user by user id. Typically, this looks up the user from a user database.
        We won't be registering or looking up users in this example, since we'll just log in using LDAP server.
        So we'll simply return a User object with the passed in username.
    """
    return User(username)


# User status management views
# Main Layout
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    dcc.Store(id='login-status', storage_type='session'),
    html.Div(id='user-status-div'),
    html.Div(id='page-content'),
])

options = dict(loop=True, autoplay=True)
# Login screen
login = html.Div([dcc.Location(id='url_login', refresh=True),
                  html.H1("Dynaspede 4.0 Test Station",
                          style={'position': 'absolute', 'top': '0px', 'left': '610px', 'font-size': '40px',
                                 'font-weight': 'bold'}),

                  dcc.Input(placeholder='Enter your username',
                            type='text', id='uname-box',
                            style={'position': 'absolute', 'top': '360px', 'left': '650px', 'width': '300px',
                                   'height': '30px',
                                   'padding': '10px', 'font-size': '16px',
                                   'border-width': '3px', 'border-color': '#a0a3a2',
                                   'text-align': 'center'}),
                  dcc.Input(placeholder='Enter your password',
                            type='password', id='pwd-box',
                            style={'position': 'absolute', 'top': '440px', 'left': '650px', 'width': '300px',
                                   'height': '30px', 'padding': '10px',
                                   'font-size': '16px',
                                   'border-width': '3px', 'border-color': '#a0a3a2',
                                   'text-align': 'center'}),
                  html.Button(children='Login', n_clicks=0,
                              type='submit', id='login-button',
                              style={'position': 'absolute', 'top': '530px', 'left': '750px',
                                     'background-color': 'greenyellow', 'width': '120px',
                                     'height': '40px', 'font-size': '20px', 'font-weight': 'bold'}),
                  html.Div(children='', id='output-state',
                           style={'padding-left': '710px', 'padding-top': '650px', 'font-size': '16px'}),
                  html.Br(),
                  html.Div([de.Lottie(options=options,
                                      url="https://assets2.lottiefiles.com/packages/lf20_ggwq3ysg.json")],
                           style={'height': '500px', 'width': '600px', 'position': 'absolute',
                                  'top': '150px', 'left': '0px'}),

                  html.Div([de.Lottie(options=options,
                                      url="https://assets2.lottiefiles.com/packages/lf20_uui8d4hv.json")],
                           style={'height': '200px', 'width': '200px', 'position': 'absolute', 'top': '100px',
                                  'left': '710px'})
                  ], style={'background-image': 'url(/assets/7.jpg)', 'width': '1920px', 'height': '936px',
                            'background-repeat': 'no-repeat',
                            'background-size': 'cover'})

# Successful login
select = html.Div([html.Div([html.H1("Dynaspede 4.0 Test Station",
                                     style={'position': 'absolute', 'top': '0px', 'left': '720px', 'font-size': '40px',
                                            'font-weight': 'bold', 'color': 'white'}),
                             html.H2('Login successful.',
                                     style={'position': 'absolute', 'top': '100px', 'left': '868px',
                                            'color': 'white', 'font-family': 'serif', 'font-weight': 'bold',
                                            "text-decoration": "none", 'font-size': '25px', 'height': '30px',
                                            'width': '200px', 'text-align': 'center'}),
                             html.Br(),
                             dcc.Link('Dashboard', href='/dashboard',
                                      style={'background-color': '#119dff', 'position': 'absolute', 'top': '310px',
                                             'left': '868px',
                                             'color': 'white', 'font-family': 'serif', 'font-weight': 'bold',
                                             "text-decoration": "none",
                                             'font-size': '25px', 'height': '30px', 'width': '200px',
                                             'text-align': 'center'}),

                             dcc.Link('Mimic', href='/mimic',
                                      style={'position': 'absolute', 'top': '420px', 'left': '868px', 'color': 'white',
                                             'font-family': 'serif',
                                             'font-weight': 'bold', "text-decoration": "none", 'font-size': '25px',
                                             'background-color': '#119dff',
                                             'width': '200px', 'text-align': 'center', 'height': '30px'}),

                             dcc.Link('Datalog', href='/datalog',
                                      style={'position': 'absolute', 'top': '530px', 'left': '868px',
                                             'background-color': '#119dff',
                                             'color': 'white', 'font-family': 'serif', 'font-weight': 'bold',
                                             "text-decoration": "none",
                                             'font-size': '25px', 'height': '30px', 'width': '200px',
                                             'text-align': 'center'}),

                             dcc.Link('Graph', href='/graph',
                                      style={'position': 'absolute', 'top': '640px', 'left': '868px', 'color': 'white',
                                             'font-family': 'serif',
                                             'font-weight': 'bold', "text-decoration": "none", 'font-size': '25px',
                                             'background-color': '#119dff',
                                             'width': '200px', 'text-align': 'center', 'height': '30px'}, ),

                             html.Div([de.Lottie(options=options,
                                                 url="https://assets7.lottiefiles.com/packages/lf20_a9xyhp9v.json")],
                                      style={'height': '100px', 'width': '200px', 'position': 'absolute', 'top': '70px',
                                             'left': '1030px'}),
                             html.Div([de.Lottie(options=options,
                                                 url="https://assets3.lottiefiles.com/packages/lf20_04usqfm9.json")],
                                      style={'height': '400px', 'width': '400px', 'position': 'absolute',
                                             'top': '300px', 'left': '1350px'}),
                             html.Div([de.Lottie(options=options,
                                                 url="https://assets3.lottiefiles.com/packages/lf20_04usqfm9.json")],
                                      style={'height': '400px', 'width': '400px', 'position': 'absolute',
                                             'top': '300px', 'left': '185px', 'transform': 'scaleX(-1)'}),

                             ])  # end div
                   ], style={'background-image': 'url(/assets/18.jpg)', 'width': '1920px', 'height': '936px',
                             'background-repeat': 'no-repeat',
                             'background-size': 'cover'})  # end div

# Dashboard Screen
dashboard = html.Div([

    html.Div(
        [
            html.Div([dcc.Dropdown(
                [

                    {
                        "label": html.Div(
                            [
                                dcc.Link('Mimic', href='/mimic')
                            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                        ),
                        "value": "R",
                    },
                    {
                        "label": html.Div(
                            [
                                dcc.Link('Datalog', href='/datalog')
                            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                        ),
                        "value": "python",
                    },
                    {
                        "label": html.Div(
                            [
                                dcc.Link('Graph', href='/graph')
                            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                        ),
                        "value": "python",
                    },
                    {
                        "label": html.Div(
                            [
                                dcc.Link('Logout', href='/logout')

                            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                        ),
                        "value": "Python",
                    },
                ], style={'backgroundColor': 'green', 'textAlign': 'center', 'color': 'white'}, placeholder="Dashboard"
            )], style={'position': 'absolute', 'top': '50px', 'left': '1715px', 'height': '40px', 'width': '150px'}),

            html.Button("Mail configuration", id="open",
                        style={'position': 'absolute', 'top': '90px', 'left': '1715px', 'height': '40px',
                               'width': '150px','font-size': '13px', 'font-weight': 'bold'
                               }),
            dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Mail configuration"), style={'font-size': '30px', 'color': 'white', 'text-align': 'center', 'font-weight': 'bold'}),
                            dbc.ModalBody(
                                [
                                   # html.Plaintext("Mail configuration", style={'position': 'absolute', 'top': '0px', 'left': '450px', 'font-size': '25px', 'color': 'white'}),
                                    dcc.Input(id='mail',placeholder="Enter new mailid", style={'height': '35px', 'width': '300px', 'position': 'absolute', 'top': '53px', 'left': '10px', 'font-size': '16px'}),
                                    html.Button('Add', id='button', style={'width': '100px', 'height': '40px', 'position': 'absolute', 'top': '53px', 'left': '318px', 'font-weight': 'bold'}),
                                    html.Plaintext(id='id[0]'),
                                    dcc.Dropdown(id='dropdown',placeholder="Select mail id", style={'width': '300px', 'height': '40px', 'position': 'absolute', 'top': '27px', 'margin-left': '223px', 'verticalAlign': "middle"}),
                                    html.Button('Delete', id='del', style={'width': '100px', 'height': '40px', 'position': 'absolute', 'top': '53px', 'left': '746px',  'font-weight': 'bold'}),

                                    dbc.Container(
                                        children=[
                                            html.Details([
                                                html.Summary('Select mailid',style={'font-size': '16px'} ),
                                                dbc.Col([
                                                    dcc.Checklist(id='checkbox-group',
                                                                  labelStyle={'display': 'block', 'color': 'black',
                                                                              'backgroundColor': 'white', 'height': '50px',
                                                                              'width': '300px'},
                                                                  persistence=True,
                                                                  persistence_type='session'

                                                                  )
                                                ], style={"overflow-y": "scroll", "overflow-x": 'hidden', "height": '400px'}),
                                                html.Button("Update", id="save", style={ 'height': '40px', 'width': '100px', 'background-color': 'lightgreen','position': 'absolute', 'left': '95px'}),
                                            ], id = 'detail')
                                        ], style={'position': 'absolute', 'top': '53px', 'left': '870px', 'height': '40px',
                                                  'width': '300px', 'backgroundColor': 'white'}),
                                         html.Button("Close", id="close", style={'position': 'absolute', 'top': '590px', 'left': '10px', 'height': '40px', 'width': '100px', 'font-size': '16px', 'font-weight': 'bold'
                                      })

                                ]
                            ),

                        ],
                        id="modal",
                        backdrop="static",
                        #is_open=False,
                        style={'position': 'absolute', 'top': '150px', 'left': '350px','height': '650px', 'width': '1200px', 'background-image': 'url(/assets/mail.jpg)'}
                    ),
            dcc.ConfirmDialog(id='popup'),
            dcc.ConfirmDialog(id='update-popup'),
            dcc.ConfirmDialog(id='delete-popup'),

            dcc.Interval(id='interval-component', interval=500, n_intervals=0),
            html.Div(
                className="date", children=[html.Plaintext(id='date')]),
            dcc.Interval(id='update', interval=100),

            html.Div(
                className="text1", children=[html.Plaintext(id='id[0]')]),
            html.Div(
                className="text2", children=[html.Plaintext(id='id[1]')]),
            html.Div(
                className="text3", children=[html.Plaintext(id='id[2]')]),
            html.Div(
                className="text4", children=[html.Plaintext(id='id[3]')]),
            html.Div(
                className="text5", children=[html.Plaintext(id='id[4]')]),
            html.Div(
                className="text6", children=[html.Plaintext(id='id[5]')]),
            html.Div(
                className="text7", children=[html.Plaintext(id='id[6]')]),
            html.Div(
                className="text8", children=[html.Plaintext(id='id[7]')]),
            html.Div(
                className="text9", children=[html.Plaintext(id='id[8]')]),
            html.Div(
                className="text10", children=[html.Plaintext(id='id[9]')]),
            html.Div(
                className="text11", children=[html.Plaintext(id='id[10]')]),
            html.Div(
                className="text12", children=[html.Plaintext(id='id[11]')]),
            html.Div(
                className="text13", children=[html.Plaintext(id='id[12]')]),
            html.Div(
                className="text14", children=[html.Plaintext(id='id[13]')]),
            html.Div(
                className="text15", children=[html.Plaintext(id='id[14]')]),
            html.Div(
                className="text16", children=[html.Plaintext(id='id[15]')]),
            html.Div(
                className="text17", children=[html.Plaintext(id='id[16]')]),
            html.Div(
                className="text18", children=[html.Plaintext(id='id[17]')]),
            html.Div(
                className="text19", children=[html.Plaintext(id='id[18]')]),
            html.Div(
                className="text20", children=[html.Plaintext(id='id[19]')]),
            html.Div(
                className="fault_no", children=[html.Plaintext(id='id[20]')]),
            html.Div(
                className="text21", children=[html.Plaintext(id='id[21]')]),
            html.Div(
                className="text22", children=[html.Plaintext(id='id[22]')]),
            html.Div(
                className="text23", children=[html.Plaintext(id='id[23]')]),
            html.Div(
                className="text24", children=[html.Plaintext(id='id[24]')]),
            html.Div(
                className="text25", children=[html.Plaintext(id='id[25]')]),
            html.Div(
                className="text26", children=[html.Plaintext(id='id[26]')]),

            html.Div(
                className="Header", children=[html.H1("Endurance & Differential Test(Siemens Drive)")]),
            html.Div(
                className="Fault", children=[html.Marquee(id='fault_marq')], style={'text-align': 'center'}),

            html.Div(
                className="Marquee", children=[html.Marquee(
                    "Welcome To Dynaspede 4.0...!, Dynaspede Integrated Systems(P) Limited, Visit us at www.dynaspede.com, Contact No- 8667391167")]),


            daq.Indicator(id='Run', style=dict(display='none'), size=50, color="#28ff42", label="Run",
                          labelPosition="bottom"),

            daq.Indicator(id='Idle', style=dict(display='none'), size=50, color="yellow", label="Idle",
                          labelPosition="bottom"),

            daq.Indicator(id='Fault', style=dict(display='none'), size=50, color="red", label="Fault",
                          labelPosition="bottom"),

            dcc.Input(id='MAN_MODE', style=dict(display='none'), value="MANMODE"),
            dcc.Input(id='AUTO_MODE', style=dict(display='none'), value="AUTOMODE"),

            html.Div(
                className="Machine", children=[html.Plaintext("Machine")]),
            html.Div(
                className="Status", children=[html.Plaintext("Status")]),
            html.Div(
                className="ip_Speed", children=[html.Plaintext("IP Speed")]),
            html.Div(
                className="lh_Speed", children=[html.Plaintext("LH Speed")]),
            html.Div(
                className="rh_Speed", children=[html.Plaintext("RH Speed")]),
            html.Div(
                className="G_Ratio", children=[html.Plaintext("Gear ratio")]),
            html.Div(
                className="R_Step", children=[html.Plaintext("Running Step")]),
            html.Div(
                className="Trial_No", children=[html.Plaintext("Trial No")]),
            html.Div(
                className="Oil_Temp", children=[html.Plaintext("Oil Temp")]),
            html.Div(
                className="Ip_Trq", children=[html.Plaintext("IP Torque")]),
            html.Div(
                className="Lh_Trq", children=[html.Plaintext("LH Torque")]),
            html.Div(
                className="Rh_Trq", children=[html.Plaintext("RH Torque")]),
            html.Div(
                className="R_G_Id", children=[html.Plaintext("R Gear Id")]),
            html.Div(
                className="P_Stp", children=[html.Plaintext("P Step")]),
            html.Div(
                className="B_Status", children=[html.Plaintext("Bench Status")]),
            html.Div(
                className="Serial_No", children=[html.Plaintext("Serial No")]),
            html.Div(
                className="Ip_Pwr", children=[html.Plaintext("IP Power")]),
            html.Div(
                className="Lh_Pwr", children=[html.Plaintext("LH Power")]),
            html.Div(
                className="Rh_Pwr", children=[html.Plaintext("RH Power")]),
            html.Div(
                className="T_G_Id", children=[html.Plaintext("T Gear Id")]),
            html.Div(
                className="Seq_On", children=[html.Plaintext("Seq On")]),
            html.Div(
                className="M_Of_Bench", children=[html.Plaintext("Mode of Bench")]),
            html.Div(
                className="Fault_No", children=[html.Plaintext("Fault No")]),
            html.Div(
                className="S_I_spd", children=[html.Plaintext("S IP Speed")]),
            html.Div(
                className="S_I_trq", children=[html.Plaintext("S IP Torque")]),
            html.Div(
                className="S_L_spd", children=[html.Plaintext("S LH Speed")]),
            html.Div(
                className="S_L_trq", children=[html.Plaintext("S LH Torque")]),
            html.Div(
                className="S_R_spd", children=[html.Plaintext("S RH Speed")]),
            html.Div(
                className="S_R_trq", children=[html.Plaintext("S RH Torque")]),
            html.Div(
                className="I_rpm", children=[html.Plaintext("rpm")]),
            html.Div(
                className="L_rpm", children=[html.Plaintext("rpm")]),
            html.Div(
                className="R_rpm", children=[html.Plaintext("rpm")]),
            html.Div(
                className="I_nm", children=[html.Plaintext("Nm")]),
            html.Div(
                className="L_nm", children=[html.Plaintext("Nm")]),
            html.Div(
                className="R_nm", children=[html.Plaintext("Nm")]),
            html.Div(
                className="Centigrade", children=[html.Plaintext("°C")]),
            html.Div(
                className="I_kw", children=[html.Plaintext("KW")]),
            html.Div(
                className="L_kw", children=[html.Plaintext("KW")]),
            html.Div(
                className="R_kw", children=[html.Plaintext("KW")]),
            html.Div(
                className="S_I_rpm", children=[html.Plaintext("rpm")]),
            html.Div(
                className="S_I_nm", children=[html.Plaintext("Nm")]),
            html.Div(
                className="S_L_rpm", children=[html.Plaintext("rpm")]),
            html.Div(
                className="S_L_nm", children=[html.Plaintext("Nm")]),
            html.Div(
                className="S_R_rpm", children=[html.Plaintext("rpm")]),
            html.Div(
                className="S_R_nm", children=[html.Plaintext("Nm")]),
        ], style={'background-image': 'url(/assets/16.jpg)', 'width': '1920px', 'height': '936px',
                  'background-repeat': 'no-repeat',
                  'background-size': 'cover'}
    )

])



@callback(
    Output('id[0]', 'children'),
    Output('id[1]', 'children'),
    Output('id[2]', 'children'),
    Output('id[3]', 'children'),
    Output('id[4]', 'children'),
    Output('id[5]', 'children'),
    Output('id[6]', 'children'),
    Output('id[7]', 'children'),
    Output('id[8]', 'children'),
    Output('id[9]', 'children'),
    Output('id[10]', 'children'),
    Output('id[11]', 'children'),
    Output('id[12]', 'children'),
    Output('id[13]', 'children'),
    Output('id[14]', 'children'),
    Output('id[15]', 'children'),
    Output('id[16]', 'children'),
    Output('id[17]', 'children'),
    Output('id[18]', 'children'),
    Output('id[19]', 'children'),
    Output('id[20]', 'children'),
    Output('id[21]', 'children'),
    Output('id[22]', 'children'),
    Output('id[23]', 'children'),
    Output('id[24]', 'children'),
    Output('id[25]', 'children'),
    Output('id[26]', 'children'),
    Output('fault_marq', 'children'),
    Output('Run', 'value'),
    Output('Idle', 'value'),
    Output('Fault', 'value'),
    Input('update', 'n_intervals')
)
def update(timer):
    return [ip_spd, LH_Speed, RH_Speed, Gear_Ratio, Running_Step, Trial_No, oil_temp, IP_Torque, LH_Torque, RH_Torque,
            Running_Gear_Id, Present_Step, Bench_Status, Serial_No, ip_pwr, lh_pwr, rh_pwr,
            Target_Gear_Id, Sequence_On, Mode_Of_Bench, Fault_No, s_spd, s_trq, S_LH_Spd, S_LH_Trq, s_r_spd, s_r_trq, Flt_No[Fault_No],
            True if Bench_Status == 0 else False, True if Bench_Status == 1 else False,
            True if Bench_Status == 2 else False]


@callback(
    Output('Run', component_property='style'),
    Output('Idle', component_property='style'),
    Output('Fault', component_property='style'),

    Input('update', 'n_intervals'))
def vis(timer):
    if Bench_Status == 0:
        return [{'position': 'absolute', 'top': '60px', 'left': '1590px', 'color': '#28ff42', 'font-size': '100px',
                 'font-weight': 'bold'},
                {'display': 'none'}, {'display': 'none'}]

    elif Bench_Status == 1:
        return [{'display': 'none'},
                {'position': 'absolute', 'top': '60px', 'left': '1590px', 'color': 'yellow', 'font-size': '100px',
                 'font-weight': 'bold'}, {'display': 'none'}]
    else:
        return [{'display': 'none'}, {'display': 'none'},
                {'position': 'absolute', 'top': '60px', 'left': '1590px', 'color': 'red',
                 'font-size': '100px', 'font-weight': 'bold'}]


@callback(
    Output('MAN_MODE', component_property='style'),
    Output('AUTO_MODE', component_property='style'),
    Input('update', 'n_intervals'))
def vis(timer):
    if Mode_Of_Bench == 0:
        return [{'position': 'absolute', 'left': '12px', 'top': '60px', 'font-size': '15px', 'text-align': 'center',
                 'font-weight': 'bold',
                 'height': '40px', 'width': '150px', 'background-color': "#28ff42"}, {'display': 'none'}]

    elif Mode_Of_Bench == 1:
        return [{'display': 'none'},
                {'position': 'absolute', 'text-align': 'center', 'left': '12px', 'top': '60px', 'font-size': '15px',
                 'font-weight': 'bold', 'height': '40px', 'width': '150px', 'background-color': "#28ff42",
                 'color': 'black'}]


@callback(Output('date', 'children'), [Input('interval-component', 'n_intervals')])
def update_date(n):
    tz_Ind = pytz.timezone('Asia/Kolkata')
    e = datetime.datetime.now(tz_Ind)
    return str(e.strftime("%d-%b-%y %I:%M:%S%p"))




@callback(Output('button', 'n_clicks'),
              Output('popup', 'displayed'),
              Output('popup', 'message'),
              Output('mail', 'value'),
              Input('mail', 'value'),
              Input('button', 'n_clicks'))
def add_mail(value, n_clicks):
    if n_clicks :
        exist_count = res.count(value)

        # checking if it is more than 0
        if exist_count > 0:
            message = "{} already Exists...!".format(value)
            return [0, True, message, None]
        elif value == None or value == "":
            message = "Please enter an mailid to add...!"
            return [0, True, message, None]
        elif exist_count == 0 and value != None and value != "":
            print(value)
            mydb = mysql.connector.connect(
                host="rgdyna-ci-mysql-test.mysql.database.azure.com",
                user="Dyna_Software",
                password="DiS3#4344",
                database="test"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO emailid (mailid, name) VALUES (%s, %s)"
            val = (value, "amirul")

            mycursor.execute(sql, val)

            mydb.commit()
            message = "{} was added  successfully...!".format(value)
            return [0, True, message, ""]

    message = " "
    return [0, False, message, value]


@callback(Output('checkbox-group', 'options'),
          Output('dropdown', 'options'),
          Input('interval-component', 'n_intervals'))
def Display_mail(n):
        #print(res)
        return [res, res]


@callback(Output('del', 'n_clicks'),
          Output('delete-popup', 'displayed'),
          Output('delete-popup', 'message'),
          Output('dropdown', 'value'),
          Input('dropdown', 'value'),
          Input('del', 'n_clicks'))
def delete_mail(value, n_clicks):
    print(value)
    if n_clicks:
        if value != None and value != "":
            mydb = mysql.connector.connect(
                host="rgdyna-ci-mysql-test.mysql.database.azure.com",
                user="Dyna_Software",
                password="DiS3#4344",
                database="test"
            )
            mycursor = mydb.cursor()

            sql = "DELETE FROM emailid WHERE mailid = %s"
            adr = (value,)

            mycursor.execute(sql, adr)

            mydb.commit()
            message = "{} deleted successfully...!".format(value)
            return 0, True, message, None
        else:
            message = "Please select an Mailid to delete...!"
            return 0, True, message, None
    message=""
    return 0, False, message, value


@callback(Output("save", "n_clicks"),
          Output('update-popup', 'displayed'),
          Output('update-popup', 'message'),
          Output('detail', 'open'),
          Input("checkbox-group", "value"),
          Input("save", "n_clicks"))
def checkbox(value, n_clicks):
    if n_clicks:
        print(len(value))
        if len(value) != 0:
            mydb = mysql.connector.connect(
                host="rgdyna-ci-mysql-test.mysql.database.azure.com",
                user="Dyna_Software",
                password="DiS3#4344",
                database="test"
            )
            mycursor = mydb.cursor()

            var_string = ', '.join(value)
            varstring1 = ', '.join(res1)
            sql = "UPDATE selectedemailid SET mailid = %s WHERE mailid = %s"
            val = (var_string, varstring1)
            #sql = "INSERT INTO selectedemailid (mailid, name) VALUES (%s, %s)"
            #val = (var_string, "amirul")
            mycursor.execute(sql, val)
            mydb.commit()
            message = "{} updated Successfully...!".format(value)
            return [0, True, message, None]
        else:
            message = "Please select Mailid to update...!"
            return [0, True, message, False]
    message = ""
    return [0, False, message, False]


@callback(
    [Output("modal", "is_open"),
],
    Input("open", "n_clicks"),
    Input("close", "n_clicks"),
)
def open_modal(liveview, liveview1):
    ctx = dash.callback_context


    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "open":
        return [True]
    elif button_id == "close":
        return [False]
    else:
        return [False]


@dash_app.callback(
    Output('url_login', 'pathname'), Output('output-state', 'children'), Output('uname-box', 'value'),
    Output('pwd-box', 'value'), [Input('login-button', 'n_clicks')],
    [State('uname-box', 'value'), State('pwd-box', 'value')])
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        if username == 'Dynaspede' and password == '123':
            user = User(username)
            login_user(user)
            return '/select', '', '', ''
        else:
            return '/login', 'Incorrect username or password', '', ''
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update


# Mimic Screen
mimic = html.Div(
    [
        html.Div([dcc.Dropdown(
            [

                {
                    "label": html.Div(
                        [
                            dcc.Link('Dashboard', href='/dashboard')
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "Julia",
                },
                {
                    "label": html.Div(
                        [
                            dcc.Link('Datalog', href='/datalog')
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "R",
                },
                {
                    "label": html.Div(
                        [
                            dcc.Link('Graph', href='/graph')
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "T",
                },
                {
                    "label": html.Div(
                        [
                            dcc.Link('Logout', href='/logout')
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "Python",
                },
            ], style={'backgroundColor': 'green', 'textAlign': 'center', 'color': 'white'}, placeholder="Mimic"
        )], style={'position': 'absolute', 'top': '50px', 'left': '1715px', 'height': '40px', 'width': '150px'}),

        dcc.Interval(id='interval-component', interval=500, n_intervals=0),
        html.Div(
            className="date", children=[html.Plaintext(id='date1')]),
        dcc.Interval(id='update', interval=100),

        html.Div(
            className="text100", children=[daq.Gauge(id='id1[0]', showCurrentValue=True, size=250,
                                                     style={'position': 'absolute', 'top': '0px', 'left': '4px',
                                                            'font-Size': '200px'}, max=5000,
                                                     min=0, label={'label': 'IP_SPEED',
                                                                   'style': {'font-size': 20, 'color': 'aqua',
                                                                             'font-weight': 'bold'}},
                                                     color='#28ff42', )]),
        html.Div(
            className="text101", children=[daq.Gauge(id='id1[1]', showCurrentValue=True, size=250,
                                                     style={'position': 'absolute', 'top': '0px', 'left': '5px',
                                                            'font-Size': '200px'}, max=500,
                                                     min=0, label={'label': 'IP_Torque',
                                                                   'style': {'font-size': 20, 'color': 'aqua',
                                                                             'font-weight': 'bold'}},
                                                     color='yellow', )]),
        html.Div(
            className="text102", children=[daq.Gauge(id='id1[2]', showCurrentValue=True, size=250,
                                                     style={'position': 'absolute', 'top': '0px', 'left': '20px',
                                                            'font-Size': '200px'}, max=5000,
                                                     min=0, label={'label': 'LH_SPEED',
                                                                   'style': {'font-size': 20, 'color': 'aqua',
                                                                             'font-weight': 'bold'}},
                                                     color='#28ff42')]),
        html.Div(
            className="text103", children=[daq.Gauge(id='id1[3]', showCurrentValue=True, size=250,
                                                     style={'position': 'absolute', 'top': '0px', 'left': '40px',
                                                            'font-Size': '200px'}, max=1000,
                                                     min=0, label={'label': 'LH_Torque',
                                                                   'style': {'font-size': 20, 'color': 'aqua',
                                                                             'font-weight': 'bold'}},
                                                     color='yellow', )]),
        html.Div(
            className="text104", children=[daq.Gauge(id='id1[4]', showCurrentValue=True, size=250,
                                                     style={'position': 'absolute', 'top': '0px', 'left': '60px',
                                                            'font-Size': '200px'}, max=5000,
                                                     min=0, label={'label': 'RH_SPEED',
                                                                   'style': {'font-size': 20, 'color': 'aqua',
                                                                             'font-weight': 'bold'}},
                                                     color='#28ff42')]),
        html.Div(
            className="text105", children=[daq.Gauge(id='id1[5]', showCurrentValue=True, size=250,
                                                     style={'position': 'absolute', 'top': '0px', 'left': '70px',
                                                            'font-Size': '200px'}, max=1000,
                                                     min=0, label={'label': 'RH_Torque',
                                                                   'style': {'font-size': 20, 'color': 'aqua',
                                                                             'font-weight': 'bold'}},
                                                     color='yellow', )]),
        html.Div(
            className="text106", children=[daq.Thermometer(id='id1[6]', showCurrentValue=True,
                                                           style={'position': 'absolute', 'top': '0px', 'left': '110px',
                                                                  'font-Size': '200px'}, max=100,
                                                           min=0, label={'label': 'Oil_Temp',
                                                                         'style': {'font-size': 20, 'color': 'aqua',
                                                                                   'font-weight': 'bold'}},
                                                           color='red')]),
        html.Div(
            className="text107", children=[daq.LEDDisplay(id='id1[7]', size=25, color="black", value="0.0", )]),
        html.Div(
            className="text108", children=[daq.LEDDisplay(id='id1[8]', size=25, color="black", value="0.0", )]),
        html.Div(
            className="text109", children=[daq.LEDDisplay(id='id1[9]', size=25, color="black", value="0.0", )]),
        html.Div(
            className="text110", children=[daq.LEDDisplay(id='id1[10]', size=25, color="black", value="0.0", )]),
        html.Div(
            className="text111", children=[daq.LEDDisplay(id='id1[11]', size=25, color="black", value="0.0", )]),

        html.Div(
            className="text112", children=[
                daq.Gauge(id='id1[12]', showCurrentValue=True, style={'position': 'absolute', 'font-Size': '200px'},
                          max=100,
                          min=0, label={'label': 'IP_POWER',
                                        'style': {'font-size': 20, 'color': 'aqua', 'font-weight': 'bold'}})]),
        html.Div(
            className="text113", children=[
                daq.Gauge(id='id1[13]', showCurrentValue=True, style={'position': 'absolute', 'font-Size': '200px'},
                          max=100,
                          min=0, label={'label': 'LH_POWER',
                                        'style': {'font-size': 20, 'color': 'aqua', 'font-weight': 'bold'}})]),
        html.Div(
            className="text114", children=[
                daq.Gauge(id='id1[14]', showCurrentValue=True, style={'position': 'absolute', 'font-Size': '200px'},
                          max=100,
                          min=0, label={'label': 'RH_POWER',
                                        'style': {'font-size': 20, 'color': 'aqua', 'font-weight': 'bold'}})]),

        html.Div(
            className="Header", children=[html.H1("Endurance & Differential Test(Siemens Drive)")]),
        html.Div(
            className="Marquee", children=[html.Marquee(
                "Welcome To Dynaspede 4.0...!, Dynaspede Integrated Systems(P) Limited, Visit us at www.dynaspede.com, Contact No- 8667391167")]),

        # html.Button('ACK', style={'position': 'absolute', 'top': '55px', 'left': '1652px',
        #         'background-color': 'greenyellow', 'width': '120px', 'height': '60px', 'font-size': '20px', 'font-weight': 'bold'}),
        # html.Button('LOGOUT', style={'position': 'absolute', 'top': '55px', 'left': '1770px',
        # 'background-color': 'lightpink', 'width': '120px', 'height': '60px',
        # 'font-size': '20px', 'font-weight': 'bold'}),

        daq.Indicator(id='Run1', style=dict(display='none'), size=50, color="#28ff42", label="Run",
                      labelPosition="bottom"),
        daq.Indicator(id='Idle1', style=dict(display='none'), size=50, color="yellow", label="Idle",
                      labelPosition="bottom"),
        daq.Indicator(id='Fault1', style=dict(display='none'), size=50, color="red", label="Fault",
                      labelPosition="bottom"),

        dcc.Input(id='MAN_MODE1', style=dict(display='none'), value="MAN_MODE"),
        dcc.Input(id='AUTO_MODE1', style=dict(display='none'), value="AUTO_MODE"),

        html.Div(
            className="Label100", children=[html.Plaintext("Machine")]),
        html.Div(
            className="Label101", children=[html.Plaintext("Status")]),
        html.Div(
            className="Label102", children=[html.Plaintext("Gear_Ratio")]),
        html.Div(
            className="Label103", children=[html.Plaintext("Running_Gear_Id")]),
        html.Div(
            className="Label104", children=[html.Plaintext("Target_Gear_Id")]),
        html.Div(
            className="Label105", children=[html.Plaintext("Running_Step")]),
        html.Div(
            className="Label106", children=[html.Plaintext("Present_Step")]),
        html.Div(
            className="Label107", children=[html.Plaintext("RPM")]),
        html.Div(
            className="Label108", children=[html.Plaintext("RPM")]),
        html.Div(
            className="Label109", children=[html.Plaintext("RPM")]),
        html.Div(
            className="Label110", children=[html.Plaintext("NM")]),
        html.Div(
            className="Label111", children=[html.Plaintext("NM")]),
        html.Div(
            className="Label112", children=[html.Plaintext("NM")]),
        html.Div(
            className="Label113", children=[html.Plaintext("KW")]),
        html.Div(
            className="Label114", children=[html.Plaintext("KW")]),
        html.Div(
            className="Label115", children=[html.Plaintext("KW")]),
    ], style={'background-image': 'url(/assets/11.jpg)', 'position': 'fill',
              'width': '1920px', 'height': '936px', 'background-repeat': 'no-repeat', 'background-size': 'cover'}
)


@callback(
    Output('id1[0]', 'value'),
    Output('id1[1]', 'value'),
    Output('id1[2]', 'value'),
    Output('id1[3]', 'value'),
    Output('id1[4]', 'value'),
    Output('id1[5]', 'value'),
    Output('id1[6]', 'value'),
    Output('id1[7]', 'value'),
    Output('id1[8]', 'value'),
    Output('id1[9]', 'value'),
    Output('id1[10]', 'value'),
    Output('id1[11]', 'value'),
    Output('id1[12]', 'value'),
    Output('id1[13]', 'value'),
    Output('id1[14]', 'value'),

    Output('Run1', 'value'),
    Output('Idle1', 'value'),
    Output('Fault1', 'value'),

    Input('update', 'n_intervals')
)
def update(timer):
    return [IP_Speed, iptrq, lhspd, lhtrq, rhspd, rhtrq, Oil_Temperature, Gear_Ratio, Running_Gear_Id, Target_Gear_Id,
            Running_Step, Present_Step, IP_Power, LH_Power, RH_Power,
            True if Bench_Status == 0 else False, True if Bench_Status == 1 else False,
            True if Bench_Status == 2 else False, ]


@callback(
    Output('Run1', component_property='style'),
    Output('Idle1', component_property='style'),
    Output('Fault1', component_property='style'),
    Input('update', 'n_intervals'))
def vis(timer):
    if Bench_Status == 0:
        return [{'position': 'absolute', 'top': '60px', 'left': '1590px', 'color': '#28ff42', 'font-size': '100px',
                 'font-weight': 'bold'},
                {'display': 'none'}, {'display': 'none'}]

    elif Bench_Status == 1:
        return [{'display': 'none'},
                {'position': 'absolute', 'top': '60px', 'left': '1590px', 'color': 'yellow', 'font-size': '100px',
                 'font-weight': 'bold'}, {'display': 'none'}]
    else:
        return [{'display': 'none'}, {'display': 'none'},
                {'position': 'absolute', 'top': '60px', 'left': '1590px', 'color': 'red',
                 'font-size': '100px', 'font-weight': 'bold'}]


@callback(
    Output('MAN_MODE1', component_property='style'),
    Output('AUTO_MODE1', component_property='style'),
    Input('update', 'n_intervals'))
def vis(timer):
    if Mode_Of_Bench == 0:
        return [{'position': 'absolute', 'left': '12px', 'top': '60px', 'font-size': '15px', 'text-align': 'center',
                 'font-weight': 'bold', 'width': '150px', 'height': '40px', 'background-color': "aqua"},
                {'display': 'none'}]

    elif Mode_Of_Bench == 1:
        return [{'display': 'none'},
                {'position': 'absolute', 'left': '12px', 'top': '60px', 'font-size': '15px', 'text-align': 'center',
                 'font-weight': 'bold', 'width': '150px', 'height': '40px', 'background-color': "#28ff42"}]


@callback(Output('date1', 'children'), [Input('interval-component', 'n_intervals')])
def update_date(n):
    tz_Ind = pytz.timezone('Asia/Kolkata')
    e = datetime.datetime.now(tz_Ind)
    return str(e.strftime("%d-%m-%y %I:%M:%S%p"))


# Datalog Screen
datalog = html.Div([
    html.Div([dcc.Dropdown(
        [

            {
                "label": html.Div(
                    [
                        dcc.Link('Dashboard', href='/dashboard')
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Julia",
            },
            {
                "label": html.Div(
                    [
                        dcc.Link('Mimic', href='/mimic')
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "R",
            },
            {
                "label": html.Div(
                    [
                        dcc.Link('Graph', href='/graph')
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "T",
            },
            {
                "label": html.Div(
                    [
                        dcc.Link('Logout', href='/logout')
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Python",
            },
        ], style={'backgroundColor': 'green', 'textAlign': 'center', 'color': 'white'}, placeholder="Datalog"
    )], style={'position': 'absolute', 'top': '50px', 'left': '1715px', 'height': '40px', 'width': '150px'}),

    dcc.Interval(id='interval-component', interval=30000),
    html.Div(
        className="Header", children=[
            html.H1("Endurance & Differential Test(Siemens Drive)")], style={'color': '#28ff42'}),
    html.Div([dash_table.DataTable(style_header={'background-image': 'url(/assets/13.jpg)', 'fontWeight': 'bold'},

                                   style_data={'color': 'black', 'background-image': 'url(/assets/13.jpg)',
                                               'fontWeight': 'bold'},
                                   id='data_table',
                                   columns=[{'name': 'Date_And_Time', 'id': 'column'},
                                            {'name': 'IP_Speed', 'id': 'column1'},
                                            {'name': 'IP_TORQUE', 'id': 'column2'},
                                            {'name': 'IP_POWER', 'id': 'column3'},
                                            {'name': 'LH_SPEED', 'id': 'column4'},
                                            {'name': 'LH_TORQUE', 'id': 'column5'},
                                            {'name': 'LH_POWER', 'id': 'column6'},
                                            {'name': 'RH_SPEED', 'id': 'column7'},
                                            {'name': 'RH_TORQUE', 'id': 'column8'},
                                            {'name': 'RH_POWER', 'id': 'column9'},
                                            {'name': 'GEAR_RATIO', 'id': 'column10'},
                                            {'name': 'RUNNING_GEAR_ID', 'id': 'column11'},
                                            {'name': 'TARGET_GEAR_ID', 'id': 'column12'},
                                            {'name': 'PRESENT_STEP', 'id': 'column13'},
                                            {'name': 'RUNNING_STEP', 'id': 'column14'},
                                            {'name': 'SEQUENCE_ON', 'id': 'column15'},
                                            {'name': 'TRIAL_NO', 'id': 'column16'},
                                            {'name': 'BENCH_STATUS', 'id': 'column17'},
                                            {'name': 'MODE_OF_BENCH', 'id': 'column18'},
                                            {'name': 'OIL_TEMPERATURE', 'id': 'column19'},
                                            {'name': 'SERIAL_NO', 'id': 'column20'},
                                            ],
                                   data=[{'column0': 0}])],
             style={'position': 'absolute', 'top': '100px', 'left': '25', 'width': '1920px'}),
    html.Div(id='output_div'),

], style={'background-image': 'url(/assets/15.png)', 'width': '1920px', 'height': '1920px',
          'background-repeat': 'no-repeat', 'background-size': 'cover'})


@callback(
    Output('data_table', 'data'),
    Input('interval-component', 'n_intervals'),
    [State('data_table', 'data'),
     State('data_table', 'columns')]
)
def updateData(n, data, columns):
    tz_Ind = pytz.timezone('Asia/Kolkata')
    e = datetime.datetime.now(tz_Ind)
    x = str(e.strftime("%d-%m-%y %I:%M:%S %p"))

    data.insert(0, {
        'column': x,
        'column1': ip_spd,
        'column2': IP_Torque,
        'column3': ip_pwr,
        'column4': LH_Speed,
        'column5': LH_Torque,
        'column6':  lh_pwr,
        'column7': RH_Speed,
        'column8': RH_Torque,
        'column9':  rh_pwr,
        'column10': Gear_Ratio,
        'column11': Running_Gear_Id,
        'column12': Target_Gear_Id,
        'column13': Present_Step,
        'column14': Running_Step,
        'column15': Sequence_On,
        'column16': Trial_No,
        'column17': Bench_Status,
        'column18': Mode_Of_Bench,
        'column19': oil_temp,
        'column20': Serial_No})
    return data


# Graph Screen
graph = html.Div([
    html.Div([dcc.Dropdown(
        [
            {
                "label": html.Div(
                    [
                        dcc.Link('Dashboard', href='/dashboard')
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "J",
            },
            {
                "label": html.Div(
                    [
                        dcc.Link('Mimic', href='/mimic')
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "R",
            },
            {
                "label": html.Div(
                    [
                        dcc.Link('Datalog', href='/datalog')
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "T",
            },
            {
                "label": html.Div(
                    [
                        dcc.Link('Logout', href='/logout')
                    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Python",
            },
        ], style={'backgroundColor': 'green', 'textAlign': 'center', 'color': 'white'}, placeholder="Graph")],
        style={'position': 'absolute', 'top': '50px', 'left': '1715px', 'height': '40px', 'width': '150px'}),

    html.Div(
        className="Header",
        children=[html.H1("Endurance & Differential Test(Siemens Drive)", style={'color': '#bbff35'})]),
    html.Plaintext("IP_Torque(NM)", style={'position': 'absolute', 'top': '300px', 'left': '15px', 'font-size': '15px',
                                           'transform': 'rotate(-90deg)', 'color': 'white'}),
    html.Plaintext("LH_Torque(NM)", style={'position': 'absolute', 'top': '300px', 'left': '620px', 'font-size': '15px',
                                           'transform': 'rotate(-90deg)', 'color': 'white'}),
    html.Plaintext("RH_Torque(NM)",
                   style={'position': 'absolute', 'top': '300px', 'left': '1230px', 'font-size': '15px',
                          'transform': 'rotate(-90deg)', 'color': 'white'}),
    html.Plaintext("Time(Ms)", style={'position': 'absolute', 'top': '550px', 'left': '290px', 'font-size': '15px',
                                      'color': 'white'}),
    html.Plaintext("Time(Ms)", style={'position': 'absolute', 'top': '550px', 'left': '910px', 'font-size': '15px',
                                      'color': 'white'}),
    html.Plaintext("Time(Ms)", style={'position': 'absolute', 'top': '550px', 'left': '1510px', 'font-size': '15px',
                                      'color': 'white'}),
    html.Plaintext("IP_Torque", style={'position': 'absolute', 'top': '55px', 'left': '90px', 'font-size': '20px',
                                       'color': 'white'}),
    html.Plaintext("LH_Torque", style={'position': 'absolute', 'top': '55px', 'left': '700px', 'font-size': '20px',
                                       'color': 'white'}),
    html.Plaintext("RH_Torque", style={'position': 'absolute', 'top': '55px', 'left': '1310px', 'font-size': '20px',
                                       'color': 'white'}),

    dcc.Interval(
        id='interval_extendablegraph_update', interval=100, n_intervals=100, max_intervals=-1),

    html.Div([deg.ExtendableGraph(

        id='extendablegraph_example', figure=dict(data=[{'x': [], 'y': [], 'mode': 'lines+markers'}]), )],
        style={'width': '500px', 'position': 'absolute', 'left': '90px',
               'top': '100px'}),

    html.Div([deg.ExtendableGraph(
        id='extendablegraph_example1', figure=dict(data=[{'x': [], 'y': [], 'mode': 'lines+markers'}]))],
        style={'width': '500px', 'position': 'absolute', 'top': '100px',
               'left': '700px'}),
    html.Div([deg.ExtendableGraph(
        id='extendablegraph_example2', figure=dict(data=[{'x': [], 'y': [], 'mode': 'lines+markers'}]))],
        style={'width': '500px', 'position': 'absolute', 'top': '100px',
               'left': '1310px', 'background-color': 'yellow'}),
    html.Div(id='output'), ], style={'background-image': 'url(/assets/6.jpg)', 'width': '1920px', 'height': '936px',
                                     'background-repeat': 'no-repeat', 'background-size': 'cover'})


@callback(Output('extendablegraph_example', 'extendData'),
          Input('interval_extendablegraph_update', 'n_intervals'),
          State('extendablegraph_example', 'figure'))
def update_extendData(n_intervals, existing):
    x_new = n_intervals
    y_new = IP_Torque
    return [dict(x=[x_new], y=[y_new])], [1], 100


@callback(Output('extendablegraph_example1', 'extendData'),
          Input('interval_extendablegraph_update', 'n_intervals'),
          State('extendablegraph_example1', 'figure'))
def update_extendData(n_intervals, existing):
    x_new = n_intervals
    y_new = LH_Torque
    return [dict(x=[x_new], y=[y_new])], [1], 100


@callback(Output('extendablegraph_example2', 'extendData'),
          Input('interval_extendablegraph_update', 'n_intervals'),
          State('extendablegraph_example2', 'figure'))
def update_extendData(n_intervals, existing):
    x_new = n_intervals
    y_new = RH_Torque
    return [dict(x=[x_new], y=[y_new])], [1], 100


@dash_app.callback(Output('login-status', 'data'), [Input('url', 'pathname')])
def login_status(url):
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated and url != '/logout':
        return current_user.get_id()
    else:
        return 'loggedout'


# Main router
@dash_app.callback(Output('page-content', 'children'), Output('redirect', 'pathname'),
                   [Input('url', 'pathname')])
def display_page(pathname):
    url = dash.no_update

    if pathname == '/select':
        if current_user.is_authenticated:
            view = select
        else:
            view = login
            url = '/login'
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            view = login
        else:
            view = login
            url = '/login'

    elif pathname == '/dashboard':
        if current_user.is_authenticated:
            view = dashboard
        else:
            view = login
            url = '/login'
    elif pathname == '/mimic':
        if current_user.is_authenticated:
            view = mimic
        else:
            view = login
            url = '/login'
    elif pathname == '/datalog':
        if current_user.is_authenticated:
            view = datalog
        else:
            view = login
            url = '/login'
    elif pathname == '/graph':
        if current_user.is_authenticated:
            view = graph
        else:
            view = login
            url = '/login'
    else:
        if current_user.is_authenticated:
            logout_user()
            view = login
        else:

            view = login
            url = '/login'
    # You could also return a 404 "URL not found" page here
    return view, url


if __name__ == '__main__':
    dash_app.run_server(debug=False)
