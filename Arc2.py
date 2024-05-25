#region Import y Globales
import tkinter
from tkinter import *
from tkinter import messagebox, ttk
from copy import copy
import pandas
import random
import os

global lista_equipos  # Lista de equipos actuales
global lista_equipos_nombre  # Auxiliar de lista_equipos
global historial_equipos  # Historial de cambios de nombres
global lista_labels_nombre  # Lista de etiquetas en pestaña Equipos
global lista_labels_numero  # Lista de etiquetas de número de equipo en pestaña Equipos
global lista_labels_cmbb  # Lista de comboboxes de avatares en pestaña Equipos
global cambios  # Suma nombre de equipo, cambio de equipo y eliminación del equioi al historial, resta regresar
global preguntas_lbl  # Lista de etiquetas de preguntas
global preguntas_btn  # Lista de botones de preguntas faltantes
global equipos  # Pestaña de selección de equipos
global puntaje_equipos  # Puntaje de los equipos
global bot_seg_lista  # Lista de equipos a participar si se quiere reresponder
global contador_selec  # Cuántas preguntas han sido seleccionadas
global categorias_puntos  # Número de puntajes

categorias_puntos = 5
#endregion

# Importación de archivo de preguntas y de texto de instrucciones
excel_file = pandas.read_excel("file_excel_questions")  # Insert direct link here.
txt_file = "instructions_file"  # Insert .txt file complete link here.

categorias = ["Category 1", "Category 2", "Category 3", "Category 4"]

preguntas_tot = 76  # Preguntas totales del archivo de Excel.
columnas_tot = 7  # Elementos del vector de cada pregunta. No cambiar a menos que el formato del Excel cambie.


# region Programación
# region Adicionales
matriz_file = excel_file.values.tolist()
with open(txt_file, "r") as file:
    txt_instr = file.read()
matriz = []  # Preguntas separadas por categorías con todos los elementos
matriz_contador = 0
tiempos = [10, 15, 20, 25, 30]


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


# Creación de matriz del archivo de Excel
for _ in range(preguntas_tot):
    matriz_aux = []
    matriz_contador += 1
    for j in range(columnas_tot):
        matriz_aux.append(matriz_file[matriz_contador-1][j])
    matriz.append(matriz_aux)


def terminar_juego(foo4):
    if contador_selec == categorias_puntos * len(categorias):
        maximo = max(puntaje_equipos)
        index_win_eq = []
        index_win_pun = []
        for r in range(len(puntaje_equipos)):
            if puntaje_equipos[r] == maximo:
                index_win_eq.append(lista_equipos[r])
                index_win_pun.append(puntaje_equipos[r])
        if len(lista_equipos) == 1:
            messagebox.showinfo(title="Fin del juego", message=f"Puntaje: {puntaje_equipos[0]}")
        else:
            if len(index_win_eq) == 1:
                messagebox.showinfo(message=f"El ganador es {index_win_eq[0]} con"
                                            f" {index_win_pun[0]} puntos", title="Fin del juego")
            if len(index_win_eq) > 1:
                t = 0
                msg_ganadores = ""
                for t in range(len(index_win_eq)):
                    if (t+1) == len(index_win_eq):
                        msg_ganadores += f" y {index_win_eq[t]} con {index_win_pun[t]} puntos."
                    else:
                        msg_ganadores += f"{index_win_eq[t]} con {index_win_pun[t]} puntos, "
                messagebox.showinfo(message=f"Los ganadores son: {msg_ganadores}", title="Fin del juego")
        foo4.destroy()
        Boton_jugar.config(state="normal")
        root.protocol("WM_DELETE_WINDOW", root.destroy)


# Evita cerrar con el botón de la esquina superior derecha
def botx():
    return
# endregion


