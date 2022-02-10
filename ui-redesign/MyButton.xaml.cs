using System;
using System.Windows.Input;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace MindTrailsHome.CustomControls
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class MyButton : ContentView
    {
        public event EventHandler Clicked;
        public static readonly BindableProperty ButtonText
        = BindableProperty.Create(nameof(Text), typeof(string), typeof(MyButton));

        public string Text
        {
            get => (string)GetValue(ButtonText);
            set => SetValue(ButtonText, value);
        }

        public static readonly BindableProperty ButtonImage
        = BindableProperty.Create(nameof(Image), typeof(string), typeof(MyButton));

        public string Image
        {
            get => (string)GetValue(ButtonImage);
            set => SetValue(ButtonImage, value);
        }

        public static readonly BindableProperty BgColor
        = BindableProperty.Create(nameof(FrameBackgroundColor), typeof(string), typeof(MyButton), "#00");

        public string FrameBackgroundColor
        {
            get => (string)GetValue(BgColor);
            set => SetValue(BgColor, value);
        }

        //public static readonly BindableProperty buttonOpacity =
        //    BindableProperty.Create(nameof(Opacity), typeof(string), typeof(MyButton), "#00");

        //public string Opacity
        //{
        //    get => (string)GetValue(buttonOpacity);
        //    set => SetValue(buttonOpacity, value);
        //}

        public static readonly BindableProperty TxtColor
        = BindableProperty.Create(nameof(TextColor), typeof(string), typeof(MyButton), "#FFFFFF");

        public string TextColor
        {
            get => (string)GetValue(TxtColor);
            set => SetValue(TxtColor, value);
        }

        public static readonly BindableProperty CommandProperty = BindableProperty.Create(nameof(Command),
        typeof(ICommand), typeof(MyButton), null);

        public ICommand Command
        {
            get => (ICommand)GetValue(CommandProperty);
            set => SetValue(CommandProperty, value);
        }

        public static readonly BindableProperty CommandPropertyParam = BindableProperty.Create(nameof(CommandParam),
        typeof(object), typeof(MyButton), null);

        public object CommandParam
        {
            get => (object)GetValue(CommandPropertyParam);
            set => SetValue(CommandPropertyParam, value);
        }
        public MyButton()
        {
            InitializeComponent();

            this.GestureRecognizers.Add(new TapGestureRecognizer
            {
                Command = new Command(() => {
                    Clicked?.Invoke(this, EventArgs.Empty);
                    if (Command != null)
                    {
                        if (Command.CanExecute(CommandParam))
                            Command.Execute(CommandParam);
                    }
                })

            });
        }
        protected override void OnParentSet()
        {
            base.OnParentSet();
            btnIcon.Source = Image;
            btnText.Text = Text;
            myFrame.BackgroundColor = Color.FromHex(FrameBackgroundColor);
            btnText.TextColor = Color.FromHex(TextColor);

            //stack.BackgroundColor = Color.FromHex(FrameBackgroundColor);
            //btnText.BackgroundColor = Color.FromHex(FrameBackgroundColor);
            //btnIcon.BackgroundColor = Color.FromHex(FrameBackgroundColor);
        }

    }
}
