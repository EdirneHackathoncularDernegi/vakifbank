using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace VefaChatBot
{
    public static class ApiClient
    {
        private static readonly HttpClient client = new HttpClient();

        public static async Task<string> GetChatBotResponse(string userInput)
        {
            string apiUrl = "https://your-chatbot-api.com/respond";
            var parameters = new Dictionary<string, string>
            {
                { "input", userInput }
            };

            var content = new FormUrlEncodedContent(parameters);
            HttpResponseMessage response = await client.PostAsync(apiUrl, content);

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return "ChatBot API'ye bağlanırken bir hata oluştu.";
            }
        }
    }
}
