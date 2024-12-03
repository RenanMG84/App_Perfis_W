import math
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import LabelFrame, Combobox, Button
from pylatex import Document, Section, Subsection, Math, NoEscape, Center

class Principal(Tk):
    def __init__(self):
        super().__init__()
        self.title("Cálculo de Perfis Laminados - Ver. 1.0")
        #self.geometry("+600+100")
        self.resizable(FALSE, FALSE)
        #Variáveis globais (do aço e dimensões do perfil)
        self.lx = 0
        self.ly = 0
        self.lz = 0
        self.lb = 0
        self.e = 0

        #Organização dos frames--------------------------------------
        #as instâncias dos frames serão criadas e posicionadas aqui !!
        self.frame_perfil = Frame_Perfil(self)
        self.frame_perfil.grid(row = 0, column = 0, columnspan=2 )
        self.solicitacoes = Solicitacoes(self)
        self.solicitacoes.grid(row = 0 , column=2, pady= 5, padx = 10, sticky= 'w')
        self.comp_barras = Comp_Barras(self)
        self.comp_barras.grid(row = 1, column= 2, sticky='w', pady = 5, padx = 10)
        self.frame_cb = Frame_Cb(self)
        self.frame_cb.grid(row = 2, column= 2, sticky='w', pady = 5, padx = 10)
        self.prop_aco = Aco(self)
        self.prop_aco.grid(row = 1, column= 0, padx = 10)
        self.frame_resul = Frame_Resultados(self)
        self.frame_resul.grid(row = 3 , column= 2, pady = 5, padx = 10, sticky = 'w')
        self.frame_botoes = Botoes(self)
        self.frame_botoes.grid(row = 2, column= 0, rowspan= 3, columnspan= 2,pady = 30,  sticky='nsew')

    
    def calcular(self):
        try:
            #Limpa as entry de resultados no Frame Resultados
            self.frame_resul.entry_ntrd.delete(0, END)
            self.frame_resul.entry_ncrd.delete(0, END)
            self.frame_resul.entry_vxrd.delete(0, END)
            self.frame_resul.entry_vyrd.delete(0, END)
            self.frame_resul.entry_myrd.delete(0, END)
            self.frame_resul.entry_mxrd.delete(0, END)

            #passa os valores dos entrys do aço para as variáveis globais do frame Principal
            self.e = float(self.prop_aco.entry_e.get())
            self.g = float(self.prop_aco.entry_g.get())
            self.fy = float(self.prop_aco.entry_fy.get())
            self.fu = float(self.prop_aco.entry_fu.get())

            #passa os valores dos entrys do comprimento da barra para as variáveis globais do frame principal
            self.lx = float(self.comp_barras.entry_lx.get())
            self.ly = float(self.comp_barras.entry_ly.get())
            self.lz = float(self.comp_barras.entry_lz.get())
            self.lb = float(self.comp_barras.entry_lb.get())

            #pega o valor de cb
            self.cb = float(self.frame_cb.entry_cb.get())

            #cria objetos para calculo e insere os resultados nos respectivos entrys
            #Tração
            self.calc_tracao = Tracao(self.frame_perfil.area, self.fy)
            self.frame_resul.entry_ntrd.insert(1,f"{self.calc_tracao.ntrd:.2f}")
            if float(self.solicitacoes.entry_ntsd.get()) / float(self.frame_resul.entry_ntrd.get()) < 1.0:
                self.frame_resul.entry_ntrd.configure(fg= 'green')
            else:
                self.frame_resul.entry_ntrd.configure(fg= 'red')


            #Compressão
            self.calc_compressao = Compressao(self.e, self.fy, self.frame_perfil.area, self.frame_perfil.dlinha, self.frame_perfil.tw, self.frame_perfil.bf, self.frame_perfil.tf,
                                            self.frame_perfil.ix, self.lx, self.frame_perfil.iy, self.ly, self.lz, self.frame_perfil.it, self.g, self.frame_perfil.cw, self.frame_perfil.rx,
                                                self.frame_perfil.ry, 0, 0)
            self.frame_resul.entry_ncrd.insert(1,f"{self.calc_compressao.ncrd:.2f}")
            if float(self.solicitacoes.entry_ncsd.get()) / float(self.frame_resul.entry_ncrd.get()) < 1.0:
                self.frame_resul.entry_ncrd.configure(fg= 'green')
            else:
                self.frame_resul.entry_ncrd.configure(fg= 'red')

            #Momento em X
            self.calc_mom_x = Momento_X(self.e, self.g, self.fy, self.frame_perfil.zx, self.frame_perfil.wx, self.frame_perfil.it, self.frame_perfil.bf, self.frame_perfil.tf,
                                        self.frame_perfil.dlinha, self.frame_perfil.tw, self.lb, self.frame_perfil.ry, self.cb, self.frame_perfil.iy, self.frame_perfil.cw)
            self.frame_resul.entry_mxrd.insert(1,f"{self.calc_mom_x.mxrd:.2f}")
            if float(self.solicitacoes.entry_mxsd.get()) / float(self.frame_resul.entry_mxrd.get()) < 1.0:
                self.frame_resul.entry_mxrd.configure(fg= 'green')
            else:
                self.frame_resul.entry_mxrd.configure(fg= 'red')

            #Momento em Y
            self.calc_mom_y = Momento_Y(self.e, self.g, self.fy, self.frame_perfil.zy, self.frame_perfil.wy, self.frame_perfil.it, self.frame_perfil.bf, self.frame_perfil.tf,
                                        self.frame_perfil.dlinha, self.frame_perfil.tw, self.lb, self.frame_perfil.ry, self.cb, self.frame_perfil.iy, self.frame_perfil.cw)
            self.frame_resul.entry_myrd.insert(1,f"{self.calc_mom_y.myrd:.2f}")
            if float(self.solicitacoes.entry_mysd.get()) / float(self.frame_resul.entry_myrd.get()) < 1.0:
                self.frame_resul.entry_myrd.configure(fg= 'green')
            else:
                self.frame_resul.entry_myrd.configure(fg= 'red')

            #Cortante em X 
            self.calc_cort_x = Cortante_X(self.frame_perfil.dlinha, self.frame_perfil.tw, self.fy,self.e)
            self.frame_resul.entry_vxrd.insert(1,f"{self.calc_cort_x.vrd:.2f}")
            if float(self.solicitacoes.entry_vxsd.get()) / float(self.frame_resul.entry_vxrd.get()) < 1.0:
                self.frame_resul.entry_vxrd.configure(fg= 'green')
            else:
                self.frame_resul.entry_vxrd.configure(fg= 'red')

            #Cortante em Y
            self.calc_cort_y = Cortante_Y(self.frame_perfil.bf, self.frame_perfil.tf, self.fy,self.e, self.frame_perfil.tw)
            self.frame_resul.entry_vyrd.insert(1,f"{self.calc_cort_y.vrd:.2f}")
            if float(self.solicitacoes.entry_vysd.get()) / float(self.frame_resul.entry_vyrd.get()) < 1.0:
                self.frame_resul.entry_vyrd.configure(fg= 'green')
            else:
                self.frame_resul.entry_vyrd.configure(fg= 'red')

        except ValueError:
            messagebox.showerror("Erro de Valor", "Certifique-se de que todos os campos estão preenchidos corretamente com valores numéricos.")
        except AttributeError as e:
            messagebox.showerror("Erro de Atributo", f"Erro encontrado: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
   

    def apagar(self):
        #apaga as entradas
        self.frame_resul.entry_ntrd.delete(0, END)
        self.frame_resul.entry_ncrd.delete(0, END)
        self.frame_resul.entry_vxrd.delete(0, END)
        self.frame_resul.entry_vyrd.delete(0, END)
        self.frame_resul.entry_mxrd.delete(0, END)
        self.frame_resul.entry_myrd.delete(0, END)

    def memorial(self):
        self.gerar_mem = Gerar_pdf(self.frame_perfil, self.calc_tracao, self.calc_compressao, self.calc_cort_x, self.calc_cort_y, self.calc_mom_x, self.calc_mom_y)   
        self.gerar_mem.gerar()

class Solicitacoes(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.labelframe = LabelFrame(self, text= 'Solicitações de Cálculo (kN e kN*cm)', width= 250, height = 100)
        self.labelframe.grid(row= 0 , column=  0)
        self.labelframe.grid_propagate(False)  

        self.label_ncsd = Label(self.labelframe, text= 'Nc,Sd')
        self.label_ncsd.grid(row=0, column= 0, pady = (5,3), padx= (10,0))
        self.entry_ncsd = Entry(self.labelframe, width = 10)
        self.entry_ncsd.insert(0,"0")
        self.entry_ncsd.grid(row = 0, column= 1, padx= 3, pady = (5,0), sticky='w')

        self.label_ntsd = Label(self.labelframe, text= 'Nt,Sd')
        self.label_ntsd.grid(row=1, column= 0, pady = 3, padx= (10,0))
        self.entry_ntsd = Entry(self.labelframe, width = 10)
        self.entry_ntsd.insert(0,"0")
        self.entry_ntsd.grid(row = 1, column= 1, padx= 3, sticky='w')

        self.label_mxsd = Label(self.labelframe, text= 'Mx,Sd')
        self.label_mxsd.grid(row=2, column= 0, pady = 3, padx= (10,0))
        self.entry_mxsd = Entry(self.labelframe, width = 10)
        self.entry_mxsd.insert(0,"0")
        self.entry_mxsd.grid(row = 2, column= 1, pady = 3,padx= 3, sticky='w')

        self.label_vxsd = Label(self.labelframe, text= 'Vx,Sd')
        self.label_vxsd.grid(row=0, column= 2, pady = (5,3))
        self.entry_vxsd = Entry(self.labelframe, width = 10)
        self.entry_vxsd.insert(0,"0")
        self.entry_vxsd.grid(row = 0, column= 3, pady = (5,0), sticky='w')

        self.label_vysd = Label(self.labelframe, text= 'Vy,Sd')
        self.label_vysd.grid(row=1, column= 2, pady = 3)
        self.entry_vysd = Entry(self.labelframe, width = 10)
        self.entry_vysd.insert(0,"0")
        self.entry_vysd.grid(row = 1, column= 3, sticky='w')

        self.label_mysd = Label(self.labelframe, text= 'My,Sd')
        self.label_mysd.grid(row=2, column= 2, padx= 5)
        self.entry_mysd = Entry(self.labelframe, width = 10)
        self.entry_mysd.insert(0,"0")
        self.entry_mysd.grid(row = 2, column= 3, sticky='w')

class Aco(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.labelframe = LabelFrame(self, text= 'Propriedades do aço (MPa)')
        self.labelframe.grid(row= 0 , column=  0)

        self.label_fy = Label(self.labelframe, text= 'fy')
        self.label_fy.grid(row=0, column= 0, padx= (10,0))
        self.entry_fy = Entry(self.labelframe, width=7)
        self.entry_fy.grid(row = 0, column= 1, padx=5)
        self.entry_fy.insert(0,"345")

        self.label_fu = Label(self.labelframe, text= 'fu')
        self.label_fu.grid(row=1, column= 0, padx= (10,0))
        self.entry_fu = Entry(self.labelframe, width=7)
        self.entry_fu.grid(row = 1, column= 1, padx=5)
        self.entry_fu.insert(0,"450")

        self.label_e = Label(self.labelframe, text= 'E')
        self.label_e.grid(row=0, column= 2, padx= (10,0))
        self.entry_e = Entry(self.labelframe, width= 9)
        self.entry_e.grid(row = 0, column= 3, padx= 5, pady = 5)
        self.entry_e.insert(0,"200000")

        self.label_g = Label(self.labelframe, text= 'G')
        self.label_g.grid(row=1, column= 2, padx= (10,0))
        self.entry_g = Entry(self.labelframe, width= 9)
        self.entry_g.grid(row = 1, column= 3, padx= 5, pady = 5)
        self.entry_g.insert(0,"77000")

class Frame_Cb(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.labelframe = LabelFrame(self, text= 'Coef. Cb', width= 250, height = 50)
        self.labelframe.grid_propagate(False) 
        self.labelframe.grid(row= 0 , column=  0)

        self.label_cb = Label(self.labelframe, text= 'Cb')
        self.label_cb.grid(row=0, column= 0, padx= (20,0))
        self.entry_cb = Entry(self.labelframe, width= 5)
        self.entry_cb.grid(row = 0, column= 1, padx= 3, pady = 5)
        self.entry_cb.insert(0,"1")

        """
        self.label_ct = Label(self.labelframe, text= 'Ct')
        self.label_ct.grid(row=0, column= 2, padx= (20,0))
        self.entry_ct = Entry(self.labelframe, width= 9)
        self.entry_ct.grid(row = 0, column= 3, padx= 3, pady = 5)
        self.entry_ct.insert(0,"1")
        """

class Botoes(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master  # Guarda a instância de Principal

        self.frame = Frame(self)
        self.frame.grid(row=0, column=0, sticky='nsew')

        # Configura a expansão das colunas e linhas para centralizar os botões
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.btn_calc = Button(self.frame, text='Calcular', command=self.master.calcular)
        self.btn_calc.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.btn_apagar = Button(self.frame, text='Apagar', command=self.master.apagar)
        self.btn_apagar.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        self.btn_memorial = Button(self.frame, text='Gerar Memorial', command=self.master.memorial)
        self.btn_memorial.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

class Comp_Barras(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.labelframe = LabelFrame(self, text= 'Comprimentos das barras (cm)', width= 250, height = 80)
        self.labelframe.grid(row= 0 , column=  0)
        self.labelframe.grid_propagate(False)  

        self.label_lx = Label(self.labelframe, text= 'Lx')
        self.label_lx.grid(row=0, column= 0, padx= (20,0))
        self.entry_lx = Entry(self.labelframe, width = 10)
        self.entry_lx.insert(0, "300")
        self.entry_lx.grid(row = 0, column= 1, pady= 3, padx= 3)

        self.label_ly = Label(self.labelframe, text= 'Ly')
        self.label_ly.grid(row=1, column= 0, padx= (20,0))
        self.entry_ly = Entry(self.labelframe, width = 10)
        self.entry_ly.insert(0, "300")
        self.entry_ly.grid(row = 1, column= 1, pady = 3)

        self.label_lz = Label(self.labelframe, text= 'Lz')
        self.label_lz.grid(row = 0, column= 2, padx = (30,3))
        self.entry_lz = Entry(self.labelframe, width = 10)
        self.entry_lz.insert(0, "300")
        self.entry_lz.grid(row = 0, column= 3, pady = 3)

        self.label_lb = Label(self.labelframe, text= 'Lb')
        self.label_lb.grid(row = 1, column= 2, padx = (30,3))
        self.entry_lb = Entry(self.labelframe, width = 10)
        self.entry_lb.insert(0, "300")
        self.entry_lb.grid(row = 1, column= 3, pady = 3)

class Frame_Perfil(Frame):
    def __init__(self, master = None,  frame_height=400, frame_width=400):
        super().__init__(master, height = frame_height, width=frame_width)
        self.pack_propagate(False)  # Prevent frame from adjusting to its contents
        self.columnconfigure(0,weight= 1)
        self.columnconfigure(1,weight= 1)
        self.peso = 13.0
        self.d = 148
        self.bf = 100
        self.tw = 4.3
        self.tf = 4.9
        self.h = 138
        self.dlinha = 118
        self.area = 16.6
        self.ix = 635
        self.wx = 85.8
        self.rx = 6.18
        self.zx = 96.4
        self.iy = 82
        self.wy = 16.4
        self.ry = 2.22
        self.zy = 25.50
        self.it = 1.72
        self.cw = 4181

        # Cria os perfis Gerdau
        self.perfis = [                 #peso,  d,  bf,  tw,  tf,  h,   d',  area, ix,  wx,   rx,   zx,   iy, wy,   ry,   zy,    it,   cw
            PerfilGerdau("W 150 x 13,0", 13.0, 148, 100, 4.3, 4.9, 138,	118, 16.6, 635, 85.8, 6.18, 96.4, 82, 16.4, 2.22, 25.50, 1.72, 4181),
            PerfilGerdau("W 150 x 18,0", 18.0, 153,	102, 5.8, 7.1, 139,	119, 23.4, 939, 122.8, 6.34, 139.4, 126, 24.7, 2.32, 38.50, 4.34, 6683),
            PerfilGerdau("W 150 x 22.5(H)",22.5,152, 152, 5.8, 6.6, 139, 119, 29.0,	1229, 161.7, 6.51, 179.6, 387, 50.9, 3.65, 77.90, 4.75,	20417),
            PerfilGerdau('W 150 x 24.0', 24.0, 160, 102	, 6.6, 10.3, 139, 115, 31.5, 1384, 173.0, 6.63,	197.6, 183, 35.9, 2.41, 55.80, 11.08, 10206),
            PerfilGerdau('W 150 x 29.8(H)', 29.8, 157, 153, 6.6, 9.3, 138, 118, 38.5, 1739, 221.5, 6.72, 247.5,	556, 72.6, 3.80, 110.80, 10.95,	30277),
            PerfilGerdau('W 150 x 37.1(H)', 37.1, 162, 154, 8.1, 11.6, 139,	119, 47.8, 2244, 277.0,	6.85, 313.5, 707, 91.8,	3.84, 140.40, 20.58, 39930),
            PerfilGerdau('W 200 x 15.0', 15.0, 200,	100, 4.3, 5.2, 190,	170, 19.4, 1305, 130.5,	8.20, 147.9, 87, 17.4, 2.12, 27.30,	2.05, 8222),
            PerfilGerdau('W 200 x 19.3', 19.3, 203,	102, 5.8, 6.5, 190,	170, 25.1, 1686, 166.1, 8.19, 190.6, 116, 22.7, 2.14, 35.90, 4.02, 11098),
            PerfilGerdau('W 200 x 22.5', 22.5, 206,	102, 6.2, 8.0, 190,	170, 29.0, 2029, 197.0,	8.37, 225.5, 142, 27.9,	2.22, 43.90, 6.18, 13868),
            PerfilGerdau('W 200 x 26.6', 26.6, 207,	133, 5.8, 8.4, 190,	170, 34.2, 2611, 252.3, 8.73, 282.3, 330, 49.6,	3.10, 76.30, 7.65, 32477),
            PerfilGerdau('W 200 x 31.3', 31.3, 210, 134, 6.4, 10.2, 190, 170, 40.3, 3168, 301.7, 8.86, 338.6, 410, 61.2, 3.19, 94.00, 12.59, 40822),
            PerfilGerdau('W 200 x 35.9(H)', 35.9, 201, 165, 6.2, 10.2, 181, 161, 45.7, 3437, 342.0, 8.67, 379.2, 764, 92.6, 4.09, 141.00, 14.51, 69502),
            PerfilGerdau('W 200 x 41.7(H)', 41.7, 205, 166, 7.2, 11.8, 181, 157, 53.5, 4114, 401.4, 8.77, 448.6, 901, 108.5, 4.10, 165.70, 23.19, 83948),
            PerfilGerdau('W 200 x 46.1(H)', 46.1, 203, 203, 7.2, 11.0, 181, 161, 58.6, 4543, 447.6, 8.81, 495.3, 1535, 151.2, 5.12, 229.50, 22.01, 141342),
            PerfilGerdau('W 200 x 52.0(H)', 52.0, 206, 204, 7.9, 12.6, 181, 157, 66.9, 5298, 514.4, 8.90, 572.5, 1784, 174.9, 5.16, 265.80, 33.34, 166710),
            PerfilGerdau('HP 200 x 53.0(H)', 53.0, 204, 207, 11.3, 11.3, 181, 161, 68.1, 4977, 488.0, 8.55, 551.3, 1673, 161.7, 4.96, 248.60, 31.93, 155075),
            PerfilGerdau('W 200 x 59.0(H)', 59.0, 210, 205, 9.1, 14.2, 182, 158, 76.0, 6140, 584.8, 8.99, 655.9, 2041, 199.1, 5.18, 303.00, 47.69, 195418),
            PerfilGerdau('W 200 x 71.0(H)', 71.0, 216, 206, 10.2, 17.4, 181, 161, 91.0, 7660, 709.2, 9.17, 803.2, 2537, 246.3, 5.28, 374.50, 81.66, 249976),
            PerfilGerdau('W 200 x 86.0(H)', 86.0, 222, 209, 13.0, 20.6, 181, 157, 110.9, 9498, 855.7, 9.26, 984.2, 3139, 300.4, 5.32, 458.70, 142.19, 317844),
            PerfilGerdau('W 250 x 17.9', 17.9, 251, 101, 4.8, 5.3, 240, 220, 23.1, 2291, 182.6, 9.96, 211.0, 91, 18.1, 1.99, 28.80, 2.54, 13735),
            PerfilGerdau('W 250 x 22.3', 22.3, 254, 102, 5.8, 6.9, 240, 220, 28.9, 2939, 231.4, 10.09, 267.7, 123, 24.1, 2.06, 38.40, 4.77, 18629),
            PerfilGerdau('W 250 x 25.3', 25.3, 257, 102, 6.1, 8.4, 240, 220, 32.6, 3473, 270.2, 10.31, 311.1, 149, 29.3, 2.14, 46.40, 7.06, 22955),
            PerfilGerdau('W 250 x 28.4', 28.4, 260, 102, 6.4, 10.0, 240, 220, 36.6, 4046, 311.2, 10.51, 357.3, 178, 34.8, 2.20, 54.90, 10.34, 27636),
            PerfilGerdau('W 250 x 32.7', 32.7, 258, 146, 6.1, 9.1, 240, 220, 42.1, 4937, 382.7, 10.83, 428.5, 473, 64.8, 3.35, 99.70, 10.44, 73104),
            PerfilGerdau('W 250 x 38.5', 38.5, 262, 147, 6.6, 11.2, 240, 220, 49.6, 6057, 462.4, 11.05, 517.8, 594, 80.8, 3.46, 124.10, 17.63, 93242),
            PerfilGerdau('W 250 x 44.8', 44.8, 266, 148, 7.6, 13.0, 240, 220, 57.6, 7158, 538.2, 11.15, 606.3, 704, 95.1, 3.50, 146.40, 27.14, 112398),
            PerfilGerdau('HP 250 x 62.0(H)', 62.0, 246, 256, 10.5, 10.7, 225, 201, 79.6, 8728, 709.6, 10.47, 790.5, 2995, 234.0, 6.13, 357.80, 33.46, 417130),
            PerfilGerdau('W 250 x 73.0(H)', 73.0, 253, 254, 8.6, 14.2, 225, 201, 92.7, 11257, 889.9, 11.02, 983.3, 3880, 305.5, 6.47, 463.10, 56.94, 552900),
            PerfilGerdau('W 250 x 80.0(H)', 80.0, 256, 255, 9.4, 15.6, 225, 201, 101.9, 12550, 980.5, 11.10, 1088, 4313, 338.3, 6.51, 513.10, 75.02, 622878),
            PerfilGerdau('HP 250 x 85.0(H)', 85.0, 254, 260, 14.4, 14.4, 225, 201, 108.5, 1228, 966.9, 10.64, 1093, 4225, 325.0, 6.24, 499.60, 82.07, 605403),
            PerfilGerdau('W 250 x 89.0(H)', 89.0, 260, 256, 10.7, 17.3, 225, 201, 113.9, 14237, 1.095, 11.18, 1224, 4841, 378.2, 6.52, 574.30, 102.81, 712351),
            PerfilGerdau('W 250 x 101.0(H)', 101.0, 264, 257, 11.9, 19.6, 225, 201, 128.7, 16352, 1.238, 11.27, 1395, 5549, 431.8, 6.57, 656.30, 147.70, 828031),
            PerfilGerdau('W 250 x 115.0(H)', 115.0, 269, 259, 13.5, 22.1, 225, 201, 146.1, 18920, 1.406, 11.38, 1597, 6405, 494.6, 6.62, 752.70, 212.00, 975265),
            PerfilGerdau('W 310 x 21.0', 21.0, 303, 101, 5.1, 5.7, 292, 272, 27.2, 3776, 249.2, 11.77, 291.9, 98, 19.5, 1.90, 31.40, 3.27, 21628),
            PerfilGerdau('W 310 x 23.8', 23.8, 305, 101, 5.6, 6.7, 292, 272, 30.7, 4346, 285.0, 11.89, 333.2, 116, 22.9, 1.94, 36.90, 4.65, 25594),
            PerfilGerdau('W 310 x 28.3', 28.3, 309, 102, 6.0, 8.9, 291, 271, 36.5, 5500, 356.0, 12.28, 412.0, 158, 31.0, 2.08, 49.40, 8.14, 35441),
            PerfilGerdau('W 310 x 32.7', 32.7, 313, 102, 6.6, 10.8, 291, 271, 42.1, 6570, 419.8, 12.49, 485.3, 192, 37.6, 2.13, 59.80, 12.91, 43612),
            PerfilGerdau('W 310 x 38.7', 38.7, 310, 165, 5.8, 9.7, 291, 271, 49.7, 8581, 553.6, 13.14, 615.4, 727, 88.1, 3.82, 134.90, 13.20, 163728),
            PerfilGerdau('W 310 x 44.5', 44.5, 313, 166, 6.6, 11.2, 291, 271, 57.2, 9997, 638.8, 13.22, 712.8, 855, 103.0, 3.87, 158.00, 19.90, 194433),
            PerfilGerdau('W 310 x 52.0', 52.0, 317, 167, 7.6, 13.2, 291, 271, 67.0, 11909, 751.4, 13.33, 842.5, 1026, 122.9, 3.91, 188.80, 31.81, 236422),
            PerfilGerdau('HP 310 x 79.0(H)', 79.0, 299, 306, 11.0, 11.0, 277, 245, 100.0, 16316, 1.091, 12.77, 1210, 5258, 343.7, 7.25, 525.40, 46.72, 1089258),
            PerfilGerdau('HP 310 x 93.0(H)', 93.0, 303, 308, 13.1, 13.1, 277, 245, 119.2, 19682, 1.299, 12.85, 1450, 6387, 414.7, 7.32, 635.50, 77.33, 1340320),
            PerfilGerdau('W 310 x 97.0(H)', 97.0, 308, 305, 9.9, 15.4, 277, 245, 123.6, 22284, 1.447, 13.43, 1594, 7286, 477.8, 7.68, 725.00, 92.12, 1558682),
            PerfilGerdau('W 310 x 107.0(H)', 107.0, 311, 306, 10.9, 17.0, 277, 245, 136.4, 24839, 1.597, 13.49, 1768, 8123, 530.9, 7.72, 806.10, 122.86, 1754271),
            PerfilGerdau('HP 310 x 110.0(H)', 110.0, 308, 310, 15.4, 15.5, 277, 245, 141.0, 23703, 1.539, 12.97, 1730, 7707, 497.3, 7.39, 763.70, 125.66, 1646104),
            PerfilGerdau('W 310 x 117.0(H)', 117.0, 314, 307, 11.9, 18.7, 277, 245, 149.9, 27563, 1.755, 13.56, 1952, 9024, 587.9, 7.76, 893.10, 161.61, 1965950),
            PerfilGerdau('HP 310 x 125.0(H)', 125.0, 312, 312, 17.4, 17.4, 277, 245, 159.0, 27076, 1.735, 13.05, 1963, 8823, 565.6, 7.45, 870.60, 177.98, 1911029),
            PerfilGerdau('W 360 x 32.9', 32.9, 349, 127, 5.8, 8.5, 332, 308, 42.1, 8358, 479.0, 14.09, 547.6, 291, 45.9, 2.63, 72.00, 9.15, 84111),
            PerfilGerdau('W 360 x 39.0', 39.0, 353, 128, 6.5, 10.7, 332, 308, 50.2, 10331, 585.3, 14.35, 667.7, 375, 58.6, 2.73, 91.90, 15.83, 109551),
            PerfilGerdau('W 360 x 44.0', 44.0, 352, 171, 6.9, 9.8, 332, 308, 57.7, 12258, 696.5, 14.58, 784.3, 818, 95.7, 3.77, 148.00, 16.70, 239091),
            PerfilGerdau('W 360 x 51.0', 51.0, 355, 171, 7.2, 11.6, 332, 308, 64.8, 14222, 801.2, 14.81, 899.5, 968, 113.3, 3.87, 174.70, 24.65, 284994),
            PerfilGerdau('W 360 x 57.8', 57.8, 358, 172, 7.9, 13.1, 332, 308, 72.5, 16143, 901.8, 14.92, 1014, 1113, 129.4, 3.92, 199.80, 34.45, 330394),
            PerfilGerdau('W 360 x 64.0', 64.0, 347, 203, 7.7, 13.5, 320, 288, 81.7, 17890, 1.031, 14.80, 1145, 1885, 185.7, 4.80, 284.50, 44.57, 523362),
            PerfilGerdau('W 360 x 72.0', 72.0, 350, 204, 8.6, 15.1, 320, 288, 91.3, 20169, 1.152, 14.86, 1285, 2140, 209.8, 4.84, 321.80, 61.18, 599082),
            PerfilGerdau('W 360 x 79.0', 79.0, 354, 205, 9.4, 16.8, 320, 288, 101.2, 22713, 1.283, 14.98, 1437, 2416, 235.7, 4.89, 361.90, 82.41, 685701),
            PerfilGerdau('W 360 x 91.0(H)', 91.0, 353, 254, 9.5, 16.4, 320, 288, 115.9, 26755, 1.515, 15.19, 1680, 4483, 353.0, 6.22, 538.10, 92.61, 1268709),
            PerfilGerdau('W 360 x 101.0(H)', 101.0, 357, 255, 10.5, 18.3, 320, 286, 129.5, 30279, 1.696, 15.29, 1888, 5063, 397.1, 6.25, 606.10, 128.47, 1450410),
            PerfilGerdau('W 360 x 110.0(H)', 110.0, 360, 256, 11.4, 19.9, 320, 288, 140.6, 33155, 1.841, 15.36, 2059, 5570, 435.2, 6.29, 664.50, 161.93, 1609070),
            PerfilGerdau('W 360 x 122.0(H)', 122.0, 363, 257, 13.0, 21.7, 320, 288, 155.3, 36599, 2.016, 15.35, 2269, 6147, 478.4, 6.29, 732.40, 212.70, 1787806),
            PerfilGerdau('W 410 x 38.8', 38.8, 399, 140, 6.4, 8.8, 381, 357, 50.3, 12777, 640.5, 15.94, 736.8, 404, 57.7, 2.83, 90.90, 11.69, 153190),
            PerfilGerdau('W 410 x 46.1', 46.1, 403, 140, 7.0, 11.2, 381, 357, 59.2, 15690, 778.7, 16.27, 891.1, 514, 73.4, 2.95, 115.20, 20.06, 196571),
            PerfilGerdau('W 410 x 53.0', 53.0, 403, 177, 7.5, 10.9, 381, 357, 68.4, 18734, 929.7, 16.55, 1052, 1009, 114.0, 3.84, 176.90, 23.38, 387194),
            PerfilGerdau('W 410 x 60.0', 60.0, 407, 178, 7.7, 12.8, 381, 357, 76.2, 21707, 1.066, 16.88, 1201, 1205, 135.4, 3.98, 209.20, 33.78, 467404),
            PerfilGerdau('W 410 x 67.0', 67.0, 410, 179, 8.8, 14.4, 381, 357, 86.3, 24678, 1.203, 16.91, 1362, 1379, 154.1, 4.00, 239.00, 48.11, 538546),
            PerfilGerdau('W 410 x 75.0', 75.0, 413, 180, 9.7, 16.0, 381, 357, 95.8, 27616, 1.337, 16.98, 1518, 1559, 173.2, 4.03, 269.10, 65.21, 612784),
            PerfilGerdau('W 410 x 85.0', 85.0, 417, 181, 10.9, 18.2, 381, 357, 108.6, 31658, 1.518, 17.07, 1731, 1804, 199.3, 4.08, 310.40, 94.48, 715165),
            PerfilGerdau('W 460 x 52.0', 52.0, 450, 152, 7.6, 10.8, 428, 404, 66.6, 21370, 949.8, 17.91, 1095, 634, 83.5, 3.09, 131.70, 21.79, 304837),
            PerfilGerdau('W 460 x 60.0', 60.0, 455, 153, 8.0, 13.3, 428, 404, 76.2, 25652, 1.127, 18.35, 1292, 796, 104.1, 3.23, 163.40, 34.60, 387230),
            PerfilGerdau('W 460 x 68.0', 68.0, 459, 154, 9.1, 15.4, 428, 404, 87.6, 29851, 1.300, 18.46, 1495, 941, 122.2, 3.28, 192.40, 52.29, 461163),
            PerfilGerdau('W 460 x 74.0', 74.0, 457, 190, 9.0, 14.5, 428, 404, 94.9, 33415, 1.462, 18.77, 1657, 1661, 174.8, 4.18, 271.30, 52.97, 811417),
            PerfilGerdau('W 460 x 82.0', 82.0, 460, 191, 9.9, 16.0, 428, 404, 104.7, 37157, 1.615, 18.84, 1836, 1862, 195.0, 4.22, 303.30, 70.62, 915745),
            PerfilGerdau('W 460 x 89.0', 89.0, 463, 192, 10.5, 17.7, 428, 404, 114.1, 41105, 1.775, 18.98, 2019, 2093, 218.0, 4.28, 339.00, 92.49, 1035073),
            PerfilGerdau('W 460 x 97.0', 97.0, 466, 193, 11.4, 19.0, 428, 404, 123.4, 44658, 1.916, 19.03, 2187, 2283, 236.6, 4.30, 368.80, 115.05, 1137180),
            PerfilGerdau('W 460 x 106.0', 106.0, 469, 194, 12.6, 20.6, 428, 404, 135.1, 48978, 2.088, 19.04, 2394, 2515, 259.3, 4.32, 405.70, 148.19, 1260063),
            PerfilGerdau('W 530 x 66.0', 66.0, 525, 165, 8.9, 11.4, 502, 478, 83.6, 34971, 1.332, 20.46, 1558, 857, 103.9, 3.20, 166.00, 31.52, 562854),
            PerfilGerdau('W 530 x 72.0', 72.0, 524, 207, 9.0, 10.9, 502, 478, 91.6, 39969, 1.525, 20.89, 1755, 1615, 156.0, 4.20, 244.60, 33.41, 1060548),
            PerfilGerdau('W 530 x 74.0', 74.0, 529, 166, 9.7, 13.6, 502, 478, 95.1, 40969, 1.548, 20.76, 1804, 1041, 125.5, 3.31, 200.10, 47.39, 688558),
            PerfilGerdau('W 530 x 82.0', 82.0, 528, 209, 9.5, 13.3, 501, 477, 104.5, 47569, 1.801, 21.34, 2058, 2028, 194.1, 4.41, 302.70, 51.23, 1340255),
            PerfilGerdau('W 530 x 85.0', 85.0, 535, 166, 10.3, 16.5, 502, 478, 107.7, 48453, 1.811, 21.21, 2099, 1263, 152.2, 3.42, 241.60, 72.93, 845463),
            PerfilGerdau('W 530 x 92.0', 92.0, 533, 209, 10.2, 15.6, 502, 478, 117.6, 55157, 2.069, 21.65, 2359, 2379, 227.6, 4.50, 354.70, 75.50, 1588565),
            PerfilGerdau('W 530 x 101.0', 101.0, 537, 210, 10.9, 17.4, 502, 470, 130.0, 62198, 2.316, 21.87, 2640, 2693, 256.5, 4.55, 400.60, 106.04, 1812734),
            PerfilGerdau('W 530 x 109.0', 109.0, 539, 211, 11.6, 18.8, 501, 469, 139.7, 67226, 2.494, 21.94, 2847, 2952, 279.8, 4.60, 437.40, 131.38, 1991291),
            PerfilGerdau('W 610 x 101.0', 101.0, 603, 228, 10.5, 14.9, 573, 541, 130.3, 77003, 2.554, 24.31, 2922, 2951, 258.8, 4.76, 405.00, 81.68, 2544966),
            PerfilGerdau('W 610 x 113.0', 113.0, 608, 228, 11.2, 17.3, 573, 541, 145.3, 88196, 2.901, 24.64, 3312, 3426, 300.5, 4.86, 469.70, 116.50, 2981078),
            PerfilGerdau('W 610 x 125.0', 125.0, 612, 229, 11.9, 19.6, 573, 541, 160.1, 99184, 3.241, 24.89, 3697, 3933, 343.5, 4.96, 536.30, 159.50, 3441766),
            PerfilGerdau('W 610 x 140.0', 140.0, 617, 230, 13.1, 22.2, 573, 541, 179.3, 112619, 3.650, 25.06, 4173, 4515, 392.6, 5.02, 614.00, 225.01, 3981687),
            PerfilGerdau('W 610 x 155.0', 155.0, 611, 324, 12.7, 19.0, 573, 541, 198.1, 129583, 4.241, 25.58, 4749, 10783, 665.6, 7.38, 1.022, 200.77, 9436714),
            PerfilGerdau('W 610 x 174.0', 174.0, 616, 325, 14.0, 21.6, 573, 541, 222.8, 147754, 4.797, 25.75, 5383, 12374, 761.5, 7.45, 1.171, 286.88, 10915665)
        ]

        label1 = Label(self, text = "Escolha o perfil")
        label1.grid(row = 0, column = 0, pady = 2,  sticky='nsew')
        self.cmb_perfil = Combobox(self, values=self.perfis, state="readonly", width = 17)
        self.cmb_perfil.current(0)  # define o item selecionado
        self.cmb_perfil.grid(row = 1, column=0, columnspan= 2, sticky='nsew')
        self.cmb_perfil.bind("<<ComboboxSelected>>", self.atualiza_prop)

        self.btn_prop = Button(self, text='Propriedades', command=self.mostra_prop)
        self.btn_prop.grid(row=2, column= 0, columnspan= 3, pady = 2, sticky='nsew' )

    def atualiza_prop(self, event):
        perfil_selecionado = self.cmb_perfil.get()
        perfil_selecionado_obj = next((perfil for perfil in self.perfis if str(perfil) == perfil_selecionado), None)
        self.peso = perfil_selecionado_obj.peso
        self.d = perfil_selecionado_obj.d
        self.bf = perfil_selecionado_obj.bf
        self.tw = perfil_selecionado_obj.tw
        self.tf = perfil_selecionado_obj.tf
        self.h = perfil_selecionado_obj.h
        self.dlinha = perfil_selecionado_obj.dlinha
        self.area = perfil_selecionado_obj.area
        self.ix = perfil_selecionado_obj.ix
        self.wx = perfil_selecionado_obj.wx
        self.rx = perfil_selecionado_obj.rx
        self.zx = perfil_selecionado_obj.zx
        self.iy = perfil_selecionado_obj.iy
        self.wy = perfil_selecionado_obj.wy
        self.ry = perfil_selecionado_obj.ry
        self.zy = perfil_selecionado_obj.zy
        self.it = perfil_selecionado_obj.it
        self.cw = perfil_selecionado_obj.cw
    
    def mostra_prop(self):
        self.frame_prop = Toplevel(self)
        self.frame_prop.title('Propriedades do Perfil')
        self.label_prop = Label(self.frame_prop, text= 'Aqui vão as propriedades do perfil', anchor='w', justify='left')
        self.label_prop.grid(row = 0 , column= 0, padx=15, sticky='w')

        #pega as propriedades do perfil escolhido
        perfil_selecionado = self.cmb_perfil.get()
        perfil_selecionado_obj = next((perfil for perfil in self.perfis if str(perfil) == perfil_selecionado), None)
        #peso,  d,  bf,  tw,  tf,  h,   d',  area, ix,  wx,   rx,   zx,   iy, wy,   ry,   zy,    it,   cw
        self.peso = perfil_selecionado_obj.peso
        self.prop = f''' 
        Perfil: {perfil_selecionado_obj.nome_perfil}

        Peso: {perfil_selecionado_obj.peso} kg/m
        d: {perfil_selecionado_obj.d} mm
        bf: {perfil_selecionado_obj.bf} mm
        tw: {perfil_selecionado_obj.tw} mm
        tf: {perfil_selecionado_obj.tf} mm
        h: {perfil_selecionado_obj.h} mm
        d': {perfil_selecionado_obj.dlinha} mm
        Área: {perfil_selecionado_obj.area} cm2
        Ix: {perfil_selecionado_obj.ix} cm4
        Wx: {perfil_selecionado_obj.wx} cm3
        rx: {perfil_selecionado_obj.rx} cm
        zx: {perfil_selecionado_obj.zx} cm3
        Iy: {perfil_selecionado_obj.iy} cm4
        Wy: {perfil_selecionado_obj.wy} cm3
        ry: {perfil_selecionado_obj.ry} cm
        zy: {perfil_selecionado_obj.zy} cm3
        it: {perfil_selecionado_obj.it} cm4
        cw: {perfil_selecionado_obj.cw} cm6
        '''
        self.label_prop.config(text= self.prop)

class Frame_Resultados(Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.label_tit = LabelFrame(self, text= 'Resultados (kN e kN*cm)', width= 250, height = 100)
        self.label_tit.grid(row= 0 , column= 0, columnspan= 2)
        self.label_tit.grid_propagate(False)

        self.label_ntrd = Label(self.label_tit, text= 'Nt,Rd')
        self.label_ntrd.grid(row=1, column=0, padx= (10,0) )
        self.entry_ntrd = Entry(self.label_tit, width = 10)
        #self.entry_ntrd.config(state='readonly')
        self.entry_ntrd.grid(row=1, column=1, padx = 3 , pady = 3)

        self.label_ncrd = Label(self.label_tit, text= 'Nc,Rd')
        self.label_ncrd.grid(row=2, column=0, padx= (10,0) )
        self.entry_ncrd = Entry(self.label_tit, width = 10)
        self.entry_ncrd.grid(row=2, column=1, padx = 3 , pady = 3)

        self.label_mxrd = Label(self.label_tit, text= 'Mx,Rd')
        self.label_mxrd.grid(row=3, column=0 , padx= (10,0))
        self.entry_mxrd = Entry(self.label_tit, width = 10)
        self.entry_mxrd.grid(row=3, column=1, padx = 3 , pady = 3)

        self.label_vxrd = Label(self.label_tit, text= 'Vx,Rd')
        self.label_vxrd.grid(row=1, column=2, padx= (15,0) )
        self.entry_vxrd = Entry(self.label_tit, width = 10)
        self.entry_vxrd.grid(row=1, column=3, padx = 3 , pady = 3)

        self.label_vyrd = Label(self.label_tit, text= 'Vy,Rd')
        self.label_vyrd.grid(row=2, column=2, padx= (15,0) )
        self.entry_vyrd = Entry(self.label_tit, width = 10)
        self.entry_vyrd.grid(row=2, column=3, padx = 3 , pady = 3)

        self.label_myrd = Label(self.label_tit, text= 'My,Rd')
        self.label_myrd.grid(row=3, column=2 , padx= (15,0) )
        self.entry_myrd = Entry(self.label_tit, width = 10)
        self.entry_myrd.grid(row=3, column=3, padx = 3 , pady = 3)

class PerfilGerdau:
    def __init__(self, nome_perfil, peso, d, bf, tw, tf, h, dlinha, area, ix, wx, rx, zx,
                 iy, wy, ry, zy, it, cw):
        self.nome_perfil = nome_perfil
        self.peso = peso
        self.d = d
        self.bf = bf
        self.tw = tw
        self.tf = tf
        self.h = h
        self.dlinha = dlinha
        self.area = area
        self.ix = ix
        self.wx = wx
        self.rx = rx
        self.zx = zx
        self.iy = iy
        self.wy = wy
        self.ry = ry
        self.zy = zy
        self.it = it
        self.cw = cw

    def __str__(self):
        return f"{self.nome_perfil}"
    
class Tracao:
    def __init__(self, ag, fy):
        self.ag = ag #cm2
        self.fy = fy /10.0 #kN/cm2
        #força resistente a tração
        self.ntrd = (self.ag * self.fy) /1.10

class Compressao:
    def __init__(self, e, fy, ag, dlinha, tw, bf, tf, ix, lx, iy, ly, lz, it, g, cw, rx, ry, x0, y0):
        self.ag = ag #cm2
        self.fy = fy /10.0 #kN/cm2
        self.e = e / 10.0 #kN/cm2
        self.dlinha = dlinha / 10.0 #cm
        self.tw = tw /10.0 #cm
        self.bf = bf/ 10.0 #cm
        self.tf = tf / 10.0 #cm
        self.ix = ix #cm4
        self.lx = lx #cm
        self.iy = iy #cm4
        self.ly = ly #cm
        self.lz = lz #cm
        self.it = it #cm4
        self.g = g / 10.0 #kN/cm2
        self.cw = cw #cm6
        self.rx = rx #cm
        self.ry = ry #cm
        self.x0 = x0 #cm
        self.y0 = y0  #cm
        self.x = 1
        self.bef_alma = 0
        self.bef_mesa = 0
        self.c1 = 0 
        self.c2 = 0
        self.tensao_ele_alma = 0
        self.tensao_ele_mesa = 0
        self.aef = 0

        #5.3.3 - Flambagem global
        #modo de flambagem em x
        self.nex = (math.pow(math.pi, 2.0) * self.e * self.ix) / (math.pow(self.lx, 2.0))
        #modo de flambagem em y
        self.ney = (math.pow(math.pi, 2.0) * self.e * self.iy) / (math.pow(self.ly, 2.0))
        #modo de flambagem em z
        self.r0 = math.sqrt((math.pow(self.x0, 2.0) + math.pow(self.y0, 2.0) + math.pow(self.rx, 2.0) + math.pow(self.ry, 2.0)))
        self.nez = (1 / math.pow(self.r0, 2.0)) * ((math.pow(math.pi,2.0) * self.e * self.cw) / (math.pow(self.lz, 2.0)) + self.g * self.it)

        self.ne = min(self.nex, self.ney, self.nez)

        #Índice de esbeltez reduzido
        self.lambda0 = math.sqrt((self.ag * self.fy) / self.ne)

        if self.lambda0 <= 1.5:
            self.x = math.pow(0.658, math.pow(self.lambda0, 2.0))
        else:
            self.x = 0.877 / math.pow(self.lambda0, 2.0)


        #5.3.4 - Área efetiva da seção transversal
        #Flambabem local da alma
        self.btalma = self.dlinha / self.tw
        self.btlimalma = 1.49 * math.sqrt(self.e / self.fy)/math.sqrt(self.x)

        if self.btalma <= self.btlimalma:
            self.bef_alma = self.dlinha
        else:
            self.c1 = 0.18
            self.c2 = 1.31
            self.tensao_ele_alma = math.pow((self.c2 * (self.btlimalma / self.btalma) ), 2.0) * self.fy
            self.bef_alma = self.dlinha * (1 - (self.c1 * math.sqrt(self.tensao_ele_alma / (self.x * self.fy))) * (math.sqrt(self.tensao_ele_alma / (self.x * self.fy))) )
        
        #Flambagem local da mesa
        self.btmesa = self.bf / (2 * self.tf)
        self.btlimmesa = 0.56 * math.sqrt(self.e / self.fy)/math.sqrt(self.x)
        if self.btmesa <= self.btlimmesa:
            self.bef_mesa = self.bf / 2.0
        else:
            self.c1 = 0.22
            self.c2 = 1.49
            self.tensao_ele_mesa = math.pow((self.c2 * (self.btlimmesa / self.btmesa) ), 2.0) * self.fy
            self.bef_mesa = self.dlinha * (1 - (self.c1 * math.sqrt(self.tensao_ele_mesa / (self.x * self.fy))) * (math.sqrt(self.tensao_ele_mesa / (self.x * self.fy))) )

        #Cálculo da área efetiva
        self.aef = self.ag - ((self.dlinha -self.bef_alma ) * self.tw + 4 * ((self.bf / 2.0 ) - self.bef_mesa) * self.tf)

        #Força normal resistente de cálculo
        self.ncrd = (self.x * self.aef * self.fy) / 1.10

class Momento_X:
    def __init__(self, e, g, fy, zx, wx, it, bf, tf, dlinha, tw, lb, ry, cb, iy, cw):
        self.e = e / 10.0  #kN/cm2
        self.fy = fy /10.0 #kN/cm2
        self.g = g /10.0 #kN/cm2
        self.zx = zx #cm3
        self.wx = wx #cm3
        self.it = it #cm4
        self.bf = bf /10 #cm
        self.tf = tf /10 #cm
        self.tw = tw /10 #cm
        self.dlinha = dlinha /10 #cm
        self.lb = lb #cm
        self.ry = ry #cm
        self.iy = iy #cm4
        self.cw = cw #cm6
        self.mrd_mesa = 0 
        self.mrd_alma = 0 
        self.mrd_flt = 0
        self.cb = cb

        #Momentos de plastificação e residual
        self.mpl = self.zx * self.fy
        self.mr = self.wx * 0.7 * self.fy    
        self.mr_fla = self.wx * self.fy    

        #Flambagem local da mesa - FLM
        #esbeltez da mesa
        self.esb_mesa = self.bf / (2 * self.tf)
        #esbeltez limite P da mesa
        self.esb_lim_p_mesa = 0.38 * math.sqrt(self.e / self.fy)
        #esbeltez limite R da mesa
        self.esb_lim_r_mesa = 0.83 * math.sqrt(self.e / (0.7*self.fy))

        #determina o momento fletor resistente para FLM
        if self.esb_mesa <= self.esb_lim_p_mesa:
            self.mrd_mesa = self.mpl / 1.10
        else:
            if self.esb_mesa > self.esb_lim_p_mesa and self.esb_mesa <= self.esb_lim_r_mesa:
                self.mrd_mesa = (self.mpl - (self.mpl - self.mr)* ((self.esb_mesa - self.esb_lim_p_mesa) / (self.esb_lim_r_mesa - self.esb_lim_p_mesa))) / 1.10
            else:
                self.mrd_mesa = (0.69 * self.e * self.wx) / math.pow(self.esb_lim_r_mesa, 2.0)

        #Flambagem local da alma - FLA
        #esbeltez da alma
        self.esb_alma = self.dlinha / self.tw
        #esbeltez limite P da alma
        self.esb_lim_p_alma = 3.76 * math.sqrt(self.e / self.fy)
        #esbeltez limite R da alma
        self.esb_lim_r_alma = 5.70 * math.sqrt(self.e / self.fy)

        #determina o momento fletor resistente para FLA
        if self.esb_alma <= self.esb_lim_p_alma:
            self.mrd_alma = self.mpl / 1.10
        else:
            if self.esb_alma > self.esb_lim_p_alma and self.esb_alma <= self.esb_lim_r_alma:
                self.mrd_alma = (self.mpl - (self.mpl - self.mr_fla)* ((self.esb_alma - self.esb_lim_p_alma) / (self.esb_lim_r_alma - self.esb_lim_p_alma))) / 1.10
            else:
                self.mrd_alma = 0

        #Flambagem lateral com torção - FLT
        #esbeltez flt
        self.esb_flt = self.lb / self.ry
        #esbeltez limite P para flt
        self.esb_lim_p_flt = 1.76 * math.sqrt(self.e / self.fy)
        #esbeltez limite R para flt
        self.b1 = (0.7 * self.fy * self.wx) / (self.e * self.it)
        self.esb_lim_r_flt =((1.38 * self.cb * math.sqrt(self.iy * self.it) ) / (self.ry * self.it * self.b1)) * math.sqrt(1 + math.sqrt(1 + (27 * self.cw * math.pow(self.b1, 2.0) ) / (math.pow(self.cb, 2.0) * self.iy)))

        #determina o momento fletor resistente para FLT
        if self.esb_flt <= self.esb_lim_p_flt:
            self.mrd_flt = self.mpl / 1.10
        else:
            if self.esb_flt > self.esb_lim_p_flt and self.esb_flt <= self.esb_lim_r_flt:
                self.mrd_flt = (self.mpl - (self.mpl - self.mr)* ((self.esb_flt - self.esb_lim_p_flt) / (self.esb_lim_r_flt - self.esb_lim_p_flt))) / 1.10
            else:
                self.mcr_flt = ((self.cb * math.pow(math.pi, 2.0)* self.e * self.iy) / math.pow(self.lb, 2.0)) * math.sqrt((self.cw / self.iy) * (1 + (0.0039 * self.it * math.pow(self.lb, 2.0)) / (self.cw)))
                self.mrd_flt = self.mcr_flt / 1.10

        #momento fletor máximo
        self.mom_max = (1.5 * self.wx * self.fy) / 1.10

        #Momento fletor resistente
        self.mxrd = min(self.mrd_alma, self.mrd_mesa, self.mrd_flt, self.mom_max)

class Momento_Y:
    def __init__(self, e, g, fy, zy, wy, it, bf, tf, dlinha, tw, lb, ry, cb, iy, cw):
        self.e = e / 10.0  #kN/cm2
        self.fy = fy /10.0 #kN/cm2
        self.g = g /10.0 #kN/cm2
        self.zy = zy #cm3
        self.wy = wy #cm3
        self.it = it #cm4
        self.bf = bf /10 #cm
        self.tf = tf /10 #cm
        self.tw = tw /10 #cm
        self.dlinha = dlinha /10 #cm
        self.lb = lb #cm
        self.ry = ry #cm
        self.iy = iy #cm4
        self.cw = cw #cm6
        self.mrd_mesa = 0 
        self.mrd_alma = 0 
        self.mrd_flt = 0
        self.cb = cb

        #Momentos de plastificação e residual
        self.mpl = self.zy * self.fy
        self.mr = self.wy * 0.7 * self.fy      
        self.mr_fla = self.wy * self.fy  

        #Flambagem local da mesa - FLM
        #esbeltez da mesa
        self.esb_mesa = self.bf / (2 * self.tf)
        #esbeltez limite P da mesa
        self.esb_lim_p_mesa = 0.38 * math.sqrt(self.e / self.fy)
        #esbeltez limite R da mesa
        self.esb_lim_r_mesa = 0.83 * math.sqrt(self.e / (0.7*self.fy))

        #determina o momento fletor resistente para FLM
        if self.esb_mesa <= self.esb_lim_p_mesa:
            self.mrd_mesa = self.mpl / 1.10
        else:
            if self.esb_mesa > self.esb_lim_p_mesa and self.esb_mesa <= self.esb_lim_r_mesa:
                self.mrd_mesa = (self.mpl - (self.mpl - self.mr)* ((self.esb_mesa - self.esb_lim_p_mesa) / (self.esb_lim_r_mesa - self.esb_lim_p_mesa))) / 1.10
            else:
                self.mrd_mesa = (0.69 * self.e * self.wx) / math.pow(self.esb_lim_r_mesa, 2.0)

        #Flambagem local da alma - FLA
        #esbeltez da alma
        self.esb_alma = self.dlinha / self.tw
        #esbeltez limite P da alma
        self.esb_lim_p_alma = 1.12 * math.sqrt(self.e / self.fy)
        #esbeltez limite R da alma
        self.esb_lim_r_alma = 1.40 * math.sqrt(self.e / self.fy)
        #momento crítico para FLA
        self.mom_cr_fla = self.wy * self.fy

        #determina o momento fletor resistente para FLA
        if self.esb_alma <= self.esb_lim_p_alma:
            self.mrd_alma = self.mpl / 1.10
        else:
            if self.esb_alma > self.esb_lim_p_alma and self.esb_alma <= self.esb_lim_r_alma:
                self.mrd_alma = (self.mpl - (self.mpl - self.mr_fla) * ((self.esb_alma - self.esb_lim_p_alma) / (self.esb_lim_r_alma - self.esb_lim_p_alma))) / 1.10
            else:
                self.mrd_alma = self.mom_cr_fla / 1.10 #kN*cm

        #momento fletor máximo
        self.mom_max = (1.5 * self.wy * self.fy) / 1.10

        #Momento fletor resistente
        self.myrd = min(self.mrd_alma, self.mrd_mesa, self.mom_max)

class Cortante_X:
    def __init__(self, dlinha, tw, fy, e):
        self.dlinha = dlinha /10.0 #cm
        self.tw = tw /10.0 # cm
        self.fy = fy /10.0 #kN/cm2
        self.e = e /10.0 #kN/cm2
        self.vrd = 0 #kN
        self.aw = self.dlinha * self.tw
        self.vpl = 0.6 * self.aw * self.fy


        #lambda da alma
        self.lambda_alma = self.dlinha / self.tw
        #lambda p
        self.lambda_p = 1.10 * math.sqrt((5 * self.e) / self.fy)
        #lambda q
        self.lambda_r = 1.37 * math.sqrt((5 * self.e) / self.fy)

        if self.lambda_alma <= self.lambda_p:
            self.vrd = self.vpl / 1.10
        elif self.lambda_alma > self.lambda_p and self.lambda_alma <= self.lambda_r:
            self.vrd = (self.lambda_p / self.lambda_r) * (self.vpl / 1.10)
        elif self.lambda_alma > self.lambda_r:
            self.vrd = 1.24 * math.pow((self.lambda_p / self.lambda_alma), 2.0) * (self.vpl / 1.10)

class Cortante_Y:
    def __init__(self, bf, tf, fy, e, tw):
        self.bf = bf /10.0 #cm
        self.tf = tf /10.0 #cm
        self.tw = tw /10.0 #cm
        self.fy = fy /10.0 #kN/cm2
        self.e = e /10.0 #kN/cm2
        self.vrd = 0 #kN
        self.h = self.bf /2 
        self.aw = 2 * self.bf * self.tf
        self.vpl = 0.6 * self.aw * self.fy

        #lambda da alma
        self.lambda_alma = self.h / self.tw
        #lambda P
        self.lambda_p = 1.10 * math.sqrt((1.2 * self.e) / self.fy)
        #lambda R
        self.lambda_r = 1.37 * math.sqrt((1.2 * self.e) / self.fy)

        if self.lambda_alma <= self.lambda_p:
            self.vrd = self.vpl / 1.10
        elif self.lambda_alma > self.lambda_p and self.lambda_alma <= self.lambda_r:
            self.vrd = (self.lambda_p / self.lambda_r) * (self.vpl / 1.10)
        elif self.lambda_alma > self.lambda_r:
            self.vrd = 1.24 * math.pow((self.lambda_p / self.lambda_alma), 2.0) * (self.vpl / 1.10)

class Gerar_pdf:
    def __init__(self, perfil_inst, tracao_inst, comp_inst, cortantex_inst, cortantey_inst, momentox_inst, momentoy_inst): #instancias das classes
        self.tracao = tracao_inst
        self.comp = comp_inst
        self.cortantex = cortantex_inst
        self.cortantey = cortantey_inst
        self.momx = momentox_inst
        self.momy = momentoy_inst
        self.perfil = perfil_inst

    def gerar(self):
        # Define as margens do PDF
        geometry_options = {
        "top": "2cm",    # Margem superior
        "bottom": "2cm", # Margem inferior
        "left": "1.5cm", # Margem esquerda
        "right": "1.5cm" # Margem direita
    }

        # Criar o documento LaTeX
        doc = Document(geometry_options=geometry_options)
        with doc.create(Center()):
            doc.append(NoEscape(r"\textbf{\Large MEMORIAL DE CÁLCULO (NBR 8800/2024)}\par"))
        doc.append(f"Perfil: {self.perfil.cmb_perfil.get()}")


    #TRAÇÃO----------------------------------------------------------
        ag = self.tracao.ag
        fy = self.tracao.fy  #kN/cm2
        ntrd = self.tracao.ntrd

        # Seção principal
        with doc.create(Section("Cálculo de Tração")):
            doc.append(f"")

        # Cálculo da força resistente
        with doc.create(Subsection("Cálculo da Força Resistente à Tração (Item 5.2.2)")):
            doc.append("Força resistente à tração (escoamento da seção bruta):")
            with doc.create(Math()):
                doc.append(NoEscape(r'N_{{trd}} = \frac{{A_g \cdot f_y}}{1.10}'))
                doc.append(NoEscape(r' = \frac{{%.2f \cdot %.2f}}{1.10}' % (ag, fy)))
                doc.append(f"= {ntrd:.2f}  \u00A0  kN")

        #Compressão ---------------------------------------------------------------------------
        self.e = self.comp.e #kN/cm2
        self.g = self.comp.g #kN/cm2
        self.lx = self.comp.lx
        self.ly = self.comp.ly
        self.lz = self.comp.lz
        self.fy = self.comp.fy
        self.ix = self.comp.ix
        self.iy = self.comp.iy
        self.it = self.comp.it
        self.nex = self.comp.nex
        self.ney = self.comp.ney
        self.nez = self.comp.nez
        self.ne = self.comp.ne
        self.r0 = self.comp.r0
        self.rx = self.comp.rx
        self.ry = self.comp.ry
        self.cw = self.comp.cw
        self.ag = self.comp.ag
        self.lamb_0 = self.comp.lambda0
        self.x = self.comp.x
        self.dlinha = self.comp.dlinha
        self.tw = self.comp.tw
        self.lamb_alma = self.comp.btalma
        self.lamb_mesa = self.comp.btmesa
        self.lamb_alma_lim = self.comp.btlimalma
        self.lamb_mesa_lim = self.comp.btlimmesa
        self.sigma_ele_alma = self.comp.tensao_ele_alma
        self.sigma_ele_mesa= self.comp.tensao_ele_mesa
        self.bef_alma = self.comp.bef_alma
        self.bef_mesa = self.comp.bef_mesa
        self.b_mesa = self.comp.bf / 2.0
        self.tf = self.comp.tf
        self.a_ef = self.comp.aef
        self.ncrd = self.comp.ncrd

        # Seção principal
        with doc.create(Section("Cálculo da Força de Compressão")):
            doc.append(f"")

        # Cálculo da força resistente a compressão
        with doc.create(Subsection("Força axial de flambagem (Item 5.3.5)")):
            with doc.create(Math()):
                doc.append(NoEscape(r"N_{ex} = \frac{{\pi^2 \cdot E \cdot I_x}}{L_x^2}"))
                doc.append(NoEscape(r"= \frac{{\pi^2 \cdot %.0f \cdot %.0f}}{%.2f^2}" % (self.e, self.ix, self.lx)))
                doc.append(NoEscape(f"= {self.nex:.2f}  \u00A0 kN \n"))  
            with doc.create(Math()):
                doc.append(NoEscape(r"N_{ey} = \frac{{\pi^2 \cdot E \cdot I_y}}{L_y^2}"))
                doc.append(NoEscape(r"= \frac{{\pi^2 \cdot %.0f \cdot %.0f}}{%.2f^2}" % (self.e, self.iy, self.ly)))
                doc.append(NoEscape(f"= {self.ney:.2f}  \u00A0 kN \n"))  
            with doc.create(Math()):
                doc.append(NoEscape(r"N_{ez} = \frac{1}{r_0^2} \cdot \left(\frac{\pi^2 \cdot E \cdot C_w}{L_z^2} + G \cdot I_t \right)"))
                doc.append(NoEscape(r" = \frac{1}{%.2f^2} \cdot \left(\frac{\pi^2 \cdot %.0f \cdot %.0f}{%.2f^2} + %.0f \cdot %.2f \right)" % 
                                    (self.r0, self.e, self.cw, self.lz,self.comp.g, self.comp.it )))
                doc.append(NoEscape(f"= {self.nez:.2f}  \u00A0 kN \n")) 
        doc.append(f"Força normal de flambagem elástica (Ne): {self.ne:.2f} kN")

        with doc.create(Subsection("Índice de esbeltez reduzido (Item 5.3.3.2)")):
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_0 = \sqrt{\frac{a_g \cdot f_y}{N_e}}'))
                doc.append(NoEscape(r'= \sqrt{\frac{%.2f \cdot %.2f}{%.2f}}' % (self.ag, self.fy, self.ne)))
                doc.append(NoEscape(f"= {self.lamb_0:.2f} \n")) 
       
        with doc.create(Subsection("Fator de redução (Item 5.3.3)")):
            if self.lamb_0 <= 1.5:
                with doc.create(Math()):
                    doc.append(NoEscape(r'\chi = 0.658^{\lambda_0^2}'))
                    doc.append(NoEscape(r' = 0.658^{%.2f^2}' % (self.lamb_0)))
                    doc.append(NoEscape(f"= {self.x:.2f} \n")) 
            else:
                with doc.create(Math()):
                    doc.append(NoEscape(r'\chi = \frac{0.877}{\lambda_0^2}'))
                    doc.append(NoEscape(r' = \frac{0.877}{%.2f^2}' % (self.lamb_0)))
                    doc.append(NoEscape(f"= {self.x:.2f} \n"))   

        with doc.create(Subsection("Largura efetiva dos elementos (Item 5.3.4.2)")):
            doc.append("Esbeltez da alma:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\frac{b}{t} = \frac{%.2f}{%.2f}" %(self.dlinha, self.tw)))
                doc.append(NoEscape(f"= {self.lamb_alma:.2f} \n")) 
            doc.append("Esbeltez limite da alma:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\frac{1.49 \cdot \sqrt{\frac{E}{f_y}}}{\sqrt{\chi}} "))
                doc.append(NoEscape(r"= \frac{1.49 \cdot \sqrt{\frac{%.0f}{%.2f}}}{\sqrt{%.2f}} " % (self.e, self.fy, self.x)))
                doc.append(NoEscape(f"= {self.lamb_alma_lim:.2f} \n"))
            doc.append("Largura efetiva da alma:")
            if self.lamb_alma <= self.lamb_alma_lim:
                with doc.create(Math()):
                    doc.append(NoEscape(r" b_{ef} = %.2f \ cm" % (self.bef_alma)))
            else:
                with doc.create(Math()):        
                    doc.append(NoEscape(r" b_{ef} = b \cdot \left( 1 - c_1 \cdot \sqrt{\frac{\sigma_{el}}{\chi \cdot f_y}} \right) \cdot \sqrt{\frac{\sigma_{el}}{\chi \cdot f_y}} ")) 
                    doc.append(NoEscape(r" = %.2f \cdot \left(1 - 0.18 \cdot \sqrt{\frac{%.2f}{%.2f \cdot %.2f}} \right) \cdot \sqrt{\frac{%.2f}{%.2f \cdot %.2f}}" % (self.dlinha, self.sigma_ele_alma, self.x, self.fy, self.sigma_ele_alma, self.x, self.fy ))) 
                    doc.append(NoEscape(f"= {self.bef_alma:.2f} \n")) 
            
            doc.append("Esbeltez da mesa:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\frac{b}{t} = \frac{%.2f}{%.2f}" %(self.b_mesa, self.tf)))
                doc.append(NoEscape(f"= {self.lamb_mesa:.2f} \n")) 
            doc.append("Esbeltez limite da mesa:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\frac{0.56 \cdot \sqrt{\frac{E}{f_y}}}{\sqrt{\chi}} "))
                doc.append(NoEscape(r"= \frac{0.56 \cdot \sqrt{\frac{%.0f}{%.2f}}}{\sqrt{%.2f}} " % (self.e, self.fy, self.x)))
                doc.append(NoEscape(f"= {self.lamb_mesa_lim:.2f} \n"))
            doc.append("Largura efetiva da mesa:")
            if self.lamb_mesa <= self.lamb_mesa_lim:
                with doc.create(Math()):
                    doc.append(NoEscape(r" b_{ef} = %.2f \ cm" % (self.bef_mesa)))
            else:
                with doc.create(Math()):        
                    doc.append(NoEscape(r" b_{ef} = b \cdot \left( 1 - c_1 \cdot \sqrt{\frac{\sigma_{el}}{\chi \cdot f_y}} \right) \cdot \sqrt{\frac{\sigma_{el}}{\chi \cdot f_y}} ")) 
                    doc.append(NoEscape(r" = %.2f \cdot \left(1 - 0.18 \cdot \sqrt{\frac{%.2f}{%.2f \cdot %.2f}} \right) \cdot \sqrt{\frac{%.2f}{%.2f \cdot %.2f}}" % (self.dlinha, self.sigma_ele_mesa, self.x, self.fy, self.sigma_ele_mesa, self.x, self.fy ))) 
                    doc.append(NoEscape(f" = {self.bef_mesa:.2f} \n")) 

            doc.append("Área efetiva:")
            with doc.create(Math()):
                doc.append(NoEscape(r" A_{ef} = %.2f \ {cm}^2" % (self.a_ef)))

            doc.append("Força axial resistente de cálculo:")
            with doc.create(Math()):
                doc.append(NoEscape(r" N_{c,rd} = \frac{\chi \cdot A_{ef} \cdot f_y}{1.10}"))
                doc.append(NoEscape(r" = \frac{%.2f \cdot %.2f \cdot %.2f}{1.10}" % (self.x, self.a_ef, self.fy)))
                doc.append(NoEscape(f" = {self.ncrd:.2f} \u00A0 kN \n")) 


        #Cortante X----------------------------------------------------------------------------
        self.dlinha = self.cortantex.dlinha  #cm
        self.tw = self.cortantex.tw  #cm
        self.aw = self.cortantex.aw #cm2
        self.vpl = self.cortantex.vpl #kN
        self.lamb_p = self.cortantex.lambda_p
        self.lamb_r = self.cortantex.lambda_r
        self.lambda_alma = self.cortantex.lambda_alma
        self.e = self.cortantex.e #kN/cm2
        self.fy = self.cortantex.fy #kN/cm2
        self.vrd = self.cortantex.vrd #kN

        # Seção principal
        with doc.create(Section("Cálculo da Força Cortante")):
            doc.append(f"")

        # Cálculo da força resistente a cortante
        with doc.create(Subsection("Cálculo da Força Resistente a Cortante em X (Item 5.4.3.1)")):
            doc.append("Área efetiva de cisalhamento:")
            with doc.create(Math()):
                doc.append(NoEscape(r"A_w = d' \cdot t_w = %.2f \cdot %.2f" % (self.dlinha, self.tw)))
                doc.append(NoEscape(f"= {self.aw:.2f}  \u00A0 {{cm}}^2"))  # LaTeX notation for cm²

            doc.append("Força cortante de plastificação:")
            with doc.create(Math()):
                doc.append(NoEscape(r"V_{pl} = 0.6 \cdot A_w \cdot f_y"))
                doc.append(NoEscape(r"= 0.6 \cdot %.2f \cdot %.2f" % (self.aw, self.fy)))
                doc.append(NoEscape(f"= {self.vpl:.2f}  \u00A0 kN")) 

            doc.append("Esbeltez do perfil:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\lambda = \frac{d'}{t_w}"))
                doc.append(NoEscape(r"= \frac{%.2f}{%.2f}" % (self.dlinha, self.tw)))
                doc.append(f"= {self.lambda_alma:.2f}")

            doc.append("Lambda P:")
            with doc.create(Math()):
                lambda_p_formula = r'\lambda_p = 1.10 \cdot \sqrt{\frac{{k_v \cdot E}}{{f_y}}}'
                doc.append(NoEscape(lambda_p_formula))
                lambda_p_formula = r'= 1.10 \cdot \sqrt{\frac{{5 \cdot %.0f}}{{%.2f}}}' % (self.e, self.fy)
                doc.append(NoEscape(lambda_p_formula))
                doc.append(f"= {self.lamb_p:.2f} ")

            doc.append("Lambda R:")
            with doc.create(Math()):
                lambda_r_formula = r'\lambda_r = 1.37 \cdot \sqrt{\frac{{k_v \cdot E}}{{f_y}}}'
                doc.append(NoEscape(lambda_r_formula))
                lambda_r_formula = r'= 1.37 \cdot \sqrt{\frac{{5 \cdot %.0f}}{{%.2f}}}' % (self.e, self.fy)
                doc.append(NoEscape(lambda_r_formula))
                doc.append(f"= {self.lamb_r:.2f} ")

            doc.append("Força cortante resistente:")
            if self.lambda_alma <= self.lamb_p:
                with doc.create(Math()):
                    doc.append(NoEscape(r'V_{rd} = \frac{V_{pl}}{1.10}'))
                    doc.append(NoEscape(r' = \frac{%.2f}{1.10}' % (self.vpl)))
                    doc.append(f"= {self.vrd:.2f}   \u00A0   kN")
            elif self.lambda_alma > self.lamb_p and self.lambda_alma <= self.lamb_r:
                with doc.create(Math()):
                    doc.append(NoEscape(r'V_{rd} = \frac{\lambda_p}{\lambda_r} \cdot \frac{V_{pl}}{1.10}'))
                    doc.append(NoEscape(r' = \frac{%.0f}{%.0f} \cdot \frac{%.2f}{1.10}' % (self.lamb_p, self.lamb_r, self.vpl)))
                    doc.append(f"= {self.vrd:.2f}   \u00A0   kN")
            elif self.lambda_alma > self.lamb_r:
                with doc.create(Math()):
                    doc.append(NoEscape(r'V_{rd} = 1.24 \cdot \left(\frac{\lambda_p}{\lambda}\right)^2 \cdot \frac{V_{pl}}{1.10}'))
                    doc.append(NoEscape(r' = 1.24 \cdot \left(\frac{%.0f}{%.2f}\right)^2 \cdot \frac{%.2f}{1.10}' %(self.lamb_p, self.lambda_alma, self.vpl)))
                    doc.append(f"= {self.vrd:.2f}   \u00A0   kN")
       
        #Cortante Y----------------------------------------------------------------------------
        self.tw = self.cortantey.tw  #cm
        self.aw = self.cortantey.aw #cm2
        self.vpl = self.cortantey.vpl #kN
        self.lamb_p = self.cortantey.lambda_p
        self.lamb_r = self.cortantey.lambda_r
        self.lambda_alma = self.cortantey.lambda_alma
        self.e = self.cortantey.e #kN/cm2
        self.fy = self.cortantey.fy #kN/cm2
        self.vrd = self.cortantey.vrd #kN
        self.bf = self.cortantey.bf
        self.tf = self.cortantey.tf
        self.h = self.cortantey.h

        # Cálculo da força resistente a cortante em Y
        with doc.create(Subsection("Cálculo da Força Resistente a Cortante em Y (Item 5.4.3.5)")):
            doc.append("Área efetiva de cisalhamento:")
            with doc.create(Math()):
                doc.append(NoEscape(r"A_w = 2 \cdot b_f \cdot t_f = 2 \cdot %.2f \cdot %.2f " % (self.cortantey.bf, self.cortantey.tf)))
                doc.append(NoEscape(f"= {self.aw:.2f}  \u00A0 {{cm}}^2"))  # LaTeX notation for cm²

            doc.append("Força cortante de plastificação:")
            with doc.create(Math()):
                doc.append(NoEscape(r"V_{pl} = 0.6 \cdot A_w \cdot f_y"))
                doc.append(NoEscape(r"= 0.6 \cdot %.2f \cdot %.2f" % (self.aw, self.fy)))
                doc.append(NoEscape(f"= {self.vpl:.2f}  \u00A0 kN")) 
            
            doc.append("Valor de 'h':")
            with doc.create(Math()):
                doc.append(NoEscape(r"h = \frac{b_f}{2} = \frac{%.2f}{2} = %.2f \ cm" % (self.cortantey.bf, self.cortantey.h) ))

            doc.append("Esbeltez do perfil:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\lambda = \frac{h}{t_w}"))
                doc.append(NoEscape(r"= \frac{%.2f}{%.2f}" % (self.h, self.tw)))
                doc.append(f"= {self.lambda_alma:.2f}")

            doc.append("Lambda P:")
            with doc.create(Math()):
                lambda_p_formula = r'\lambda_p = 1.10 \cdot \sqrt{\frac{{k_v \cdot E}}{{f_y}}}'
                doc.append(NoEscape(lambda_p_formula))
                lambda_p_formula = r'= 1.10 \cdot \sqrt{\frac{{1.2 \cdot %.0f}}{{%.2f}}}' % (self.e, self.fy)
                doc.append(NoEscape(lambda_p_formula))
                doc.append(f"= {self.lamb_p:.2f}")
        
            doc.append("Lambda R:")
            with doc.create(Math()):
                lambda_r_formula = r'\lambda_r = 1.37 \cdot \sqrt{\frac{{k_v \cdot E}}{{f_y}}}'
                doc.append(NoEscape(lambda_r_formula))
                lambda_r_formula = r'= 1.37 \cdot \sqrt{\frac{{1.2 \cdot %.0f}}{{%.2f}}}' % (self.e, self.fy)
                doc.append(NoEscape(lambda_r_formula))
                doc.append(f"= {self.lamb_r:.2f} ")
            
            doc.append("Força cortante resistente:")
            if self.lambda_alma <= self.lamb_p:
                with doc.create(Math()):
                    doc.append(NoEscape(r'V_{rd} = \frac{V_{pl}}{1.10}'))
                    doc.append(NoEscape(r' = \frac{%.2f}{1.10}' % (self.vpl)))
                    doc.append(f"= {self.vrd:.2f}   \u00A0   kN")
            elif self.lambda_alma > self.lamb_p and self.lambda_alma <= self.lamb_r:
                with doc.create(Math()):
                    doc.append(NoEscape(r'V_{rd} = \frac{\lambda_p}{\lambda_r} \cdot \frac{V_{pl}}{1.10}'))
                    doc.append(NoEscape(r' = \frac{%.0f}{%.0f} \cdot \frac{%.2f}{1.10}' % (self.lamb_p, self.lamb_r, self.vpl)))
                    doc.append(f"= {self.vrd:.2f}   \u00A0   kN")
            elif self.lambda_alma > self.lamb_r:
                with doc.create(Math()):
                    doc.append(NoEscape(r'V_{rd} = 1.24 \cdot \left(\frac{\lambda_p}{\lambda}\right)^2 \cdot \frac{V_{pl}}{1.10}'))
                    doc.append(NoEscape(r' = 1.24 \cdot \left(\frac{%.0f}{%.2f}\right)^2 \cdot \frac{%.2f}{1.10}' %(self.lamb_p, self.lambda_alma, self.vpl)))
                    doc.append(f"= {self.vrd:.2f}   \u00A0   kN")

        #Momento X----------------------------------------------------------------------------
        self.dlinha = self.momx.dlinha
        self.tw = self.momx.tw
        self.bf = self.momx.bf
        self.tf = self.momx.tf
        self.esb_alma = self.momx.esb_alma
        self.esb_lim_p_alma = self.momx.esb_lim_p_alma
        self.esb_lim_r_alma = self.momx.esb_lim_r_alma
        self.esb_mesa = self.momx.esb_mesa
        self.esb_lim_p_mesa = self.momx.esb_lim_p_mesa
        self.esb_lim_r_mesa = self.momx.esb_lim_r_mesa
        self.esb_flt = self.momx.esb_flt
        self.esb_lim_p_flt = self.momx.esb_lim_p_flt
        self.esb_lim_r_flt = self.momx.esb_lim_r_flt
        self.mrd_fla = self.momx.mrd_alma
        self.mrd_flm = self.momx.mrd_mesa
        self.mrd_flt = self.momx.mrd_flt
        self.mpl = self.momx.mpl
        self.mr_fla = self.momx.mr_fla
        self.mr = self.momx.mr
        self.zx = self.momx.zx
        self.wx = self.momx.wx
        self.fy = self.momx.fy
        self.e = self.momx.e
        self.lb = self.momx.lb
        self.ry = self.momx.ry
        self.b1 = self.momx.b1
        self.cb = self.momx.cb

        # Seção principal
        with doc.create(Section("Cálculo do Momento Fletor")):
            doc.append(f"")

        # Cálculo do momento fletor resistente
        with doc.create(Subsection("Cálculo do momento fletor resistente em X (Item D.2.1)")):
            doc.append("Momento fletor de plastificação: ")
            with doc.create(Math()):
                doc.append(NoEscape(r"M_{pl} = z_x \cdot f_y = %.2f \cdot %.2f = %.2f \  \text{kN} \cdot \text{cm}" % (self.zx, self.fy, self.mpl)))

            doc.append("Flambagem local da alma - FLA:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\lambda = \frac{d'}{t_w} = \frac{%.2f}{%.2f} " % (self.dlinha, self.tw)))
                doc.append(NoEscape(f"= {self.esb_alma:.2f} "))
            doc.append("Lambda P:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_p = 3.76 \cdot \sqrt{\frac{E}{f_y}} = 3.76 \cdot \sqrt{\frac{%.0f}{%.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_p_alma)))
            doc.append("Lambda R:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_r = 5.70 \cdot \sqrt{\frac{E}{f_y}} = 5.70 \cdot \sqrt{\frac{%.0f}{%.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_r_alma)))
            
            doc.append("Momento fletor resistente:")
            with doc.create(Math()):
                if self.esb_alma <= self.esb_lim_p_alma:
                    doc.append(NoEscape(r"M_{rd} = \frac{M_{pl}}{1.10} = \frac{%.2f}{1.10} = %.2f \  \text{kN} \cdot \text{cm}" % (self.mpl, self.mrd_fla)))
                else:
                    if self.esb_alma > self.esb_lim_p_alma and self.esb_alma <= self.esb_lim_r_alma:
                        doc.append(NoEscape(r"M_{rd} = \frac{1}{1.10} \cdot \left( M_{pl} - \left( M_{pl} - M_r \right) \cdot \frac{\lambda - \lambda_p}{\lambda_r - \lambda_p} \right)"))
                        doc.append(NoEscape(r" = \frac{1}{1.10} \cdot \left( %.2f - \left( %.2f - %.2f \right) \cdot \frac{%.2f - %.2f}{%.2f - %.2f} \right)" % (self.mpl, self.mpl, self.mr_fla, self.esb_alma, self.esb_lim_p_alma, self.esb_lim_r_alma, self.esb_lim_p_alma )))
                        doc.append(NoEscape(r" = %.2f \  \text{kN} \cdot \text{cm} " %(self.mrd_fla)))
                    else:
                        doc.append("Viga esbelta - Não aplicável a FLA")
            

            doc.append("Flambagem local da mesa - FLM:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\lambda = \frac{b_f}{2 \cdot t_f} = \frac{%.2f}{%.2f} " % (self.bf, self.tf)))
                doc.append(NoEscape(f"= {self.esb_mesa:.2f} ")) 
            doc.append("Lambda P:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_p = 0.38 \cdot \sqrt{\frac{E}{f_y}} = 0.38 \cdot \sqrt{\frac{%.0f}{%.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_p_mesa)))
            doc.append("Lambda R:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_r = 0.83 \cdot \sqrt{\frac{E}{0.7 \cdot f_y}} = 0.83 \cdot \sqrt{\frac{%.0f}{0.7 \cdot %.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_r_mesa)))
            
            doc.append("Momento fletor resistente:")
            with doc.create(Math()):
                if self.esb_mesa <= self.esb_lim_p_mesa:
                    doc.append(NoEscape(r"M_{rd} = \frac{M_{pl}}{1.10} = \frac{%.2f}{1.10} = %.2f \  \text{kN} \cdot \text{cm}" % (self.mpl, self.mrd_flm)))
                else:
                    if self.esb_mesa > self.esb_lim_p_mesa and self.esb_mesa <= self.esb_lim_r_mesa:
                        doc.append(NoEscape(r"M_{rd} = \frac{1}{1.10} \cdot \left( M_{pl} - \left( M_{pl} - M_r \right) \cdot \frac{\lambda - \lambda_p}{\lambda_r - \lambda_p} \right)"))
                        doc.append(NoEscape(r" = \frac{1}{1.10} \cdot \left( %.2f - \left( %.2f - %.2f \right) \cdot \frac{%.2f - %.2f}{%.2f - %.2f} \right)" % (self.mpl, self.mpl, self.mr, self.esb_mesa, self.esb_lim_p_mesa, self.esb_lim_r_mesa, self.esb_lim_p_mesa )))
                        doc.append(NoEscape(r" = %.2f \  \text{kN} \cdot \text{cm} " %(self.mrd_flm)))
                    else:
                        doc.append(NoEscape(r"M_{cr} = \frac{0.69 \cdot E \cdot w_x}{\lambda^2} = \frac{0.69 \cdot %.0f \cdot %.2f}{%.2f^2} = %.2f \  \text{kN} \cdot \text{cm}" % (self.e, self.wx, self.esb_mesa, self.mrd_flm)))

            doc.append("Flambagem lateral com torção - FLT:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\lambda = \frac{L_b}{r_y} = \frac{%.2f}{%.2f}" % (self.lb, self.ry)))
                doc.append(NoEscape(f"= {self.esb_flt:.2f} ")) 
            doc.append("Lambda P:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_p = 1.76 \cdot \sqrt{\frac{E}{f_y}} = 1.76 \cdot \sqrt{\frac{%.0f}{%.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_p_flt)))
            doc.append("Lambda R:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\beta_1 = \frac{ \left( f_y - \sigma_r \right) \cdot w_x}{E \cdot i_t} = \frac{ \left( %.2f - 0.3 \cdot %.2f \right) \cdot %.2f}{%.2f \cdot %.2f}' % (self.fy, self.fy, self.wx, self.e, self.it)))
                doc.append(NoEscape(f"= {self.b1:.2f} "))
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_r = \frac{1.38 \cdot C_b \sqrt{I_y \cdot I_t}}{r_y \cdot I_t \cdot \beta_1} \cdot \sqrt{1 + \sqrt{1 + \frac{27 \cdot C_w \cdot \beta_1^2}{C_b^2 \cdot I_y}}}' ))
                doc.append(NoEscape(r'= \frac{1.38 \cdot %.2f \sqrt{%.2f \cdot %.2f}}{%.2f \cdot %.2f \cdot %.2f} \cdot \sqrt{1 + \sqrt{1 + \frac{27 \cdot %.0f \cdot %.2f^2}{%.2f^2 \cdot %.2f}}}'%
                                                         (self.cb, self.iy, self.it, self.ry, self.it, self.b1, self.cw, self.b1, self.cb, self.iy ) ))
                doc.append(NoEscape(f"= {self.esb_lim_r_flt:.2f} "))

            doc.append("Momento fletor resistente:")
            with doc.create(Math()):
                if self.esb_flt <= self.esb_lim_p_flt:
                    doc.append(NoEscape(r"M_{rd} = \frac{M_{pl}}{1.10} = \frac{%.2f}{1.10} = %.2f \  \text{kN} \cdot \text{cm}" % (self.mpl, self.mrd_flt)))
                else:
                    if self.esb_flt > self.esb_lim_p_flt and self.esb_flt <= self.esb_lim_r_flt:
                        doc.append(NoEscape(r"M_{rd} = \frac{1}{1.10} \cdot \left( M_{pl} - \left( M_{pl} - M_r \right) \cdot \frac{\lambda - \lambda_p}{\lambda_r - \lambda_p} \right)"))
                        doc.append(NoEscape(r" = \frac{1}{1.10} \cdot \left( %.2f - \left( %.2f - %.2f \right) \cdot \frac{%.2f - %.2f}{%.2f - %.2f} \right)" % (self.mpl, self.mpl, self.mr, self.esb_flt, self.esb_lim_p_flt, self.esb_lim_r_flt, self.esb_lim_p_flt )))
                        doc.append(NoEscape(r" = %.2f \  \text{kN} \cdot \text{cm} " %(self.mrd_flt)))
                    else:
                        doc.append(NoEscape(r"M_{cr} = \frac{C_b \cdot \pi^2 \cdot E \cdot I_y}{L_b^2} \cdot \sqrt{ \frac{C_w}{I_y} \cdot \left( 1 + 0.0039 \cdot \frac {I_t \cdot L_b^2}{C_w}\right)}"))
                        doc.append(NoEscape(r"= \frac{%.2f \cdot \pi^2 \cdot %.2f \cdot %.2f}{%.2f^2} \cdot \sqrt{ \frac{%.0f}{%.2f} \cdot \left( 1 + 0.0039 \cdot \frac {%.2f \cdot %.2f^2}{%.0f}\right)}" %
                                                            (self.cb, self.e, self.iy, self.lb, self.cw, self.iy, self.it, self.lb, self.cw)))
                        doc.append(NoEscape(r" = %.2f \  \text{kN} \cdot \text{cm} " %(self.mrd_flt)))

        #Momento Y----------------------------------------------------------------------------
        self.dlinha = self.momy.dlinha
        self.tw = self.momy.tw
        self.bf = self.momy.bf
        self.tf = self.momy.tf
        self.esb_alma = self.momy.esb_alma
        self.esb_lim_p_alma = self.momy.esb_lim_p_alma
        self.esb_lim_r_alma = self.momy.esb_lim_r_alma
        self.esb_mesa = self.momy.esb_mesa
        self.esb_lim_p_mesa = self.momy.esb_lim_p_mesa
        self.esb_lim_r_mesa = self.momy.esb_lim_r_mesa
        self.mrd_fla = self.momy.mrd_alma
        self.mrd_flm = self.momy.mrd_mesa
        self.mpl = self.momy.mpl
        self.mr = self.momy.mr
        self.mr_fla = self.momy.mr_fla
        self.wy = self.momy.wy
        self.fy = self.momy.fy
        self.e = self.momy.e
        self.ry = self.momy.ry
        self.cb = self.momy.cb
        self.mom_cr_fla = self.momy.mom_cr_fla

        # Cálculo do momento fletor resistente
        with doc.create(Subsection("Cálculo do momento fletor resistente em Y (Item D.2.1)")):

            doc.append("Flambagem local da alma - FLA:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\lambda = \frac{d'}{t_w} = \frac{%.2f}{%.2f} " % (self.dlinha, self.tw)))
                doc.append(NoEscape(f"= {self.esb_alma:.2f} "))
            doc.append("Lambda P:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_p = 1.12 \cdot \sqrt{\frac{E}{f_y}} = 1.12 \cdot \sqrt{\frac{%.0f}{%.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_p_alma)))
            doc.append("Lambda R:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_r = 1.40 \cdot \sqrt{\frac{E}{f_y}} = 1.40 \cdot \sqrt{\frac{%.0f}{%.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_r_alma)))
            
            doc.append("Momento fletor resistente:")
            with doc.create(Math()):
                if self.esb_alma <= self.esb_lim_p_alma:
                    doc.append(NoEscape(r"M_{rd} = \frac{M_{pl}}{1.10} = \frac{%.2f}{1.10} = %.2f \  \text{kN} \cdot \text{cm}" % (self.mpl, self.mrd_fla)))
                else:
                    if self.esb_alma > self.esb_lim_p_alma and self.esb_alma <= self.esb_lim_r_alma:
                        doc.append(NoEscape(r"M_{rd} = \frac{1}{1.10} \cdot \left( M_{pl} - \left( M_{pl} - M_r \right) \cdot \frac{\lambda - \lambda_p}{\lambda_r - \lambda_p} \right)"))
                        doc.append(NoEscape(r" = \frac{1}{1.10} \cdot \left( %.2f - \left( %.2f - %.2f \right) \cdot \frac{%.2f - %.2f}{%.2f - %.2f} \right)" % (self.mpl, self.mpl, self.mr_fla, self.esb_alma, self.esb_lim_p_alma, self.esb_lim_r_alma, self.esb_lim_p_alma )))
                        doc.append(NoEscape(r" = %.2f \  \text{kN} \cdot \text{cm} " %(self.mrd_fla)))
                    else:
                        doc.append(NoEscape(r"M_{cr} = W_y \cdot f_y = %.2f \cdot %.2f = %.2f \  \text{kN} \cdot \text{cm}" % (self.wy, self.fy, self.mom_cr_fla)))
            

            doc.append("Flambagem local da mesa - FLM:")
            with doc.create(Math()):
                doc.append(NoEscape(r"\lambda = \frac{b_f}{2 \cdot t_f} = \frac{%.2f}{%.2f} " % (self.bf, self.tf)))
                doc.append(NoEscape(f"= {self.esb_mesa:.2f} ")) 
            doc.append("Lambda P:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_p = 0.38 \cdot \sqrt{\frac{E}{f_y}} = 0.38 \cdot \sqrt{\frac{%.0f}{%.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_p_mesa)))
            doc.append("Lambda R:")
            with doc.create(Math()):
                doc.append(NoEscape(r'\lambda_r = 0.83 \cdot \sqrt{\frac{E}{0.7 \cdot f_y}} = 0.83 \cdot \sqrt{\frac{%.0f}{0.7 \cdot %.2f}} = %.2f' % (self.e, self.fy, self.esb_lim_r_mesa)))
            
            doc.append("Momento fletor resistente:")
            with doc.create(Math()):
                if self.esb_mesa <= self.esb_lim_p_mesa:
                    doc.append(NoEscape(r"M_{rd} = \frac{M_{pl}}{1.10} = \frac{%.2f}{1.10} = %.2f \  \text{kN} \cdot \text{cm}" % (self.mpl, self.mrd_flm)))
                else:
                    if self.esb_mesa > self.esb_lim_p_mesa and self.esb_mesa <= self.esb_lim_r_mesa:
                        doc.append(NoEscape(r"M_{rd} = \frac{1}{1.10} \cdot \left( M_{pl} - \left( M_{pl} - M_r \right) \cdot \frac{\lambda - \lambda_p}{\lambda_r - \lambda_p} \right)"))
                        doc.append(NoEscape(r" = \frac{1}{1.10} \cdot \left( %.2f - \left( %.2f - %.2f \right) \cdot \frac{%.2f - %.2f}{%.2f - %.2f} \right)" % (self.mpl, self.mpl, self.mr, self.esb_mesa, self.esb_lim_p_mesa, self.esb_lim_r_mesa, self.esb_lim_p_mesa )))
                        doc.append(NoEscape(r" = %.2f \  \text{kN} \cdot \text{cm} " %(self.mrd_flm)))
                    else:
                        doc.append(NoEscape(r"M_{cr} = \frac{0.69 \cdot E \cdot w_x}{\lambda^2} = \frac{0.69 \cdot %.0f \cdot %.2f}{%.2f^2} = %.2f \  \text{kN} \cdot \text{cm}" % (self.e, self.wx, self.esb_mesa, self.mrd_flm)))

 

        # Gerar o PDF
        doc.generate_pdf("memorial", clean_tex=False)
        messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")

def main():
    app = Principal()
    #app.wm_attributes('-toolwindow', 'True')
    app.mainloop()


if __name__ == "__main__":
    main()


