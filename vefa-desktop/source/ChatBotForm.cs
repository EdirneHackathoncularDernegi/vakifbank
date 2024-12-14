using System;
using System.Windows.Forms;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.WinForms;

namespace VefaChatBot
{
    public class ChatBotForm : Form
    {
        private WebView2 webView;

        public ChatBotForm()
        {
            this.Text = "ChatBot - Vefa";
            this.Size = new System.Drawing.Size(800, 600);
            this.StartPosition = FormStartPosition.CenterScreen;
            webView = new WebView2
            {
                Dock = DockStyle.Fill
            };

            this.Controls.Add(webView);
            this.Load += ChatBotForm_Load;
        }

        private async void ChatBotForm_Load(object sender, EventArgs e)
        {
            await webView.EnsureCoreWebView2Async(null);
            webView.CoreWebView2.Navigate("https://app.livechatai.com/ai-bot/cm4o95w7k0001ialzvmdu19to");
        }
    }
}
