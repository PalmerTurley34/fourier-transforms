import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
from ttkbootstrap.constants import TOP, BOTH, YES, SUCCESS, WARNING, OUTLINE, NSEW
import time

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
        self.frequencies_selected = [ttk.BooleanVar(value=False) for _ in range(num_freq)]
        self.active_frequencies = []
        for freq in range(num_freq):
            check_button = ttk.Checkbutton(
                self.freq_frame, 
                variable=self.frequencies_selected[freq], 
                text=f'{freq+1} Hz',
                onvalue=True,
                offvalue=False, 
                command=self.update_active_frequencies)
            check_button.grid(row=freq//5, column=freq%5, padx=4, pady=2)
        self.frequencies_selected[0].set(True)
        self.update_active_frequencies()

        self.x_data = np.linspace(0, 20*np.pi, 1024)
        self.x_axis_data = self.x_data.copy()
        self.y_data = np.zeros(self.x_data.shape)
        self.fft_x = np.fft.rfftfreq(1024, (self.x_data[1]-self.x_data[0])/(2*np.pi))
        self.fft_y = np.fft.rfft(self.y_data, 1024)

    def update_data(self):
        shift_by = 15
        self.y_data = np.roll(self.y_data, -shift_by)
        new_data = np.zeros(shift_by)
        for freq in self.active_frequencies:
            new_data += np.sin(freq * self.x_data[-shift_by:])
        self.y_data[-shift_by:] = new_data
        self.x_data = np.roll(self.x_data, -shift_by)
        # self.fft_y = np.abs(np.fft.rfft(self.y_data, 1024))
        self.fft_y = np.fft.rfft(self.y_data, 1024)

    def draw_data(self):
        self.running = True
        while self.running:
            self.update_data()
            self.sine_ax.cla()
            self.sine_ax.plot(self.x_axis_data, self.y_data)
            self.fft_ax.cla()
            self.fft_ax.plot(self.fft_x, self.fft_y.real)
            self.fft_ax.plot(self.fft_x, self.fft_y.imag)
            self.fft_ax.plot(self.fft_x, np.abs(self.fft_y))
            self.plot_frame.draw()
            self.plot_frame.flush_events()
            time.sleep(0.05)

    def update_active_frequencies(self):
        selected = [int(state.get()) for state in self.frequencies_selected]
        frequencies = [0] + [i+1 for i in np.nonzero(selected)[0]]
        self.active_frequencies = frequencies

    def close(self):
        self.running = False
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