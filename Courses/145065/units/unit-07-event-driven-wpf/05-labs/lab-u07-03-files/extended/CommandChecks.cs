// CommandChecks.cs  .  145065 Unit 7  .  Lab U07-03 EXTENDED
//
// These checks are for the EXTENDED option only. Copy this file into your
// ShiftTally.SelfCheck folder, next to BindingChecks.cs, then run dotnet test.
// While it sits in this "extended" folder, nothing compiles it.
//
// Until TallyViewModel has AddGoodCommand, AddScrapCommand, and UndoCommand,
// this file does not compile. Read the compiler's message: it names exactly
// what is missing.

using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Input;
using ShiftTally.Core;

namespace ShiftTally.SelfCheck;

public class CommandChecks
{
    [Theory]
    [InlineData("GoodButton")]
    [InlineData("ScrapButton")]
    [InlineData("UndoButton")]
    public void TheCountingButtonsUseCommands(string name)
    {
        WpfTestHost.Run(w =>
        {
            Button button = WpfTestHost.Find<Button>(w, name);
            Assert.True(BindingOperations.IsDataBound(button, ButtonBase.CommandProperty),
                $"{name}.Command is not bound to a command on TallyViewModel.");
        });
    }

    [Fact]
    public void UndoIsOnlyAllowedWhenThereIsSomethingToUndo()
    {
        TallyViewModel tally = new();
        int announced = 0;
        tally.UndoCommand.CanExecuteChanged += (_, _) => announced++;

        Assert.False(tally.UndoCommand.CanExecute(null));
        tally.AddGoodCommand.Execute(null);
        Assert.True(tally.UndoCommand.CanExecute(null));
        Assert.True(announced > 0, "UndoCommand never raised CanExecuteChanged, so the button would stay grey.");

        tally.UndoCommand.Execute(null);
        Assert.Equal(0, tally.Good);
        Assert.False(tally.UndoCommand.CanExecute(null));
    }

    [Fact]
    public void TheButtonGreysOutWhenUndoIsNotAllowed()
    {
        WpfTestHost.Run(w =>
        {
            Button undo = WpfTestHost.Find<Button>(w, "UndoButton");
            Assert.False(undo.IsEnabled);
            WpfTestHost.Click(WpfTestHost.Find<Button>(w, "ScrapButton"));
            Assert.True(undo.IsEnabled);
        });
    }

    [Theory]
    [InlineData(Key.F2, ModifierKeys.None, "AddGoodCommand")]
    [InlineData(Key.F3, ModifierKeys.None, "AddScrapCommand")]
    [InlineData(Key.Z, ModifierKeys.Control, "UndoCommand")]
    public void EachShortcutRunsTheSameCommandAsItsButton(Key key, ModifierKeys modifiers, string commandName)
    {
        WpfTestHost.Run(w =>
        {
            KeyBinding? binding = w.InputBindings.OfType<KeyBinding>()
                .FirstOrDefault(b => b.Key == key && b.Modifiers == modifiers);
            Assert.True(binding is not null, $"No KeyBinding for {modifiers}+{key} in Window.InputBindings.");

            object expected = typeof(TallyViewModel).GetProperty(commandName)!.GetValue(w.Tally)!;
            Assert.Same(expected, binding!.Command);
        });
    }
}
