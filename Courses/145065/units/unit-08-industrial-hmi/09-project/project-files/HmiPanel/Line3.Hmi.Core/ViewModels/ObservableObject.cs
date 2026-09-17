// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core/ViewModels/ObservableObject.cs.
// Given to you. Read it; you do not need to change it.
//
// ObservableObject.cs  .  145065 HMI anchor  .  Line3.Hmi.Core.ViewModels
//
// The piece that makes data binding work. When a property changes, the view
// model raises PropertyChanged with the property's name, and WPF re-reads
// that one binding. Forget to raise it and the screen keeps showing the old
// value while the object holds the new one: a bug that does not crash.

using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

namespace Line3.Hmi.Core.ViewModels;

public abstract class ObservableObject : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value))
        {
            return false;
        }

        field = value;
        OnPropertyChanged(name);
        return true;
    }

    protected void OnPropertyChanged([CallerMemberName] string? name = null) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}

/// <summary>A button's action and whether it is allowed right now.</summary>
public sealed class RelayCommand : ICommand
{
    private readonly Action execute;
    private readonly Func<bool> canExecute;

    public RelayCommand(Action execute, Func<bool>? canExecute = null)
    {
        this.execute = execute;
        this.canExecute = canExecute ?? (() => true);
    }

    public event EventHandler? CanExecuteChanged;

    public bool CanExecute(object? parameter) => canExecute();

    public void Execute(object? parameter)
    {
        // A button can be pressed in the instant between the state changing and
        // the button greying out. Check again rather than trusting the screen.
        if (canExecute())
        {
            execute();
        }
    }

    public void RaiseCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}
