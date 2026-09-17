// MainWindow.xaml.cs  .  145065 Unit 7  .  ShiftTally
//
// The code-behind: the other half of MainWindow. MainWindow.xaml and this
// file are two parts of ONE class ("partial"). The build turns the XAML into
// C# that creates every control and a field for every x:Name.
//
// Lab U07-01 writes no code here. Lab U07-02 adds the event handlers.

using System.Windows;

namespace ShiftTally;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        // Builds every object described in MainWindow.xaml. Remove this line
        // and every x:Name field stays null.
        InitializeComponent();
    }
}