# region Programación Jeoprdy
# Pestaña Principal Jeopardy
def jeopardy():
    global equipos
    global lista_equipos
    global preguntas_btn
    global puntaje_equipos
    global contador_selec
    print(lista_equipos)
    contador_selec = 0
    equipos.destroy()
    game = Tk()
    game.title("Jeopardy Químico")
    game.protocol("WM_DELETE_WINDOW", botx)
    game.configure(bg="#00083d")
    preguntas_btn = []
    puntaje_equipos = []

    # Bloquea el botón finalizar
    def desbloq():
        if finish_btn["state"] == "disabled":
            finish_btn.config(state="normal")
            desbloq_btn.config(text="Bloquear botón")
        else:
            finish_btn.config(state="disabled")
            desbloq_btn.config(text="Desbloquear botón")

    # Botón Finalizar
    def terminate():
        Boton_jugar.config(state="normal")
        game.destroy()
        root.protocol("WM_DELETE_WINDOW", root.destroy)

    # Preguntas de botones de pantalla principal
    def pregunta(index_i, index_j):
        preguntas_btn[index_i][index_j].config(text="")
        preguntas_btn[index_i][index_j].config(state="disabled")
        preguntas_btn[index_i][index_j].config(bg="#00083D")
        label_button = Label(game, bg="#00083D")
        label_button.grid(row=index_j+2, column=index_i, ipady=17.5, ipadx=len(categorias[index_i])*7)

        if len(lista_equipos) == 1:
            global puntaje_equipos
            global contador_selec
            contador_selec += 1
            question = Tk()
            question.title(f"{categorias[index_i]} {str((index_j + 1) * 100)}")
            question.protocol("WM_DELETE_WINDOW", botx)
            question.configure(bg="#00083D")
            center_window(question, 700, 300)
            question.columnconfigure(0, weight=1)
            question.columnconfigure(1, weight=1)
            # Se elije la pregunta y se copian las respuestas
            len_num_preguntas = 0  # Cuántas preguntas hay por categoría
            copia_preguntas = []  # Copia las respuestas de la pregunta para no modificar la matriz
            respuestas_posibles = []  # Cuatro respuestas de la pregunta
            for _ in range(len(matriz)):
                respuestas_posibles_aux = []
                if (matriz[_][0] == index_i) & (matriz[_][1] == index_j):
                    copia_preguntas.append(matriz[_])
                    c = 0
                    for i in range(4):
                        if not isinstance(matriz[_][c + 3], str):
                            matriz[_][c + 3] = str(matriz[_][c + 3])
                        respuestas_posibles_aux.append(matriz[_][c + 3])
                        c += 1
                    respuestas_posibles.append(respuestas_posibles_aux)
                    len_num_preguntas += 1

            rng = random.randint(0, len_num_preguntas - 1)
            label_question = Label(question, text=copia_preguntas[rng][2], wraplength=600, bg="#00083D",
                                   fg="white", font=("Dafont", 15, "bold"), pady=10, padx=10)
            label_question.grid(row=0, column=0, columnspan=2)
            respuestas_ocupadas = respuestas_posibles[rng]
            respuestas_ocupadas_ordenadas = respuestas_ocupadas.copy()
            random.shuffle(respuestas_ocupadas)
            respuestas_ocupadas_revueltas = respuestas_ocupadas
            print(respuestas_ocupadas_ordenadas)
            print(respuestas_ocupadas_revueltas)

            def verifyuno(foo5):
                for f in range(len(botones_respuestas)):
                    botones_respuestas[f].config(state="disabled")
                texto_boton = botones_respuestas[foo5].cget("text")
                print(texto_boton)
                if texto_boton == respuestas_ocupadas_ordenadas[0]:
                    # Se asignan los puntos
                    puntaje_equipos[0] += (index_j + 1) * 100
                    lbl_puntaje_equipos[0].config(text=f"{str(puntaje_equipos[0])} puntos")
                    print(puntaje_equipos)
                    question.destroy()
                    root.lower()
                    terminar_juego(game)
                else:
                    root.lower()
                    botones_respuestas[foo5].config(state="disabled")
                    msg = messagebox.askyesno("Respuesta Incorrecta", message="¿Deseas volver a intentar?")
                    if msg:
                        root.lower()
                        for f in range(len(botones_respuestas)):
                            if botones_respuestas[f] != botones_respuestas[foo5]:
                                botones_respuestas[f].config(state="normal")
                        def verify2(foo3):
                            texto_boton = botones_respuestas[foo3].cget("text")
                            print(texto_boton)
                            if texto_boton == respuestas_ocupadas_ordenadas[0]:
                                # Se asignan los puntos
                                puntaje_equipos[0] += (index_j + 1) * 50
                                lbl_puntaje_equipos[0].config(
                                    text=f"{str(puntaje_equipos[0])} puntos")
                                print(puntaje_equipos)
                                question.destroy()
                                root.lower()
                                terminar_juego(game)
                            else:
                                for g in range(len(botones_respuestas)):
                                    botones_respuestas[g].config(state="disabled")
                                messagebox.showinfo("Respuesta Incorrecta",
                                                    message=f"La respuestas correcta es: "
                                                            f"{respuestas_ocupadas_ordenadas[0]}")
                                question.destroy()
                                root.lower()
                                terminar_juego(game)

                        for a in range(len(botones_respuestas)):
                            botones_respuestas[a]["command"] = lambda a=a: verify2(a)
                    else:
                        messagebox.showinfo("Respuesta",
                                            message=f"La respuestas correcta es: "
                                                    f"{respuestas_ocupadas_ordenadas[0]}")
                        question.destroy()
                        root.lower()
                        terminar_juego(game)


            botones_respuestas = []
            ij = 0
            counter_uno = 0
            for i in range(2):
                ji = 0
                for p in range(2):
                    but = Button(question, text=respuestas_ocupadas_revueltas[counter_uno],
                                 command=lambda counter_uno=counter_uno: verifyuno(counter_uno),
                                 fg="white", bg="#060CE9", font=("Dafont", 15, "bold"))
                    botones_respuestas.append(but)
                    but.grid(row=ij + 1, column=ji, columnspan=1, pady=15)
                    ji += 1
                    counter_uno += 1
                ij += 1
            lenlon = []
            for w in botones_respuestas:
                lenlon.append(len(w["text"]))
            center_window(question, 5*max(lenlon)+700, 350)

        elif len(lista_equipos) > 1:
            contador_selec += 1
            question = Tk()
            question.title(f"{categorias[index_i]} {str((index_j + 1) * 100)}")
            question.protocol("WM_DELETE_WINDOW", botx)
            question.configure(bg="#00083D")
            lista_lon_equipos =[]
            for b in range(len(lista_equipos)):
                lista_lon_equipos.append(len(lista_equipos[b]))
            center_window(question, 10*max(lista_lon_equipos)+200, 250+25*len(lista_equipos))
            question.columnconfigure(2, weight=1)

            # Cambia el puntaje en la pestaña del Jeopardy
            def puntos(foo):
                global puntaje_equipos
                for _ in range(len(boton_equipos)):
                    boton_equipos[_].config(state="disabled")
                equipos_part.config(text="")

                # Se elije la pregunta y se copian las respuestas
                len_num_preguntas = 0  # Cuántas preguntas hay por categoría
                copia_preguntas = []  # Copia las respuestas de la pregunta para no modificar la matriz
                respuestas_posibles = []  # Cuatro respuestas de la pregunta
                print(index_i, index_j)
                print(len(matriz))
                for _ in range(len(matriz)):
                    respuestas_posibles_aux = []
                    if (matriz[_][0] == index_i) & (matriz[_][1] == index_j):
                        copia_preguntas.append(matriz[_])
                        c = 0
                        for i in range(4):
                            if not isinstance(matriz[_][c + 3], str):
                                matriz[_][c + 3] = str(matriz[_][c + 3])
                            respuestas_posibles_aux.append(matriz[_][c + 3])
                            c += 1
                        respuestas_posibles.append(respuestas_posibles_aux)
                        len_num_preguntas += 1
                print(len_num_preguntas)

                rng = random.randint(0, len_num_preguntas - 1)
                label_question = Label(question, text=copia_preguntas[rng][2], wraplength=600, bg="#00083D",
                                       fg="white", font=("Dafont", 15, "bold"), pady=10, padx=10)
                label_question.grid(row=0, column=0, columnspan=2)
                center_window(question, 10 * max(lista_lon_equipos) + 900, 250+50*len(lista_equipos))
                respuestas_ocupadas = respuestas_posibles[rng]
                respuestas_ocupadas_ordenadas = respuestas_ocupadas.copy()
                random.shuffle(respuestas_ocupadas)
                respuestas_ocupadas_revueltas = respuestas_ocupadas
                print(respuestas_ocupadas_ordenadas)
                print(respuestas_ocupadas_revueltas)

                # Verifica la respuesta
                def verify(foo1):
                    global bot_seg_lista
                    texto_boton = botones_respuestas[foo1].cget("text")
                    for y in range(len(botones_respuestas)):
                        botones_respuestas[y].config(state="disabled")
                    print(texto_boton)
                    if texto_boton == respuestas_ocupadas_ordenadas[0]:
                        # Se asignan los puntos
                        puntaje_equipos[foo] += (index_j + 1) * 100
                        lbl_puntaje_equipos[foo].config(text=f"{str(puntaje_equipos[foo])} puntos")
                        print(puntaje_equipos)
                        question.destroy()
                        root.lower()
                        terminar_juego(game)
                    else:
                        root.lower()
                        botones_respuestas[foo1].config(state="disabled")
                        msg = messagebox.askyesno("Respuesta Incorrecta", message="¿Otro equipo desea participar?")
                        if msg:
                            # Opción para volver a participar
                            root.lower()
                            equipos_part.config(text="Seleccionar equipo")
                            def new(foo2):
                                for _ in range(len(boton_equipos)):
                                    if boton_equipos[_]["state"] != "disabled":
                                        boton_equipos[_].config(state="disabled")
                                for y in range(len(botones_respuestas)):
                                    botones_respuestas[y].config(state="normal")
                                botones_respuestas[foo1].config(state="disabled")
                                print(foo2)
                                equipos_part.config(text="")

                                def verify2(foo3):
                                    texto_boton = botones_respuestas[foo3].cget("text")
                                    print(texto_boton)
                                    if texto_boton == respuestas_ocupadas_ordenadas[0]:
                                        # Se asignan los puntos
                                        puntaje_equipos[foo2] += (index_j + 1) * 50
                                        lbl_puntaje_equipos[foo2].config(text=f"{str(puntaje_equipos[foo2])} puntos")
                                        print(puntaje_equipos)
                                        question.destroy()
                                        root.lower()
                                        terminar_juego(game)
                                    else:
                                        for h in range(len(botones_respuestas)):
                                            botones_respuestas[h].config(state="disabled")
                                        root.lower()
                                        messagebox.showinfo("Respuesta Incorrecta",
                                                            message=f"La respuestas correcta es: "
                                                                    f"{respuestas_ocupadas_ordenadas[0]}")
                                        root.lower()
                                        question.destroy()
                                        terminar_juego(game)

                                for a in range(len(botones_respuestas)):
                                    botones_respuestas[a]["command"] = lambda a=a: verify2(a)

                            for q in range(len(boton_equipos)):
                                boton_equipos[q]["command"] = lambda q=q: new(q)
                                boton_equipos[q].config(state="normal")
                            boton_equipos[foo].config(state="disabled")

                        else:
                            messagebox.showinfo("Respuesta Incorrecta", message=f"La respuestas correcta es: "
                                                f"{respuestas_ocupadas_ordenadas[0]}")
                            root.lower()
                            question.destroy()
                            terminar_juego(game)

                # Creación de botones de respuesta
                botones_respuestas = []
                ij = 0
                counter = 0
                for i in range(2):
                    ji = 0
                    for p in range(2):
                        but = Button(question, text=respuestas_ocupadas_revueltas[counter],
                                     command=lambda counter=counter: verify(counter),
                                     fg="white", bg="#060CE9", font=("Dafont", 15, "bold"))
                        botones_respuestas.append(but)
                        but.grid(row=ij + 1, column=ji, columnspan=1, pady=10)
                        ji += 1
                        counter += 1
                    ij += 1
                lenlon1 = []
                for x in botones_respuestas:
                    lenlon1.append(len(x["text"]))
                if max(lista_lon_equipos) < max(lenlon1):
                    center_window(question, 5 * max(lenlon1) + 900, 250+50*len(lista_equipos))

            # Creación de botones de equipos
            equipos_part = Label(question, text="Seleccionar equipo", wraplength=600, bg="#00083D",
                                 fg="white", font=("Dafont", 15, "bold"))
            equipos_part.grid(row=0, column=2, columnspan=1)
            boton_equipos = []  # Botones de equipos de la pestaña equipos
            for m in range(len(lista_equipos)):
                cual_equipo = Button(question, text=f"{lista_equipos[m]}", command=lambda m=m: puntos(m),
                                     fg="#FFD700", bg="#060CE9", font=("Dafont", 15, "bold"))
                boton_equipos.append(cual_equipo)
                cual_equipo.grid(row=m+1, column=2, columnspan=1, padx=10, pady=10)

    label_title = Label(game, text="JEOPARDY QUÍMICO", bg="#00083d", fg="#FFD700", font=("Dafont", 20, "bold"))
    label_title.grid(row=0, column=0, columnspan=6)

    # Variable que guardará los puntos
    lbl_puntaje_equipos = []
    for _ in range(len(lista_equipos)):
        puntaje_equipos.append(0)

    # Creación de categorías y botones de pregunta. k/index_i son las columnas y l/index_j las filas.
    for k in range(0, len(categorias)):
        lbl_categoria = Label(game, text=categorias[k], fg="#FFD700", font=("Dafont", 20, "bold"), bg="#00083d")
        lbl_categoria.grid(row=1, column=k, columnspan=1, pady=5, padx=10)
        preguntas_btn_aux = []
        for l in range(0, categorias_puntos):
            btn = Button(game, text=str((l + 1) * 100), command=lambda k=k, l=l: pregunta(k, l),
                         fg="#FFD700", font=("Dafont", 20, "bold"), bg="#060CE9")
            preguntas_btn_aux.append(btn)
            lbl1 = Label(game, bg="#00083d")
            # lbl1.grid(row=l+2, column=k, columnspan=1, ipadx=100, pady=5)
            btn.grid(row=l+2, column=k, columnspan=1, padx=3)

        preguntas_btn.append(copy(preguntas_btn_aux))

    # Creación de Equipos y Avatares
    for _ in range(0, len(lista_equipos)):
        equipos_escogidos = Label(game, text=str(lista_equipos[_]), bg="#00083d", fg="#FFD700",
                                  font=("Dafont", 20, "bold"))
        lbl_puntos_equipo = Label(game, text="0" + " puntos", bg="#00083d", fg="#FFD700",
                                  font=("Dafont", 20, "bold"))
        lbl_puntaje_equipos.append(lbl_puntos_equipo)
        equipos_escogidos.grid(row=8, column=_, pady=10)
        lbl_puntos_equipo.grid(row=9, column=_)

    # Botón de finalización
    finish_btn = Button(game, text="Finalizar juego", command=terminate, state="disabled", fg="#FFD700",
                        font=("Dafont", 10, "bold"), bg="#B22222")
    desbloq_btn = Button(game, text="Desbloquear botón", command=desbloq, fg="#FFD700", font=("Dafont", 10, "bold"),
                         bg="#060CE9")

    if len(categorias) > len(lista_equipos):
        finish_btn.grid(row=9, column=len(categorias) + 1, columnspan=6)
        desbloq_btn.grid(row=8, column=len(categorias) + 1)
        lon = 0
        for _ in range(len(categorias)):
            if len(categorias) < 12:
                lon += 11
            else:
                lon += len(categorias[_])
        center_window(game, 12*lon+250+len(categorias)*10, 5*50+250)
        for _ in range((len(categorias))+1):
            game.columnconfigure(_, weight=1)
    else:
        finish_btn.grid(row=9, column=len(lista_equipos) + 1, columnspan=6)
        desbloq_btn.grid(row=8, column=len(lista_equipos) + 1)
        lon = 0
        for _ in range(len(lista_equipos)):
            if len(lista_equipos) < 12:
                lon += 11
            else:
                lon += len(lista_equipos[_])
        center_window(game, 26*lon+250, 5*50+250)
        for _ in range((len(lista_equipos))+1):
            game.columnconfigure(_, weight=1)
