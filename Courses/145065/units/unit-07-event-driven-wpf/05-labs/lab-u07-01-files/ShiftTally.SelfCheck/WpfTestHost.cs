// WpfTestHost.cs  .  145065 Unit 7  .  self-check helper
//
// You do not need to change this file. Read it once, because it shows two
// rules of WPF that the labs depend on.
//
// Rule 1: a WPF object belongs to the thread that created it, and that thread
// must be an STA thread. xunit runs tests on other threads, so every check
// creates its own STA thread, builds the window there, and runs there.
//
// Rule 2: in a running app, a handler runs inside WPF's event loop, and an
// "await" inside it comes back to the same thread. The line that sets the
// SynchronizationContext gives the tests that same arrangement.

using System.IO;
using System.Reflection;
using System.Runtime.ExceptionServices;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;

// One window at a time. WPF keeps some shared state while it loads XAML, and
// two STA threads loading windows at once can break each other. The binding
// error listener is shared too. Running the checks in order avoids both.
[assembly: CollectionBehavior(DisableTestParallelization = true)]

namespace ShiftTally.SelfCheck;

internal static class WpfTestHost
{
    public const int Width = 900;
    public const int Height = 600;

    /// <summary>Builds a MainWindow on an STA thread, lays it out, and runs the check.</summary>
    public static void Run(Action<MainWindow> check)
    {
        Exception? failure = null;
        Thread sta = new(() =>
        {
            SynchronizationContext.SetSynchronizationContext(
                new DispatcherSynchronizationContext(Dispatcher.CurrentDispatcher));
            MainWindow? window = null;
            try
            {
                window = new MainWindow();
                LayOut(window);
                check(window);
            }
            catch (Exception problem)
            {
                failure = problem;
            }
            finally
            {
                window?.Close();
                Dispatcher.CurrentDispatcher.InvokeShutdown();
            }
        });
        sta.SetApartmentState(ApartmentState.STA);
        sta.Start();
        sta.Join();

        if (failure is not null)
        {
            ExceptionDispatchInfo.Capture(failure).Throw();
        }
    }

    /// <summary>Sizes the window's content as if the window were open at 900 by 600.</summary>
    public static void LayOut(Window window)
    {
        FrameworkElement root = (FrameworkElement)window.Content;
        root.Measure(new Size(Width, Height));
        root.Arrange(new Rect(0, 0, Width, Height));
        root.UpdateLayout();
    }

    /// <summary>Finds a control by its x:Name, with a message that says what to fix.</summary>
    public static T Find<T>(Window window, string name) where T : FrameworkElement
    {
        object? found = window.FindName(name);
        Assert.True(found is not null, $"No control named {name}. Check the x:Name in MainWindow.xaml.");
        Assert.True(found is T, $"{name} is a {found!.GetType().Name}, but the lab asks for a {typeof(T).Name}.");
        return (T)found;
    }

    /// <summary>Where a control sits inside the window, in pixels.</summary>
    public static Rect BoundsOf(Window window, FrameworkElement element)
    {
        FrameworkElement root = (FrameworkElement)window.Content;
        Point topLeft = element.TranslatePoint(new Point(0, 0), root);
        return new Rect(topLeft, new Size(element.ActualWidth, element.ActualHeight));
    }

    /// <summary>
    /// Presses a button the way a mouse does. WPF's own OnClick method raises
    /// the Click event (every attached handler runs) and then runs the button's
    /// Command, if it has one. OnClick is protected, so the check reaches it
    /// by reflection.
    /// </summary>
    public static void Click(Button button)
    {
        Assert.True(button.IsEnabled, $"{button.Name} is disabled, so an operator could not press it.");
        OnClick.Invoke(button, null);
    }

    private static readonly MethodInfo OnClick =
        typeof(ButtonBase).GetMethod("OnClick", BindingFlags.Instance | BindingFlags.NonPublic)
        ?? throw new InvalidOperationException("ButtonBase.OnClick was not found.");

    /// <summary>Lets WPF's event loop run until the condition is true or time runs out.</summary>
    public static bool PumpUntil(Func<bool> done, TimeSpan timeout)
    {
        DateTime giveUpAt = DateTime.UtcNow + timeout;
        DispatcherFrame frame = new();
        DispatcherTimer timer = new(TimeSpan.FromMilliseconds(20), DispatcherPriority.Background,
            (_, _) =>
            {
                if (done() || DateTime.UtcNow > giveUpAt)
                {
                    frame.Continue = false;
                }
            },
            Dispatcher.CurrentDispatcher);
        timer.Start();
        Dispatcher.PushFrame(frame);
        timer.Stop();
        return done();
    }

    /// <summary>
    /// Saves a picture of the window's content, so you can look at your layout
    /// without opening the app. Returns where the file went.
    /// </summary>
    public static string SavePicture(Window window, string fileName)
    {
        // A window that was never shown does not draw itself, so draw its content.
        // The content gets the window's DataContext BEFORE it is detached. The
        // value never changes, so WPF does not re-read the bindings, and the
        // picture shows exactly what the screen showed, stale values included.
        FrameworkElement content = (FrameworkElement)window.Content;
        content.DataContext = window.DataContext;
        window.Content = null;
        content.Measure(new Size(Width, Height));
        content.Arrange(new Rect(0, 0, Width, Height));
        content.UpdateLayout();
        Dispatcher.CurrentDispatcher.Invoke(() => { }, DispatcherPriority.ContextIdle);

        RenderTargetBitmap bitmap = new(Width, Height, 96, 96, PixelFormats.Pbgra32);
        bitmap.Render(content);
        PngBitmapEncoder encoder = new();
        encoder.Frames.Add(BitmapFrame.Create(bitmap));

        string folder = Path.Combine(AppContext.BaseDirectory, "window-pictures");
        Directory.CreateDirectory(folder);
        string path = Path.Combine(folder, fileName);
        using (FileStream file = File.Create(path))
        {
            encoder.Save(file);
        }

        window.Content = content;
        return path;
    }
}
