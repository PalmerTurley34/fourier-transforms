import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyparsing import col
import ttkbootstrap as ttk
from ttkbootstrap.constants import TOP, BOTH, YES, SUCCESS, WARNING, OUTLINE, NSEW

matplotlib.use('TkAgg')
plt.style.use('dark_background')

class FourierVisuals:
    def __init__(self, master: ttk.Window) -> None:
        self.master = master
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        self.buttons = ttk.Frame(self.master)
        self.buttons.pack(side=ttk.TOP)
        self.figure = plt.figure()
        self.sine_ax = self.figure.add_subplot(2,1,1)
        self.fft_ax = self.figure.add_subplot(2,1,2)
        self.plot_frame = FigureCanvasTkAgg(self.figure, self.master)
        self.plot_frame.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)

        self.start_button = ttk.Button(self.buttons, text='Start!', command=self.draw_data, bootstyle=(OUTLINE, SUCCESS))
        self.start_button.grid(row=0, column=0, rowspan=3, sticky=NSEW, padx=10, pady=3)
        self.freq_frame = ttk.Labelframe(self.buttons, text='Frequecies', bootstyle=WARNING)
        self.freq_frame.grid(row=0, column=1, rowspan=3)
        num_freq = 20
        self.frequencies_selected = [ttk.BooleanVar() for _ in range(num_freq)]
        for freq in range(num_freq):
            check_button = ttk.Checkbutton(self.freq_frame, variable=self.frequencies_selected[freq], text=f'{freq+1} Hz')
            check_button.grid(row=freq//5, column=freq%5, padx=4, pady=2)

    def draw_data(self):
        pass


    def close(self):
        self.master.quit()
        self.master.destroy()

def main():
    window = ttk.Window(
        title='Fourier Transforms',
        themename='darkly',
        size=(1300, 900)
    )
    app = FourierVisuals(window)
    window.mainloop()

if __name__ == '__main__':
    main()