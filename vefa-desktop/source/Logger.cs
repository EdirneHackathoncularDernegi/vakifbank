using System;
using System.IO;
using System.Windows.Forms;

namespace VefaChatBot
{
    public static class Logger
    {
        private static readonly string logFilePath = "log.txt";

        public static void Log(string message)
        {
            try
            {
                using (StreamWriter writer = new StreamWriter(logFilePath, true))
                {
                    writer.WriteLine($"{DateTime.Now}: {message}");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Loglama sırasında bir hata oluştu: {ex.Message}");
            }
        }
    }
}