# endregion


# region Equipos
# Pestaña de Equipos
def botjug():
    root.protocol("WM_DELETE_WINDOW", botx)
    global equipos
    tkinter.messagebox.showinfo(message="Favor de ingresar los nombres de los equipos.")
    Boton_jugar.config(state="disabled")
    equipos = Tk()
    equipos.title("Definición de Equipos")
    equipos.protocol("WM_DELETE_WINDOW", botx)
    equipos.configure(bg="#00083d")
    global lista_equipos
    global lista_equipos_nombre
    global historial_equipos
    global lista_labels_nombre
    global lista_labels_numero
    global cambios
    cambios = 0
    lista_equipos = []
    lista_equipos_nombre = []
    historial_equipos = []
    lista_labels_nombre = []
    lista_labels_numero = []

    # Carga las imágenes de los avatares
    imgs = r'C:/Users/rosil/Documentos/New Catalog/Miscelánea/Escuelas/UNAM/Noveno Semestre/Estancia Corta Noveno/' \
           r'Avatares'
    imgs_list = []  # Imágenes de los avatares
    names_imgs = []  # Nombres de los avatares
    for root1, dirs, files in os.walk(imgs):
        for file1 in files:
            if file1.lower().endswith('.png'):
                img_path = os.path.join(root1, file1).replace('\\', '/')
                imgs_list.append(img_path)
                name_without_extension = os.path.splitext(file1)[0]
                names_imgs.append(name_without_extension)

    # Pestaña de Nombramiento de Equipos
    def agregar():

        def agr_an():
            global lista_equipos
            global lista_equipos_nombre
            global historial_equipos
            global lista_labels_nombre
            global lista_labels_numero
            global cambios
            if inicio_juego.cget("state") == "normal":
                inicio_juego.config(state="disabled")
            qi = len(lista_equipos)
            cambios += 1
            if len(an_entry.get()) > 16:
                messagebox.showinfo(message="Límite de caracteres.")
                root.lower()
            else:
                lista_equipos.append(an_entry.get())
                lista_equipos_nombre.append(lista_equipos[qi-1])
                historial_equipos.append(lista_equipos.copy())
                num_eq = Label(equipos, text=qi+1, bg="#00083d", fg="#FFD700", font=("Dafont", 15, "bold"))
                nom_eq = Label(equipos, text=str(lista_equipos[len(lista_equipos)-1]), bg="#00083d", fg="#FFD700",
                               font=("Dafont", 15, "bold"))
                lista_labels_nombre.append(nom_eq)
                lista_labels_numero.append(num_eq)
                an_del.config(text="Cerrar")
                num_eq.grid(row=qi+1, column=1, columnspan=1, padx=15, pady=20)
                nom_eq.grid(row=qi+1, column=2, columnspan=1, padx=10, pady=20)
                an_entry.delete(0, tkinter.END)

        def an_des():
            agregar_nombre.destroy()
            agr_eq.config(state="normal")
            elim_eq.config(state="normal")
            mod_eq.config(state="normal")
            if len(lista_equipos) < 1:
                inicio_juego.config(state="disabled")
            else:
                inicio_juego.config(state="normal")

        agregar_nombre = Tk()
        agregar_nombre.title("Nombrar equipo")
        agregar_nombre.protocol("WM_DELETE_WINDOW", botx)
        agregar_nombre.configure(bg="#00083d")
        agr_eq.config(state="disabled")
        elim_eq.config(state="disabled")
        mod_eq.config(state="disabled")
        inicio_juego.config(state="disabled")
        an_label = Label(agregar_nombre, text="Ingresar nombre del equipo", fg="white", bg="#00083d",
                         font=("Dafont", 15, "bold"))
        an_entry = Entry(agregar_nombre, font=("Dafont", 15, "bold"), width=25, justify="center")
        an_button = Button(agregar_nombre, text="Aceptar", command=agr_an, bg="#006400", fg="#FFD700",
                           font=("Dafont", 15, "bold"))
        an_del = Button(agregar_nombre, command=an_des, bg="#B22222", fg="#FFD700", font=("Dafont", 15, "bold"))
        if len(lista_equipos) != 0:
            an_del.config(text="Cerrar")
        else:
            an_del.config(text="Cancelar")
        an_label.grid(row=0, column=0, columnspan=1, pady=5)
        an_entry.grid(row=1, column=0, columnspan=1, pady=10)
        an_button.grid(row=2, column=0, columnspan=1, pady=5)
        an_del.grid(row=3, column=0, columnspan=1, pady=5)
        center_window(agregar_nombre, 400, 200)
        agregar_nombre.columnconfigure(0, weight=1)

    # Pestaña de Modificación de Equipos
    def mod_eq():
        global lista_equipos
        if len(lista_equipos) < 1:
            try:
                messagebox.showinfo(message="Favor de agregar equipos primero")
                root.lower()
            except tkinter.TclError:
                return None
        else:
            modificar = Tk()
            modificar.title("Modificar el nombre de un equipo")
            modificar.protocol("WM_DELETE_WINDOW", botx)
            modificar.configure(bg="#00083d")
            agr_eq.config(state="disabled")
            elim_eq.config(state="disabled")
            mod_eq.config(state="disabled")
            inicio_juego.config(state="disabled")

            def mod_des():
                modificar.destroy()
                agr_eq.config(state="normal")
                elim_eq.config(state="normal")
                mod_eq.config(state="normal")
                inicio_juego.config(state="normal")
                root.lower()

            def mod_eq_acept():
                global lista_labels_nombre
                global historial_equipos
                global lista_equipos
                global cambios
                cambios += 1
                liseqn = []
                try:
                    num_eq_mod = int(modificar_ent1.get())
                except ValueError:
                    messagebox.showinfo(message="Favor de ingresar un número")
                    root.lower()
                try:
                    if num_eq_mod > len(lista_equipos):
                        messagebox.showinfo(message="Favor de escribir un número de equipo existente")
                        root.lower()
                    else:
                        nom_eq_mod = str(modificar_ent2.get())
                        if len(nom_eq_mod) > 16:
                            messagebox.showinfo(message="Límite de caracteres")
                            root.lower()
                        else:
                            lbl_modificada = Label(equipos, text=nom_eq_mod)
                            lista_labels_nombre[num_eq_mod-1].grid_forget()
                            lista_labels_nombre[num_eq_mod-1] = lbl_modificada
                            lista_equipos[num_eq_mod-1] = nom_eq_mod
                            liseqn = copy(lista_equipos)
                            historial_equipos.append(liseqn)
                            lista_labels_nombre[num_eq_mod-1].configure(fg="#FFD700", font=("Dafont", 15, "bold"),
                                                                    bg="#00083d")
                            lista_labels_nombre[num_eq_mod-1].grid(row=num_eq_mod, column=2, columnspan=1)
                            modificar.destroy()
                            agr_eq.config(state="normal")
                            elim_eq.config(state="normal")
                            mod_eq.config(state="normal")
                            inicio_juego.config(state="normal")
                            root.lower()
                except UnboundLocalError:
                    return None

            modificar_lbl1 = Label(modificar, text="Número de equipo", fg="white", bg="#00083d",
                                   font=("Dafont", 15, "bold"))
            modificar_lbl2 = Label(modificar, text="Nuevo nombre", font=("Dafont", 15, "bold"),
                                   fg="white", bg="#00083d")
            modificar_ent1 = Entry(modificar, justify="center", width=3, font=("Dafont", 15, "bold"))
            modificar_ent2 = Entry(modificar, justify="center", font=("Dafont", 15, "bold"), width=25)
            modificar_btn = Button(modificar, command=mod_eq_acept, text="Aceptar", font=("Dafont", 15, "bold"),
                                   bg="#006400", fg="#FFD700")
            modif_dst = Button(modificar, command=mod_des, text="Cancelar", font=("Dafont", 15, "bold"),
                               bg="#B22222", fg="#FFD700")
            modificar_lbl1.grid(row=0, column=0, columnspan=1, pady=5)
            modificar_lbl2.grid(row=0, column=1, columnspan=1, pady=5)
            modificar_ent1.grid(row=1, column=0, columnspan=1, pady=10)
            modificar_ent2.grid(row=1, column=1, columnspan=1, pady=15)
            modificar_btn.grid(row=2, column=1, columnspan=1, pady=5)
            modif_dst.grid(row=3, column=1, columnspan=1, pady=5)
            center_window(modificar, 520, 210)
            modificar.columnconfigure(0, weight=1)
            modificar.columnconfigure(1, weight=1)
            root.lower()

    # Pestaña de Eliminación de Equipos
    def elim_eq():
        global lista_equipos
        if len(lista_equipos) < 1:
            try:
                messagebox.showinfo(message="Favor de agregar equipos primero")
                root.lower()
            except tkinter.TclError:
                return None
        else:
            elim = Tk()
            elim.title("Eliminar un equipo")
            elim.protocol("WM_DELETE_WINDOW", botx)
            elim.configure(bg="#00083d")
            agr_eq.config(state="disabled")
            elim_eq.config(state="disabled")
            mod_eq.config(state="disabled")
            inicio_juego.config(state="disabled")
            eliminar_lbl1 = Label(elim, text="Número de equipo por eliminar", fg="white", bg="#00083d",
                                  font=("Dafont", 15, "bold"))
            eliminar_ent1 = Entry(elim, font=("Dafont", 15, "bold"), width=3, justify="center")

            def elim_des():
                elim.destroy()
                agr_eq.config(state="normal")
                elim_eq.config(state="normal")
                mod_eq.config(state="normal")
                inicio_juego.config(state="normal")
                root.lower()

            def elim_btn():
                global lista_labels_nombre
                global lista_labels_numero
                global historial_equipos
                global lista_equipos
                global cambios
                cambios += 1
                try:
                    num_eq_elim = int(eliminar_ent1.get())
                except ValueError:
                    messagebox.showinfo(message="Favor de ingresar un número")
                    root.lower()
                try:
                    if num_eq_elim > len(lista_equipos):
                        messagebox.showinfo(message="Favor de escribir un número de equipo existente")
                        root.lower()
                    for _ in range(0, len(lista_equipos)):
                        lista_labels_nombre[_].grid_forget()
                        lista_labels_numero[_].grid_forget()
                    del lista_equipos[num_eq_elim-1]
                    del lista_labels_nombre[num_eq_elim-1]
                    del lista_labels_numero[num_eq_elim-1]
                    liseqe = []
                    liseqe = copy(lista_equipos)
                    historial_equipos.append(liseqe)

                    for _ in range(0, len(lista_equipos)):
                        lista_labels_numero[_].config(text=str(_+1))

                    for _ in range(0, len(lista_equipos)):
                        lista_labels_nombre[_].grid(row=_+1, column=2, columnspan=1, padx=15, pady=20)
                        lista_labels_numero[_].grid(row=_+1, column=1, columnspan=1, padx=10, pady=20)
                    elim.destroy()
                    agr_eq.config(state="normal")
                    elim_eq.config(state="normal")
                    mod_eq.config(state="normal")
                    if len(lista_equipos) < 1:
                        inicio_juego.config(state="disabled")
                    else:
                        inicio_juego.config(state="normal")
                    root.lower()
                except UnboundLocalError:
                    return None

            eliminar_btn = Button(elim, command=elim_btn, text="Aceptar", bg="#006400", fg="#FFD700",
                                  font=("Dafont", 15, "bold"))
            elim_dest_btn = Button(elim, command=elim_des, text="Cancelar",
                                   bg="#B22222", fg="#FFD700", font=("Dafont", 15, "bold"))
            eliminar_lbl1.grid(row=0, column=0, columnspan=1, pady=5)
            eliminar_ent1.grid(row=1, column=0, columnspan=1, pady=10)
            eliminar_btn.grid(row=2, column=0, columnspan=2, pady=5)
            elim_dest_btn.grid(row=3, column=0, columnspan=2, pady=5)
            center_window(elim, 350, 200)
            elim.columnconfigure(0, weight=1)
            root.lower()

    agr_eq = Button(equipos, text="Agregar equipo", command=agregar, bg="#006400", fg="#FFD700",
                    font=("Dafont", 15, "bold"))
    elim_eq = Button(equipos, text="Eliminar equipo", command=elim_eq, bg="#B22222", fg="#FFD700",
                     font=("Dafont", 15, "bold"))
    mod_eq = Button(equipos, text="Modificar equipo", command=mod_eq, bg="#8B4513", fg="#FFD700",
                    font=("Dafont", 15, "bold"))
    inicio_juego = Button(equipos, text="Iniciar juego", command=jeopardy, bg="#060CE9", fg="#FFD700",
                          font=("Dafont", 15, "bold"), state="disabled")
    label_col1 = Label(equipos, text="Número", bg="#00083d", fg="#FFD700", font=("Dafont", 15, "bold"))
    label_col2 = Label(equipos, text="Equipo", bg="#00083d", fg="#FFD700", font=("Dafont", 15, "bold"))

    agr_eq.grid(row=1, column=0, columnspan=1, padx=15, pady=20)
    elim_eq.grid(row=2, column=0, columnspan=1, padx=15, pady=20)
    mod_eq.grid(row=3, column=0, columnspan=1, padx=15, pady=20)
    inicio_juego.grid(row=4, column=0, columnspan=1, padx=15, pady=20)
    label_col1.grid(row=0, column=1, columnspan=1, padx=15, pady=20)
    label_col2.grid(row=0, column=2, columnspan=1, padx=15, pady=20)
    center_window(equipos, 630, 800)
