from math import exp
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import time

matplotlib.use('TkAgg')
plt.style.use('dark_background')

class RealTimeFourierVisuals:
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
            # self.fft_ax.plot(self.fft_x, self.fft_y.real)
            # self.fft_ax.plot(self.fft_x, self.fft_y.imag)
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

class FourierVisuals:
    def __init__(self, master: ttk.Window):
        self.master  = master
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        for row in range(2):
            self.master.rowconfigure(row, weight=2)
        self.master.rowconfigure(2, weight=3)
        num_cols = 6
        for col in range(num_cols):
            self.master.columnconfigure(col, weight=1)

        self.freq_vars = [ttk.DoubleVar(value=1.0) for _ in range(4)]
        self.phase_vars = [ttk.DoubleVar(value=0.0) for _ in range(4)]
        self.amp_vars = [ttk.DoubleVar(value=1.0) for _ in range(4)]
        self.sine_x = np.linspace(0, 2*np.pi, 512)
        self.sine_waves = []
        self.line_data = []
        self.canvases = []

        for i, (row, col) in enumerate([(0 ,0), (0, num_cols//2), (1, 0), (1, num_cols//2)]):
            sine_frame = ttk.Frame(self.master)
            sine_frame.grid(row=row, column=col, columnspan=num_cols//2, sticky=NSEW)
            self.create_sine_wave_frame(sine_frame, i)

        wrap_frame = ttk.Frame(self.master, bootstyle=SUCCESS)
        wrap_frame.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        fig = plt.figure()
        self.wrap_ax = fig.add_subplot(1,1,1)
        self.wrap_ax.set_xlim((-6, 6))
        self.wrap_ax.set_ylim((-6, 6))
        self.wrap_ax.set_aspect('equal')
        self.wrap_canvas = FigureCanvasTkAgg(fig, wrap_frame)
        widget = self.wrap_canvas.get_tk_widget()
        widget.pack(side=LEFT, fill=BOTH, expand=YES)

        wrap_slider_frame = ttk.Labelframe(wrap_frame, text='Freq', labelanchor='n', bootstyle=WARNING)
        wrap_slider_frame.pack(side=LEFT, fill=Y)
        ttk.Label(wrap_slider_frame, text='10 Hz').pack(side=TOP, pady=2)
        self.wrap_freq_var = ttk.DoubleVar(value=1.0)
        wrap_freq_slider = ttk.Scale(wrap_slider_frame, orient=VERTICAL, variable=self.wrap_freq_var, from_=10.0, to=0.0, command=self.update_wrap_graph)
        wrap_freq_slider.pack(side=TOP, expand=YES, fill=Y)
        ttk.Label(wrap_slider_frame, text='0 Hz').pack(side=TOP, pady=2)
        self.sum_of_waves = np.sum(self.sine_waves, axis=0)
        fft_step = self.sum_of_waves * np.exp(-2j * np.pi * self.wrap_freq_var.get() * np.arange(512) / 512)
        self.wrap_line = self.wrap_ax.plot(fft_step.real, fft_step.imag)[0]
        
        fft_frame = ttk.Frame(self.master, bootstyle=WARNING)
        fft_frame.grid(row=2, column=2, columnspan=4, sticky=NSEW)

    def create_sine_wave_frame(self, master: ttk.Frame, index: int):
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=5)
        num_cols = 16
        for col in range(num_cols):
            master.columnconfigure(col, weight=1)

        freq_var = self.freq_vars[index]
        phs_var = self.phase_vars[index]
        amp_var = self.amp_vars[index]

        freq_frame = ttk.Labelframe(master, labelanchor='nw', text='Frequency', bootstyle=(WARNING))
        freq_frame.grid(row=0, column=0, columnspan=num_cols//2, sticky=NSEW, padx=5)
        ttk.Label(freq_frame, text='0 Hz').pack(side=LEFT, fill=Y, padx=2)
        freq_slider = ttk.Scale(freq_frame, orient=HORIZONTAL, variable=freq_var, from_=0.0, to=10.0, command=lambda x: self.update_sine_wave(index))
        freq_slider.pack(side=LEFT, fill=BOTH, expand=YES)
        ttk.Label(freq_frame, text='10 Hz').pack(side=LEFT, fill=Y, padx=2)

        phase_frame = ttk.Labelframe(master, labelanchor='nw', text='Phase', bootstyle=WARNING)
        phase_frame.grid(row=0, column=num_cols//2, columnspan=num_cols//2, sticky=NSEW, padx=5)
        ttk.Label(phase_frame, text='0 Pi').pack(side=LEFT, fill=Y, padx=2)
        phase_slider = ttk.Scale(phase_frame, orient=HORIZONTAL, variable=phs_var, from_=0.0, to=2*np.pi, command=lambda x: self.update_sine_wave(index))
        phase_slider.pack(side=LEFT, fill=BOTH, expand=YES)
        ttk.Label(phase_frame, text='2 Pi').pack(side=LEFT, fill=Y, padx=2)

        amp_frame = ttk.LabelFrame(master, labelanchor='n', text='Amp', bootstyle=WARNING)
        amp_frame.grid(row=1, column=num_cols-1, sticky=NSEW, padx=5)
        ttk.Label(amp_frame, text='5').pack(side=TOP, pady=2)
        amp_slider = ttk.Scale(amp_frame, orient=VERTICAL, variable=amp_var, from_=5.0, to=0.0001, command=lambda x: self.update_sine_wave(index))
        amp_slider.pack(side=TOP, expand=YES, fill=BOTH)
        ttk.Label(amp_frame, text='0').pack(side=TOP, pady=2)

        plot_frame = ttk.Frame(master)
        plot_frame.grid(row=1, column=0, columnspan=num_cols-1, sticky=NSEW)
        fig = plt.figure()
        canvas = FigureCanvasTkAgg(fig, plot_frame)
        widget = canvas.get_tk_widget()
        widget.pack(fill=BOTH, expand=TRUE)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_ylim((-6, 6))
        sine_wave = amp_var.get() * np.sin(freq_var.get() * self.sine_x + phs_var.get())
        line = ax.plot(self.sine_x, sine_wave)
        line = line[0]
        self.canvases.append(canvas)
        self.line_data.append(line)
        self.sine_waves.append(sine_wave)

    def update_sine_wave(self, index):
        line = self.line_data[index]
        amp_var = self.amp_vars[index]
        freq_var = self.freq_vars[index]
        phs_var = self.phase_vars[index]

        new_sine_wave = amp_var.get() * np.sin(freq_var.get() * self.sine_x + phs_var.get())
        line.set_ydata(new_sine_wave)
        self.sine_waves[index] = new_sine_wave

        canvas: FigureCanvasTkAgg = self.canvases[index]
        self.update_wrap_graph()
        canvas.draw()
        self.wrap_canvas.flush_events()
        canvas.flush_events()

    def update_wrap_graph(self, value=None):
        self.sum_of_waves = np.sum(self.sine_waves, axis=0)
        fft_step = self.sum_of_waves * np.exp(-2j * np.pi * self.wrap_freq_var.get() * np.arange(512) / 512)
        self.wrap_line.set_ydata(fft_step.imag)
        self.wrap_line.set_xdata(fft_step.real)
        self.wrap_canvas.draw()
        # self.wrap_canvas.flush_events()

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