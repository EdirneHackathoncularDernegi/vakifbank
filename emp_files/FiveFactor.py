class BesFaktorKisilikOlcegi:
    def __init__(self):
        self.faktorler = {
            "Dışadönüklük": {
                "sorular": [
                    "1. İnsanlarla konuşmayı severim.",
                    "2. Kalabalık gruplarda kendimi rahat hissederim.",
                    "3. Çevremdekilere enerji veren bir yapım vardır.",
                    "4. Eğlenceli ve keyifli biri olarak tanınırım.",
                    "5. Sosyal etkinliklere katılmayı tercih ederim.",
                    "6. Yeni insanlarla tanışmayı kolay bulurum.",
                    "7. Yalnız kalmayı tercih ederim.",  # Ters
                    "8. İletişim kurarken kendimi ifade etmekte zorlanırım.",  # Ters
                    "9. Göz önünde olmaktan hoşlanırım.",
                    "10. Konuşmalarımı enerjik bir şekilde sürdürürüm."
                ],
                "ters_sorular": [7, 8]
            },
            "Uyumluluk": {
                "sorular": [
                    "11. İnsanlara yardım etmekten keyif alırım.",
                    "12. Çoğu zaman başkalarının ihtiyaçlarını kendi ihtiyaçlarımın önüne koyarım.",
                    "13. İnsanlar beni güvenilir biri olarak görür.",
                    "14. İş arkadaşlarıma destek vermekten mutluluk duyarım.",
                    "15. Başkalarının duygularını anlama konusunda iyiyimdir.",
                    "16. Çatışmalardan kaçınmaya çalışırım.",
                    "17. Karşımdakine empatiyle yaklaşırım.",
                    "18. Kendi fikirlerimi savunma konusunda ısrarcıyımdır.",  # Ters
                    "19. İnsanların ihtiyaçlarını dikkate alırım.",
                    "20. Beni zorlasa bile işbirliği yaparım."
                ],
                "ters_sorular": [18]
            },
            "Özdenetim": {
                "sorular": [
                    "21. İşlerimi düzenli bir şekilde yürütürüm.",
                    "22. Uzun vadeli hedeflerime sadık kalırım.",
                    "23. Zamanımı iyi yönetebilirim.",
                    "24. Plan yapmadan çalışmayı tercih ederim.",  # Ters
                    "25. Sorumluluk almayı severim.",
                    "26. Görevlerimi zamanında tamamlarım.",
                    "27. Ertelemeyi alışkanlık haline getiririm.",  # Ters
                    "28. Çalışma ortamımı organize ederim.",
                    "29. Disiplinli bir şekilde çalışırım.",
                    "30. Beklenmedik durumlarda planlarımı değiştirmekte zorlanırım."
                ],
                "ters_sorular": [24, 27]
            },
            "Nörotiklik": {
                "sorular": [
                    "31. Stresli durumlarda kolayca kaygılanırım.",
                    "32. Duygusal dalgalanmalar yaşarım.",
                    "33. Kritik anlarda sakin kalmakta zorlanırım.",
                    "34. Çabuk sinirlenirim.",
                    "35. Küçük sorunlar beni strese sokar.",
                    "36. Belirsizlikten hoşlanmam.",
                    "37. Zor durumlarla baş etmekte zorlanırım.",
                    "38. Hayal kırıklığına uğradığımda sakin kalırım.",  # Ters
                    "39. Kendime güvenim tamdır.",  # Ters
                    "40. Kaygılı bir yapıya sahibim."
                ],
                "ters_sorular": [38, 39]
            },
            "Deneyime Açıklık": {
                "sorular": [
                    "41. Yeni fikirleri ve değişiklikleri kucaklarım.",
                    "42. Farklı kültürlerden insanlar ve gelenekler beni etkiler.",
                    "43. Sanat, müzik ve edebiyat gibi alanlarda yeniliklere açık biriyimdir.",
                    "44. Hayal gücümü kullanmayı severim.",
                    "45. Merak duygum yüksektir.",
                    "46. Rutin işler beni sıkar.",
                    "47. Yaratıcı aktivitelerden keyif alırım.",
                    "48. Farklı bakış açılarını anlamaya çalışırım.",
                    "49. Yenilikleri hayatıma adapte etmekte zorlanırım.",  # Ters
                    "50. Teknolojik yenilikleri takip ederim."
                ],
                "ters_sorular": [49]
            }
        }

    def ters_puanlama(self, puan):
        return 6 - puan

    def yanitlari_al(self, faktor):
        sorular = self.faktorler[faktor]["sorular"]
        ters_sorular = self.faktorler[faktor]["ters_sorular"]
        puanlar = []
        print(f"\nFaktör: {faktor}")
        for i, soru in enumerate(sorular, 1):
            yanit = int(input(f"{soru} (1-5): "))
            if i in ters_sorular:
                yanit = self.ters_puanlama(yanit)
            puanlar.append(yanit)
        return sum(puanlar)

    def puanlama(self):
        toplam_puanlar = {}
        for faktor in self.faktorler:
            toplam_puanlar[faktor] = self.yanitlari_al(faktor)
        return toplam_puanlar


# Ana kod
if __name__ == "__main__":
    test = BesFaktorKisilikOlcegi()
    sonuc = test.puanlama()
    print("\nBeş Faktör Kişilik Ölçeği Sonuçları:")
    for faktor, puan in sonuc.items():
        print(f"{faktor}: {puan}/50")
