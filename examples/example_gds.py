from utilities.set_paths import SetPaths  # noqa: F401
import gpype as gp


if __name__ == '__main__':

    # create app and pipeline
    app = gp.MainApp()
    p = gp.Pipeline()

    # g.Nautilus
    gds = gp.GDSSource(sampling_rate=250,
                       channel_count=8)

    # 2-30 Hz
    b = [0.0815,         0,   -0.1630,         0,    0.0815]  # noqa: E241
    a = [1.0000,   -2.9862,    3.3702,   -1.7553,    0.3722]  # noqa: E241
    f1 = gp.LTIFilter(b=b, a=a)

    # 50 Hz notch
    b = [0.925417400953572, 0, 0, 0, 0, -0.925417400953572]
    a = [1, 0, 0, 0, 0, -0.850834801907143]
    f2 = gp.LTIFilter(b=b, a=a)

    scope = gp.TimeSeriesScope(amplitude_limit=100,
                               time_window=10)
    sink = gp.FileSink(file_name='test.csv')

    app.add_widget(scope)
    p.connect(gds, f1)
    p.connect(f1, f2)
    p.connect(f2, scope)
    p.connect(f2, sink)
    p.start()
    app.run()
    p.stop()
