// COPIED from the course's HMI anchor, panel/Line3.Hmi.Snapshots/Program.cs,
// without the Week 13 app. Given to you. It renders YOUR PanelView.
//
// Program.cs  .  145065 HMI anchor  .  Line3.Hmi.Snapshots
//
// Builds the panel's view model from scripted poll results on a fixed clock,
// renders PanelView for each scene, and saves a PNG per scene. The scenes are
// the four states the course defines, plus the confirmation dialog and a
// single dropped sensor. The dates below are invented sample data.
//
//   dotnet run --project Line3.Hmi.Snapshots -- ..\docs\screens
//
// It reads the thresholds.json next to the panel, so your team's limits and
// reasons are the ones on screen. Read every PNG it writes: a PNG is evidence
// the XAML lays out, not proof that a gloved finger can press the button.

using System.Globalization;
using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;
using Line3.Hmi.Core;
using Line3.Hmi.Core.ViewModels;
using Line3.Hmi.Panel;

namespace Line3.Hmi.Snapshots;

public static class Program
{
    private static readonly DateTimeOffset T0 = new(2027, 1, 11, 14, 3, 22, TimeSpan.Zero);

    public static int Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.Error.WriteLine("Usage: Line3.Hmi.Snapshots <output folder>");
            return 2;
        }

        string output = Path.GetFullPath(args[0]);
        Directory.CreateDirectory(output);

        Exception? failure = null;
        Thread sta = new(() =>
        {
            try
            {
                RenderAll(output);
            }
            catch (Exception problem)
            {
                failure = problem;
            }
        });
        sta.SetApartmentState(ApartmentState.STA);
        sta.Start();
        sta.Join();

        if (failure is not null)
        {
            Console.Error.WriteLine(failure);
            return 1;
        }

        return 0;
    }

    private static void RenderAll(string output)
    {
        PanelConfig config = PanelConfig.Load(Path.Combine(AppContext.BaseDirectory, "thresholds.json"));

        Save(Scene(config, Normal), output, "panel-normal.png");
        Save(Scene(config, Alarm), output, "panel-alarm.png");
        Save(Scene(config, AlarmConfirm), output, "panel-alarm-confirm.png");
        Save(Scene(config, Stale), output, "panel-stale.png");
        Save(Scene(config, MissingConnection), output, "panel-missing-connection.png");
        Save(Scene(config, MissingOneSensor), output, "panel-missing-one-sensor.png");
    }

    // ---- scenes ------------------------------------------------------------

    private delegate void Script(PanelViewModel panel, ManualClock clock);

    private static FrameworkElement Scene(PanelConfig config, Script script)
    {
        ManualClock clock = new(T0);
        PanelViewModel panel = new(config, clock, TimeZoneInfo.Utc);
        script(panel, clock);
        return new PanelView { DataContext = panel };
    }

    private static void Normal(PanelViewModel panel, ManualClock clock)
    {
        long sequence = 1040;
        for (int i = 0; i < 3; i++)
        {
            Poll(panel, clock, sequence++, 212.0 + (i * 0.2), 3.1, 68.0);
        }

        clock.Advance(TimeSpan.FromMilliseconds(400));
        panel.Refresh();
    }

    private static void Alarm(PanelViewModel panel, ManualClock clock)
    {
        long sequence = 1040;
        double oven = 224.0;
        for (int i = 0; i < 7; i++)
        {
            Poll(panel, clock, sequence++, oven, 3.2, 67.8);
            oven += 2.0;
        }

        clock.Advance(TimeSpan.FromMilliseconds(300));
        panel.Refresh();
    }

    private static void AlarmConfirm(PanelViewModel panel, ManualClock clock)
    {
        Alarm(panel, clock);
        panel.RequestAcknowledge(panel.Tiles.First(t => t.Id == "oven-temp"));
    }

    private static void Stale(PanelViewModel panel, ManualClock clock)
    {
        // The oven went into alarm, then the Pi froze: same sample for 12 s.
        long sequence = 1040;
        Poll(panel, clock, sequence++, 226.0, 3.1, 68.0);
        Poll(panel, clock, sequence, 234.4, 3.1, 68.0);
        DateTimeOffset frozenAt = clock.UtcNow;
        for (int i = 0; i < 12; i++)
        {
            clock.Advance(TimeSpan.FromSeconds(1));
            panel.ReceiveResult(PollResult.Success(Snapshot(sequence, frozenAt, 234.4, 3.1, 68.0), clock.UtcNow));
        }
    }

    private static void MissingConnection(PanelViewModel panel, ManualClock clock)
    {
        // The oven alarmed and was acknowledged. Then the cable was pulled.
        long sequence = 1040;
        Poll(panel, clock, sequence++, 212.0, 3.1, 68.0);
        Poll(panel, clock, sequence++, 233.0, 3.1, 68.0);
        panel.RequestAcknowledge(panel.Tiles.First(t => t.Id == "oven-temp"));
        panel.ConfirmAcknowledge();
        for (int i = 0; i < 8; i++)
        {
            clock.Advance(TimeSpan.FromSeconds(1));
            panel.ReceiveResult(PollResult.Failed(PollFailure.Timeout, "no answer within 1.5 s", clock.UtcNow));
        }
    }

    private static void MissingOneSensor(PanelViewModel panel, ManualClock clock)
    {
        long sequence = 1040;
        Poll(panel, clock, sequence++, 212.2, 3.1, 68.0);
        Poll(panel, clock, sequence++, 212.4, null, 68.0);
        Poll(panel, clock, sequence, 212.3, null, 67.9);
        clock.Advance(TimeSpan.FromMilliseconds(300));
        panel.Refresh();
    }

    private static void Poll(PanelViewModel panel, ManualClock clock, long sequence,
                             double? oven, double? vibration, double? coolant)
    {
        clock.Advance(TimeSpan.FromSeconds(1));
        DateTimeOffset sampled = clock.UtcNow.AddMilliseconds(-200);
        panel.ReceiveResult(PollResult.Success(Snapshot(sequence, sampled, oven, vibration, coolant), clock.UtcNow));
    }

    private static ReadingSnapshot Snapshot(long sequence, DateTimeOffset sampledAt,
                                            double? oven, double? vibration, double? coolant)
    {
        static string Sensor(string id, string kind, string unit, double? value) => value is double v
            ? $"{{\"id\":\"{id}\",\"kind\":\"{kind}\",\"value\":{v.ToString(CultureInfo.InvariantCulture)},\"unit\":\"{unit}\",\"ok\":true}}"
            : $"{{\"id\":\"{id}\",\"kind\":\"{kind}\",\"value\":null,\"unit\":\"{unit}\",\"ok\":false}}";

        string json = "{\"device\":\"line3-pi\",\"sequence\":" + sequence
            + ",\"sampled_at\":\"" + sampledAt.UtcDateTime.ToString("yyyy-MM-dd'T'HH:mm:ss.fff'Z'", CultureInfo.InvariantCulture)
            + "\",\"sensors\":[" + Sensor("oven-temp", "temperature", "C", oven) + ","
            + Sensor("press-vibration", "vibration", "mm/s", vibration) + ","
            + Sensor("coolant-level", "level", "%", coolant) + "]}";
        ParseResult parsed = ReadingParser.Parse(json);
        return parsed.Snapshot ?? throw new InvalidOperationException(parsed.Error);
    }

    // ---- rendering -----------------------------------------------------------

    private static void Save(FrameworkElement element, string folder, string name, int width = 1280, int height = 800)
    {
        element.Measure(new Size(width, height));
        element.Arrange(new Rect(0, 0, width, height));
        element.UpdateLayout();

        // Let data binding and item generation finish before drawing.
        Dispatcher.CurrentDispatcher.Invoke(() => { }, DispatcherPriority.ContextIdle);
        element.UpdateLayout();

        RenderTargetBitmap bitmap = new(width, height, 96, 96, PixelFormats.Pbgra32);
        bitmap.Render(element);
        PngBitmapEncoder encoder = new();
        encoder.Frames.Add(BitmapFrame.Create(bitmap));
        string path = Path.Combine(folder, name);
        using (FileStream file = File.Create(path))
        {
            encoder.Save(file);
        }

        Console.WriteLine($"wrote {path} ({new FileInfo(path).Length} bytes)");
    }
}
