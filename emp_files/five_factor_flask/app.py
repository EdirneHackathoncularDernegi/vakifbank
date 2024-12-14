from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)
@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)
faktorler = {
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

def ters_puanlama(puan):
    """Ters puanlama yapılacak sorular için 6'dan çıkarılır."""
    return 6 - puan

@app.route('/')
def index():
    return render_template('index.html', faktorler=faktorler)

@app.route('/submit', methods=['POST'])
def submit():
    # Kullanıcı yanıtlarını al ve puanları hesapla
    toplam_puanlar = {}
    raw_data = {}
    for faktor, bilgiler in faktorler.items():
        sorular = bilgiler["sorular"]
        ters_sorular = bilgiler["ters_sorular"]
        puanlar = []
        yanitlar = {}

        for i, soru in enumerate(sorular, 1):
            yanit = int(request.form.get(f"{faktor}_{i}"))
            yanitlar[f"Soru {i}"] = yanit
            if i in ters_sorular:
                yanit = ters_puanlama(yanit)
            puanlar.append(yanit)
        
        toplam_puanlar[faktor] = sum(puanlar)
        raw_data[faktor] = yanitlar

    # Ham veriyi kaydet
    with open("ham_veriler.json", "w") as file:
        json.dump(raw_data, file, indent=4)

    return render_template('result.html', puanlar=toplam_puanlar)

@app.route('/ham_veri')
def ham_veri():
    try:
        with open("ham_veriler.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return "Henüz ham veri kaydedilmedi."

@app.route('/analiz')
def detayli_analiz(puanlar):
    yorumlar = {}
    for faktor, puan in puanlar.items():
        if faktor == "Dışadönüklük":
            if puan >= 40:
                yorumlar[faktor] = "Sosyal, konuşkan ve enerjik bir yapınız var. İş ortamında grup projelerine öncülük edebilir, diğer çalışanları motive edebilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde dışadönüksünüz. Sosyal ortamlarda kendinizi rahat hissetseniz de, bireysel çalışmalarda da başarılı olabilirsiniz."
            else:
                yorumlar[faktor] = "Daha içedönük bir yapınız var. Daha sessiz bir çalışma ortamı tercih edebilir ve bireysel projelerde daha üretken olabilirsiniz."
        
        elif faktor == "Uyumluluk":
            if puan >= 40:
                yorumlar[faktor] = "Son derece yardımsever, empati sahibi ve iş birliğine açık bir yapınız var. Çatışma çözümünde etkili olabilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde uyumlusunuz. İş birliğine açık olsanız da, bazen kendi fikirlerinizi savunma konusunda kararlı olabilirsiniz."
            else:
                yorumlar[faktor] = "Daha bireysel hareket eden bir yapınız var. İş yerinde çatışma durumlarında bağımsız çalışmayı tercih edebilirsiniz."

        elif faktor == "Özdenetim":
            if puan >= 40:
                yorumlar[faktor] = "Son derece düzenli, planlı ve sorumluluk sahibi bir yapınız var. Zaman yönetimi ve iş takibi konusunda örnek olabilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde özdenetim beceriniz var. Genel olarak düzenli çalışsanız da, zaman zaman planlama eksiklikleri yaşayabilirsiniz."
            else:
                yorumlar[faktor] = "Daha plansız ve düzensiz bir yapınız var. Zaman yönetimi ve iş takibi konusunda desteğe ihtiyaç duyabilirsiniz."

        elif faktor == "Nörotiklik":
            if puan >= 40:
                yorumlar[faktor] = "Stres ve duygusal dalgalanmalar konusunda hassas bir yapınız var. Daha sakin kalmayı öğrenmek için stres yönetimi eğitimleri alabilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde nörotiklik özellikleri gösteriyorsunuz. Çoğu durumda sakin kalabilseniz de, zorlayıcı durumlarda kendinizi stresli hissedebilirsiniz."
            else:
                yorumlar[faktor] = "Duygusal açıdan dengeli ve sakin bir yapınız var. Zorlayıcı durumlarla başa çıkma konusunda başarılısınız."

        elif faktor == "Deneyime Açıklık":
            if puan >= 40:
                yorumlar[faktor] = "Yaratıcı, yeniliklere açık ve öğrenmeye meraklı bir yapınız var. Farklı projelerde yeni fikirler geliştirebilir ve çeşitlilikten keyif alabilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde deneyime açıklığınız var. Yeniliklere açık olsanız da, zaman zaman alışılmış yöntemleri tercih edebilirsiniz."
            else:
                yorumlar[faktor] = "Daha geleneksel bir yapınız var. Yeniliklere adapte olmakta zorlanabilirsiniz, ancak bu sizi derinlemesine uzmanlaşmaya yönlendirebilir."

        else:
            yorumlar[faktor] = f"{faktor} için detaylı analiz henüz eklenmedi."

    return yorumlar


if __name__ == '__main__':
    app.run(debug=True)