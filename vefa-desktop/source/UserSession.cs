namespace VefaChatBot
{
    public static class UserSession
    {
        public static string Email { get; set; } = string.Empty;

        public static void ClearSession()
        {
            Email = string.Empty;
        }
    }
}