# endregion


# region Root
# Pestaña de Instrucciones
def botinstr():
    instrucciones = tkinter.Tk()
    instrucciones.title("Instrucciones")
    instrucciones.configure(bg="#00083d")
    labelinstr = Label(instrucciones, text=txt_instr, font=("Dafont", 15, "bold"), wraplength=600, fg="white",
                       bg="#00083d")

    def instrdest():
        instrucciones.destroy()

    botinstr_regresar = tkinter.Button(instrucciones, text="Cerrar", font=("Dafont", 15, "bold"),
                                       command=instrdest, bg="#060CE9", fg="#FFD700")
    botinstr_regresar.grid(row=1, column=0, columnspan=1, padx=5)
    labelinstr.grid(row=0, column=0, padx=5, pady=10)
    botinstr_regresar.grid(row=1, column=0)
    instrucciones.columnconfigure(0, weight=1)
    center_window(instrucciones, 700, 430)


# Pestaña Infografías
def info():
    win_info = Tk()

    def info_destroy():
        win_info.destroy()

    win_info.title("Infografías")
    win_info.configure(bg="#00083d")
    for _ in range(len(categorias)):
        win_info_lbl1 = Label(win_info, text=f"Infografía {categorias[_]}: (Link)", fg="white",
                              font=("Dafont", 16, "bold"), bg="#00083d")  # El link debe de estar en color verde;
        # se debe escribir como string. Las strings de los hipervínculos deben estar en un array descrito o en esta
        # pestaña o en las declaraciones debajo de los import y globales pero antes de las funciones.
        win_info_lbl1.grid(row=_, column=0, columnspan=1, pady=5)
    win_info_btn = Button(win_info, text="Cerrar", command=info_destroy, bg="#060CE9", fg="#FFD700",
                          font=("Dafont", 16, "bold"), padx=10)
    win_info_btn.grid(row=len(categorias), column=0, columnspan=1, pady=10)
    win_info.columnconfigure(0, weight=1)
    center_window(win_info, 600, 300)


