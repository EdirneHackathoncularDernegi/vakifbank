using Microsoft.Win32;
using System;
using System.Windows.Forms;

namespace VefaChatBot
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            SetBrowserFeatureControl();
            Application.Run(new Form1());
        }

        private static void SetBrowserFeatureControl()
        {
            string appName = System.IO.Path.GetFileName(Application.ExecutablePath);

            using (var key = Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BROWSER_EMULATION"))
            {
                key?.SetValue(appName, 11001, RegistryValueKind.DWord);
            }
        }
    }
}
