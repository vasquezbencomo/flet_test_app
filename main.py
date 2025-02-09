
import flet as ft
from flet import *
import pyrebase
import firebase_admin
from firebase_admin import credentials, db



firebaseConfig = {
  'apiKey': "AIzaSyBgoWbGTbBpWsMvZghNn39qagk29P-7D1k",
  'authDomain': "login-react-firebase-63636.firebaseapp.com",
  'databaseURL': "https://login-react-firebase-63636-default-rtdb.firebaseio.com",
  'projectId': "login-react-firebase-63636",
  'storageBucket': "login-react-firebase-63636.firebasestorage.app",
  'messagingSenderId': "632947844231",
  'appId': "1:632947844231:web:dd506446d185618907c422"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

cred = credentials.Certificate('login-react-firebase-63636-firebase-adminsdk-bbo5s-10e8cb69ec.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://login-react-firebase-63636-default-rtdb.firebaseio.com/'
})


class App(ft.Container):


    def __init__(self, page):

        super().__init__(expand=True)

        self.page = page
        self.page.window_width = 400
        self.thread_running = True
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"
        self.page.bgcolor = ft.colors.BLACK87


        self.confirm_dialog = ft.AlertDialog(
            modal= True,
            title= ft.Text("Por favor confirme"),
            content= ft.Text("¿Está seguro de que desea salir de la aplicación?"),
            actions=[
                ft.ElevatedButton("SI", on_click= self.yes_click),
                ft.OutlinedButton("NO", on_click= self.no_click)
            ]
        )

        self.alarm_error = ft.AlertDialog(
            modal= True,
            title= ft.Text("Error"),
            content= ft.Text("Usuario o Contraseña Incorrecto"),
            actions=[
                ft.ElevatedButton("Continuar", on_click= self.cont_click)
            ]
        )

        self.alarm_update = ft.AlertDialog(
            modal= True,
            title= ft.Text("Dato Actualizado"),
            #content= ft.Text("Correctamente"),
            actions=[
                ft.ElevatedButton("Continuar", on_click= self.cont_click)
            ]
        )

        self.user_text = ft.TextField(
            width=350,
            height=40,
            hint_text= 'Usuario',
            border ='underline',
            color ='black',
            prefix_icon = ft.icons.ACCOUNT_BOX,
        )


        self.pass_text = ft.TextField(
            width=350,
            height=40,
            hint_text= 'Contraseña',
            border ='underline',
            color ='black',
            prefix_icon = ft.icons.LOCK,
            password = True,
        )


        gradient_menu = ft.LinearGradient([ft.colors.BLUE_GREY, ft.colors.LIGHT_BLUE])

        self.info_login = ft.Container(
                gradient=gradient_menu,
                #expand=True,
                border_radius=10,
                bgcolor="blue",
                width=400,
                height=500,
                visible=True,
                content=ft.Column([
                    ft.Container(
                        ft.Image(
                            src='kiriLogo.png',
                            width=70,
                            border_radius=20
                        ),
                        padding= ft.padding.only(150,20)
                    ),
                    ft.Text(
                        'Iniciar Sesión',
                        width=360,
                        size=30,
                        weight ='w900',
                        text_align = 'center'
                    ),
                    ft.Container(
                        self.user_text,
                        padding = ft.padding.all(20),
                    ),
                    ft.Container(
                        self.pass_text,
                        padding = ft.padding.all(20)
                    ),
                    ft.Container(
                        ft.ElevatedButton(
                            content = ft.Text(
                                'INICIAR',
                                color = 'white',
                                weight ='w500',
                            ),
                            width =350,
                            bgcolor = 'black',
                            on_click=self.login
                        ),
                        padding = ft.padding.all(20)
                    ),
                    ft.Text(
                        'AUTOMATIZACION INDUSTRIAL RV CA',
                        width=360,
                        size=15,
                        weight ='w900',
                        text_align = 'center'
                    ),
                    ft.Text(
                        'automatizacionindustrialrv@gmail.com',
                        width=360,
                        size=15,
                        weight ='w900',
                        text_align = 'center'
                    ),
                ])

                )

        self.info_device = ft.Container(
                gradient=gradient_menu,
                #expand=True,
                border_radius=10,
                bgcolor="blue",
                width=400,
                height=500,
                visible=False,
                content=ft.Column([
                    ft.Container(
                        ft.Image(
                            src='assets/kiriLogo.png',
                            width=70,
                            border_radius=20
                        ),
                        padding= ft.padding.only(150,20)
                    ),
                    ft.Text(
                        'CONTROLADORES DE TEMPERATURAS',
                        width=360,
                        size=30,
                        weight ='w900',
                        text_align = 'center'
                    ),
                    ft.Container(
                        ft.ElevatedButton(
                            content = ft.Text(
                                'ACTUALIZAR',
                                color = 'white',
                                weight ='w500',
                            ),
                            width =350,
                            bgcolor = 'black',
                            on_click=self.update_fb
                        ),
                        padding = ft.padding.all(20)
                    ),
                    ft.Container(
                        ft.ElevatedButton(
                            content = ft.Text(
                                'CERRAR SESION',
                                color = 'white',
                                weight ='w500',
                            ),
                            width =350,
                            bgcolor = 'black',
                            on_click=self.login_off
                        ),
                        padding = ft.padding.all(20)
                    ),
                ])
            )


        self.page.add(ft.Column(
            expand=True,
            width=400,
            scroll=True,
            controls=[
                self.info_login,
                self.info_device,
            ]
        ))


    def login(self, e):
        user=self.user_text.value
        password=self.pass_text.value
        try:
            login = auth.sign_in_with_email_and_password(user, password)
            email = auth.get_account_info(login['idToken'])['users'][0]['email']
            self.info_login.visible=False
            self.info_device.visible=True
            self.page.update()

        except:
            self.page.overlay.append(self.alarm_error)
            self.alarm_error.open = True
            self.page.update()

        return

    def update_fb(self, e):
        ref = db.reference('/kdevice02/kcts01')
        data = 580
        ref.set(data)
        self.page.overlay.append(self.alarm_update)
        self.alarm_update.open = True
        self.page.update()


    def login_off(self, e):
        self.info_login.visible=True
        self.info_device.visible=False
        self.pass_text.value=''
        self.page.update()

    def yes_click(self, e):
        self.page.window_close()
        self.page.window_destroy()


    def no_click(self, e):
        self.confirm_dialog.open = False
        self.page.update()

    def cont_click(self, e):
        self.alarm_error.open = False
        self.alarm_update.open = False
        self.page.update()



ft.app(target=App, view=ft.AppView.WEB_BROWSER)