def cat():
    categ = Tk()
    categ.title("Puntajes")
    categ.configure(bg="#00083d")
    root.protocol("WM_DELETE_WINDOW", botx)
    categ.protocol("WM_DELETE_WINDOW", botx)
    Boton_jugar.config(state="disabled")
    Boton_num.config(state="disabled")

    def canc():
        categ.destroy()
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        Boton_jugar.config(state="normal")
        Boton_num.config(state="normal")

    def camb_num_cat():
        global categorias_puntos
        try:
            cat_nuv = int(entry_cat.get())
            if (cat_nuv > 5) or (cat_nuv == 0):
                messagebox.showinfo(message="Favor de ingresar un número válido")
                root.lower()
            else:
                categorias_puntos = cat_nuv
                categ.destroy()
                root.protocol("WM_DELETE_WINDOW", root.destroy)
                Boton_jugar.config(state="normal")
                Boton_num.config(state="normal")
        except ValueError:
            messagebox.showinfo(message="Favor de ingresar un número")
            root.lower()

    label_cat = Label(categ, text="Hay cinco puntajes por default: 100, 200, 300, 400 y 500. En esta pestaña"
                                  " se pueden reducir a cuatro o menos introduciendo un número en la casilla. "
                                  "Si en el documento de "
                                  "Excel hay más de cinco categorías, favor de cambiar directamente el código",
                      wraplength=600, justify="center", font=("Dafont", 20, "bold"), fg="white", bg="#00083d")
    entry_cat = Entry(categ, width=2, justify="center", font=("Dafont", 20, "bold"))
    but_camb = Button(categ, text="Aceptar", command=camb_num_cat, font=("Dafont", 20, "bold"), fg="#FFD700",
                      bg="#006400")
    but_reg_can = Button(categ, text="Cancelar", command=canc, font=("Dafont", 20, "bold"), fg="#FFD700",
                         bg="#B22222")

    label_cat.grid(row=0, column=0, columnspan=1, pady=10)
    entry_cat.grid(row=1, column=0, columnspan=1, pady=10)
    but_camb.grid(row=2, column=0, columnspan=1, pady=10)
    but_reg_can.grid(row=3, column=0, columnspan=1, pady=10)

    categ.columnconfigure(0, weight=1)
    center_window(categ, 600, 435)


# Pestaña de Inicio
root = tkinter.Tk()
root.title("Inicio")
root.configure(bg="#00083d")
Boton_jugar = Button(root, text="Jugar", font=("Dafont", 20, "bold"), command=botjug, fg="#FFD700", bg="#060CE9")
Boton_instrucciones = Button(root, text="Instrucciones", font=("Dafont", 20, "bold"), command=botinstr, fg="#FFD700",
                             bg="#060CE9")
Boton_info = Button(root, text="Infografías", font=("Dafont", 20, "bold"), command=info, fg="#FFD700", bg="#060CE9")
Boton_num = Button(root, text="Dificultad", font=("Dafont", 20, "bold"), command=cat,
                   fg="#FFD700", bg="#060CE9")
Boton_jugar.grid(row=0, column=0, columnspan=1, pady=5, padx=5)
Boton_instrucciones.grid(row=1, column=0, columnspan=1, pady=5, padx=10)
Boton_info.grid(row=2, column=0, columnspan=1, pady=5, padx=10)
Boton_num.grid(row=3, column=0, columnspan=1, pady=5, padx=10)
center_window(root, 225, 265)

root.mainloop()
# endregion
# endregion
