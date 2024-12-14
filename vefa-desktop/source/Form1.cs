using System;
using System.Windows.Forms;

namespace VefaChatBot
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            string email = txtEmail.Text;
            string password = txtPassword.Text;

            if (email == "test@matiricie.com" && password == "test")
            {
                MessageBox.Show("Başarıyla giriş yaptınız!", "Başarılı", MessageBoxButtons.OK, MessageBoxIcon.Information);

                ChatBotForm chatBot = new ChatBotForm();
                chatBot.Show();
                this.Hide();
            }
            else
            {
                MessageBox.Show("Hatalı e-posta veya şifre. Lütfen tekrar deneyin.", "Hata", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
