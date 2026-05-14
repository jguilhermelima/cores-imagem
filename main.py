from PIL import Image, ImageTk, UnidentifiedImageError
from matplotlib import image
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from collections import Counter

WIDTH, HEIGHT = 1280,720
CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 690

def get_hex_color(rgbs):
    hex_cor = []
    for rgb in rgbs:
        url = f"https://www.thecolorapi.com/id?rgb={rgb}"
        response = requests.get(url=url)
        response.raise_for_status()
        hexadecimal = response.json()
        hex_cor.append(hexadecimal["hex"]["value"])

    exibir_cores(hex_cor)

def get_rgb_color():
    imagem = image.imread("imagem/imagem.jpg")
    height,width = imagem.shape[:2]
    lista_rgb = []
    rgbs = []
    for x in range(0, height):
        for y in range(0, width):
            pixel = imagem[x,y]
            rgb = (int(pixel[0]),int(pixel[1]),int(pixel[2]))
            lista_rgb.append(rgb)

    mais_frequente_rgb = Counter(lista_rgb[0::10]).most_common(10)
    for rgb in mais_frequente_rgb:
        rgbs.append(rgb[0])

    get_hex_color(rgbs)

def exibir_cores(hexadecimal_cores):
    hex_cores = hexadecimal_cores
    dot_posicao = 5
    texto_posicao = 95
    canvas.delete("dots")

    for hex_cor in hex_cores:
        dot = canvas.create_oval(70, 70, 105, 105, fill=f"{hex_cor}", outline=f"{hex_cor}", tags="dots")
        canvas.move(dot, 950, dot_posicao)
        dot_texto = canvas.create_text(1120, texto_posicao, text=f"{hex_cor}", font=("Ariel", 20, "italic"), tags="dots")
        dot_posicao += 50
        texto_posicao += 50


def upload_image():
    try:
        img_path = askopenfilename()
        im = Image.open(img_path)
        img_width, img_height = im.size

        if img_width > 1000 or img_height > 1280:
            while img_width > 1000 or img_height > 1280:
                img_width *= .99
                img_height *= .99

            im = im.resize((int(img_width), int(img_height)))

        im.save("imagem/imagem.jpg")

        img =  ImageTk.PhotoImage(im)
        canvas.img = img
        canvas.itemconfig(imagem, image=img)
    except UnidentifiedImageError:
        messagebox.showinfo("Erro Upload!",
                            "Imagem não enviada. Por favor selecione uma mensagem.")

window = tk.Tk()
window.title("Pegar Paleta de Cores")
window.config(bg="gray")
window.geometry('%sx%s' % (WIDTH,HEIGHT))

canvas = tk.Canvas(window,width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
imagem = canvas.create_image(500, 300,anchor=tk.CENTER)
canvas.grid(row=1, column=0, columnspan=15)

botao_upload = tk.Button(window,text="Selecionar Imagem",width=15, command=upload_image, bg="gray", font=("Ariel", 12, "bold"))
botao_upload.grid(row=0, column=0)

botao_color = tk.Button(window,text="Pegar cor",width=15, command=get_rgb_color, bg="gray", font=("Ariel", 12, "bold"))
botao_color.grid(row=0,column=1)

window.mainloop()



